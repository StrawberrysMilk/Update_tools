"""Master password dialog: first-run setup or subsequent unlock."""
from __future__ import annotations

import json
import os

from PySide6 import QtCore, QtGui, QtWidgets

from ..config import META_PATH
from ..crypto import decrypt, derive_key, encrypt
from .style import (
    ACCENT, ACCENT_HOVER, BG_BASE, BG_ELEVATED, BG_SURFACE,
    BORDER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DISABLED, DANGER,
    RADIUS_LG,
)

_VERIFY_PLAINTEXT = "UPDATE_TOOLS_OK"


class UnlockDialog(QtWidgets.QDialog):
    """Prompt for the master password (first-run setup or unlock)."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("UpdateTools")
        self.setFixedSize(400, 480)
        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.key: bytes | None = None
        self._first_run: bool = not META_PATH.exists()
        self._drag_pos: QtCore.QPoint | None = None
        self._build_ui()

    # ── UI ─────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)

        # Card
        self._card = QtWidgets.QFrame()
        self._card.setObjectName("unlock_card")
        self._card.setStyleSheet(f"""
            QFrame#unlock_card {{
                background-color: {BG_SURFACE};
                border-radius: {RADIUS_LG};
                border: 1px solid {BORDER};
            }}
        """)

        shadow = QtWidgets.QGraphicsDropShadowEffect(self._card)
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 160))
        self._card.setGraphicsEffect(shadow)

        outer.addWidget(self._card)

        vl = QtWidgets.QVBoxLayout(self._card)
        vl.setContentsMargins(40, 48, 40, 40)
        vl.setSpacing(0)

        # ── Icon ───────────────────────────────────────────────────────────
        icon_label = QtWidgets.QLabel("⚿")  # lock unicode
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            font-size: 40px;
            background: transparent;
            color: {ACCENT};
        """)
        vl.addWidget(icon_label)
        vl.addSpacing(20)

        # ── Title ─────────────────────────────────────────────────────────
        title = QtWidgets.QLabel("UpdateTools")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 22px;
            font-weight: 700;
            color: {TEXT_PRIMARY};
            background: transparent;
            letter-spacing: 1px;
        """)
        vl.addWidget(title)
        vl.addSpacing(6)

        if self._first_run:
            sub_text = "首次使用，请设置主密码"
        else:
            sub_text = "输入主密码以继续"
        subtitle = QtWidgets.QLabel(sub_text)
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            font-size: 13px;
            color: {TEXT_SECONDARY};
            background: transparent;
        """)
        vl.addWidget(subtitle)
        vl.addSpacing(36)

        # ── Password field ────────────────────────────────────────────────
        self._pw = QtWidgets.QLineEdit()
        self._pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self._pw.setPlaceholderText("主密码")
        self._pw.setFixedHeight(44)
        self._pw.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_ELEVATED};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 0 16px;
                font-size: 14px;
                color: {TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border-color: {ACCENT};
            }}
        """)
        self._pw.returnPressed.connect(self._on_ok)
        vl.addWidget(self._pw)

        if self._first_run:
            vl.addSpacing(12)

            self._pw2 = QtWidgets.QLineEdit()
            self._pw2.setEchoMode(QtWidgets.QLineEdit.Password)
            self._pw2.setPlaceholderText("确认密码")
            self._pw2.setFixedHeight(44)
            self._pw2.setStyleSheet(self._pw.styleSheet())
            self._pw2.returnPressed.connect(self._on_ok)
            vl.addWidget(self._pw2)

            vl.addSpacing(16)
            hint = QtWidgets.QLabel("密码丢失后数据将无法恢复")
            hint.setAlignment(QtCore.Qt.AlignCenter)
            hint.setStyleSheet(f"""
                color: {TEXT_DISABLED};
                font-size: 11px;
                background: transparent;
            """)
            vl.addWidget(hint)
        else:
            self._pw2 = None

        vl.addSpacing(24)

        # ── Error label ───────────────────────────────────────────────────
        self._err_label = QtWidgets.QLabel("")
        self._err_label.setAlignment(QtCore.Qt.AlignCenter)
        self._err_label.setStyleSheet(f"""
            color: {DANGER};
            font-size: 12px;
            background: transparent;
        """)
        self._err_label.setVisible(False)
        vl.addWidget(self._err_label)
        vl.addSpacing(8)

        # ── Buttons ───────────────────────────────────────────────────────
        btn_ok = QtWidgets.QPushButton("设置密码" if self._first_run else "解锁")
        btn_ok.setObjectName("btn_primary")
        btn_ok.setFixedHeight(44)
        btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {ACCENT_HOVER};
            }}
        """)
        btn_ok.clicked.connect(self._on_ok)
        vl.addWidget(btn_ok)

        vl.addStretch()

    # ── Drag to move (frameless) ───────────────────────────────────────────

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self._drag_pos is not None and event.buttons() & QtCore.Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self._drag_pos = None

    # ── Logic ──────────────────────────────────────────────────────────────

    def _show_error(self, msg: str) -> None:
        self._err_label.setText(msg)
        self._err_label.setVisible(True)

    def _on_ok(self) -> None:
        self._err_label.setVisible(False)
        pw = self._pw.text()
        if not pw:
            self._show_error("密码不能为空")
            return

        if self._first_run:
            assert self._pw2 is not None
            if pw != self._pw2.text():
                self._show_error("两次输入的密码不一致")
                return
            if len(pw) < 6:
                self._show_error("主密码至少 6 位")
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
            self._show_error("密码错误")
            self._pw.clear()
            self._pw.setFocus()
            return
        self.key = key
        self.accept()
