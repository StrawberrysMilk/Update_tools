"""Dialog for adding / editing an update method."""
from __future__ import annotations

from PySide6 import QtWidgets

METHOD_KINDS = [
    ("ssh_command", "SSH 命令"),
    ("sftp_push", "SFTP 推送"),
    ("manual_rdp", "手工远程桌面"),
    ("custom", "自定义"),
]


class MethodDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        data: dict | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("编辑更新方式" if data else "新增更新方式")
        self.setMinimumWidth(450)
        self._data = data or {}
        self._build_ui()

    def _build_ui(self) -> None:
        form = QtWidgets.QFormLayout(self)

        self._name = QtWidgets.QLineEdit(self._data.get("name", ""))
        form.addRow("名称：", self._name)

        self._kind_combo = QtWidgets.QComboBox()
        for value, display in METHOD_KINDS:
            self._kind_combo.addItem(display, value)
        idx = next(
            (i for i, (v, _) in enumerate(METHOD_KINDS) if v == self._data.get("kind", "ssh_command")),
            0,
        )
        self._kind_combo.setCurrentIndex(idx)
        form.addRow("类型：", self._kind_combo)

        self._payload = QtWidgets.QTextEdit()
        self._payload.setPlainText(self._data.get("payload", ""))
        self._payload.setPlaceholderText(
            '命令 / 脚本 / JSON 配置\n例：{"cmd": "systemctl restart app"}'
        )
        self._payload.setMaximumHeight(120)
        form.addRow("执行内容：", self._payload)

        self._notes = QtWidgets.QLineEdit(self._data.get("notes", ""))
        self._notes.setPlaceholderText("备注（可选）")
        form.addRow("备注：", self._notes)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btns.accepted.connect(self._on_ok)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def _on_ok(self) -> None:
        if not self._name.text().strip():
            QtWidgets.QMessageBox.warning(self, "提示", "名称不能为空")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "name": self._name.text().strip(),
            "kind": self._kind_combo.currentData(),
            "payload": self._payload.toPlainText().strip(),
            "notes": self._notes.text().strip(),
        }
