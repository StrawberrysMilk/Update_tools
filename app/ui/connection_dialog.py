"""Dialog for adding / editing a connection entry."""
from __future__ import annotations

from PySide6 import QtWidgets

# Supported connection types and their display labels.
CONNECTION_TYPES = [
    ("rdp", "远程桌面 (RDP)"),
    ("ssh", "SSH"),
    ("browser", "浏览器地址"),
    ("custom", "自定义命令"),
]


class ConnectionDialog(QtWidgets.QDialog):
    """Modal dialog for a single connection entry.

    Pass ``data=dict(...)`` to pre-fill fields (edit mode).
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        data: dict | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("编辑连接" if data else "新增连接")
        self.setMinimumWidth(420)
        self._data = data or {}
        self._build_ui()

    def _build_ui(self) -> None:
        form = QtWidgets.QFormLayout(self)

        self._label = QtWidgets.QLineEdit(self._data.get("label", ""))
        form.addRow("标签：", self._label)

        self._type_combo = QtWidgets.QComboBox()
        for value, display in CONNECTION_TYPES:
            self._type_combo.addItem(display, value)
        idx = next(
            (i for i, (v, _) in enumerate(CONNECTION_TYPES) if v == self._data.get("type", "rdp")),
            0,
        )
        self._type_combo.setCurrentIndex(idx)
        form.addRow("类型：", self._type_combo)

        self._address = QtWidgets.QLineEdit(self._data.get("address", ""))
        self._address.setPlaceholderText("IP / 域名 / URL / 命令")
        form.addRow("地址 / 命令：", self._address)

        self._port = QtWidgets.QSpinBox()
        self._port.setRange(0, 65535)
        self._port.setSpecialValueText("默认")
        self._port.setValue(self._data.get("port", 0) or 0)
        form.addRow("端口：", self._port)

        self._username = QtWidgets.QLineEdit(self._data.get("username", ""))
        form.addRow("用户名：", self._username)

        self._password = QtWidgets.QLineEdit(self._data.get("password", ""))
        self._password.setEchoMode(QtWidgets.QLineEdit.Password)
        form.addRow("密码：", self._password)

        self._show_pw = QtWidgets.QCheckBox("显示密码")
        self._show_pw.toggled.connect(
            lambda checked: self._password.setEchoMode(
                QtWidgets.QLineEdit.Normal if checked else QtWidgets.QLineEdit.Password
            )
        )
        form.addRow("", self._show_pw)

        self._extra = QtWidgets.QLineEdit(self._data.get("extra", ""))
        self._extra.setPlaceholderText("备注 / 附加参数（可选）")
        form.addRow("备注：", self._extra)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btns.accepted.connect(self._on_ok)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def _on_ok(self) -> None:
        if not self._address.text().strip():
            QtWidgets.QMessageBox.warning(self, "提示", "地址 / 命令不能为空")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "label": self._label.text().strip(),
            "type": self._type_combo.currentData(),
            "address": self._address.text().strip(),
            "port": self._port.value() or None,
            "username": self._username.text().strip(),
            "password": self._password.text(),
            "extra": self._extra.text().strip(),
        }
