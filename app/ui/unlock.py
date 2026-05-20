"""Master password dialog: first-run setup or subsequent unlock."""
from __future__ import annotations

import json
import os

from PySide6 import QtWidgets

from ..config import META_PATH
from ..crypto import decrypt, derive_key, encrypt

# Plaintext used to verify a derived key matches the one used at setup.
_VERIFY_PLAINTEXT = "UPDATE_TOOLS_OK"


class UnlockDialog(QtWidgets.QDialog):
    """Prompt for the master password.

    On first run (no meta.json), asks the user to set a new password and
    persists the salt + verification token.

    On subsequent runs, verifies the entered password by decrypting the
    stored verification token.

    On success, ``self.key`` holds the 32-byte AES key.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("解锁 - 更新管理工具")
        self.setMinimumWidth(360)
        self.key: bytes | None = None
        self._first_run: bool = not META_PATH.exists()

        layout = QtWidgets.QVBoxLayout(self)

        if self._first_run:
            tip = (
                "首次使用，请设置主密码。\n"
                "此密码用于加密所有连接密码，丢失后已加密的数据无法恢复。"
            )
        else:
            tip = "请输入主密码以解锁。"
        layout.addWidget(QtWidgets.QLabel(tip))

        self._pw = QtWidgets.QLineEdit()
        self._pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self._pw.setPlaceholderText("主密码")
        layout.addWidget(self._pw)

        self._pw2: QtWidgets.QLineEdit | None = None
        if self._first_run:
            self._pw2 = QtWidgets.QLineEdit()
            self._pw2.setEchoMode(QtWidgets.QLineEdit.Password)
            self._pw2.setPlaceholderText("再次输入")
            layout.addWidget(self._pw2)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btns.accepted.connect(self._on_ok)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    # ---- handlers ---------------------------------------------------------

    def _on_ok(self) -> None:
        pw = self._pw.text()
        if not pw:
            QtWidgets.QMessageBox.warning(self, "提示", "密码不能为空")
            return

        if self._first_run:
            assert self._pw2 is not None
            if pw != self._pw2.text():
                QtWidgets.QMessageBox.warning(self, "提示", "两次输入的密码不一致")
                return
            if len(pw) < 6:
                QtWidgets.QMessageBox.warning(self, "提示", "主密码至少 6 位")
                return
            self._setup(pw)
        else:
            self._verify(pw)

    def _setup(self, pw: str) -> None:
        salt = os.urandom(16)
        key = derive_key(pw, salt)
        verify_token = encrypt(_VERIFY_PLAINTEXT, key)
        META_PATH.write_text(
            json.dumps({"salt": salt.hex(), "verify": verify_token}),
            encoding="utf-8",
        )
        self.key = key
        self.accept()

    def _verify(self, pw: str) -> None:
        try:
            meta = json.loads(META_PATH.read_text(encoding="utf-8"))
            salt = bytes.fromhex(meta["salt"])
            key = derive_key(pw, salt)
            if decrypt(meta["verify"], key) != _VERIFY_PLAINTEXT:
                raise ValueError("verify mismatch")
        except Exception:
            QtWidgets.QMessageBox.warning(self, "提示", "密码错误")
            return
        self.key = key
        self.accept()
