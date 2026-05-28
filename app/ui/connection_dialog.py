"""Dialog for adding / editing a connection entry."""
from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from .style import (
    ACCENT, BG_ELEVATED, BORDER, DANGER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DISABLED,
)

CONNECTION_TYPES = [
    ("rdp",     "远程桌面 (RDP)"),
    ("ssh",     "SSH"),
    ("browser", "浏览器地址"),
    ("custom",  "自定义命令"),
]


class ConnectionDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        data: dict | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("编辑连接" if data else "新增连接")
        self.setMinimumWidth(460)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self._data = data or {}
        self._build_ui()

    def _build_ui(self) -> None:
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 24)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────
        title = QtWidgets.QLabel("编辑连接" if self._data else "新增连接")
        title.setStyleSheet(f"""
            font-size: 17px;
            font-weight: 700;
            color: {TEXT_PRIMARY};
            background: transparent;
        """)
        root.addWidget(title)
        root.addSpacing(24)

        # ── Form ──────────────────────────────────────────────────────────
        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        form.setHorizontalSpacing(16)
        form.setVerticalSpacing(14)
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)

        def _lbl(text: str) -> QtWidgets.QLabel:
            l = QtWidgets.QLabel(text)
            l.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px; background: transparent;")
            return l

        # Label
        self._label = QtWidgets.QLineEdit(self._data.get("label", ""))
        self._label.setPlaceholderText("如：生产环境 RDP")
        self._label.setFixedHeight(38)
        form.addRow(_lbl("标签"), self._label)

        # Type
        self._type_combo = QtWidgets.QComboBox()
        self._type_combo.setFixedHeight(38)
        for value, display in CONNECTION_TYPES:
            self._type_combo.addItem(display, value)
        idx = next(
            (i for i, (v, _) in enumerate(CONNECTION_TYPES)
             if v == self._data.get("type", "rdp")), 0,
        )
        self._type_combo.setCurrentIndex(idx)
        form.addRow(_lbl("类型"), self._type_combo)

        # Address
        self._address = QtWidgets.QLineEdit(self._data.get("address", ""))
        self._address.setPlaceholderText("IP / 域名 / URL / 命令")
        self._address.setFixedHeight(38)
        form.addRow(_lbl("地址"), self._address)

        # Port
        self._port = QtWidgets.QSpinBox()
        self._port.setRange(0, 65535)
        self._port.setSpecialValueText("默认")
        self._port.setValue(self._data.get("port", 0) or 0)
        self._port.setFixedHeight(38)
        self._port.setFixedWidth(120)
        form.addRow(_lbl("端口"), self._port)

        # Username
        self._username = QtWidgets.QLineEdit(self._data.get("username", ""))
        self._username.setPlaceholderText("用户名")
        self._username.setFixedHeight(38)
        form.addRow(_lbl("用户名"), self._username)

        # Password row with show/hide toggle
        pw_row = QtWidgets.QHBoxLayout()
        pw_row.setSpacing(8)
        self._password = QtWidgets.QLineEdit(self._data.get("password", ""))
        self._password.setEchoMode(QtWidgets.QLineEdit.Password)
        self._password.setPlaceholderText("密码")
        self._password.setFixedHeight(38)
        pw_row.addWidget(self._password)

        self._eye_btn = QtWidgets.QPushButton("显示")
        self._eye_btn.setFixedSize(52, 38)
        self._eye_btn.setCheckable(True)
        self._eye_btn.setStyleSheet(f"""
            QPushButton {{
                background: {BG_ELEVATED};
                border: 1px solid {BORDER};
                border-radius: 6px;
                color: {TEXT_SECONDARY};
                font-size: 11px;
            }}
            QPushButton:checked {{
                background: {ACCENT};
                border-color: {ACCENT};
                color: #ffffff;
            }}
        """)
        self._eye_btn.toggled.connect(
            lambda on: self._password.setEchoMode(
                QtWidgets.QLineEdit.Normal if on else QtWidgets.QLineEdit.Password
            )
        )
        pw_row.addWidget(self._eye_btn)
        form.addRow(_lbl("密码"), pw_row)

        # Extra / notes
        self._extra = QtWidgets.QLineEdit(self._data.get("extra", ""))
        self._extra.setPlaceholderText("备注")
        self._extra.setFixedHeight(38)
        form.addRow(_lbl("备注"), self._extra)

        root.addLayout(form)
        root.addSpacing(28)

        # ── Buttons ───────────────────────────────────────────────────────
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        btn_cancel = QtWidgets.QPushButton("取消")
        btn_cancel.setFixedHeight(38)
        btn_cancel.setMinimumWidth(80)
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)

        btn_ok = QtWidgets.QPushButton("保存")
        btn_ok.setObjectName("btn_primary")
        btn_ok.setFixedHeight(38)
        btn_ok.setMinimumWidth(80)
        btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_ok.clicked.connect(self._on_ok)
        btn_row.addWidget(btn_ok)

        root.addLayout(btn_row)

    def _on_ok(self) -> None:
        if not self._address.text().strip():
            self._address.setStyleSheet(f"border: 1px solid {DANGER}; border-radius: 6px;")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "label":    self._label.text().strip(),
            "type":     self._type_combo.currentData(),
            "address":  self._address.text().strip(),
            "port":     self._port.value() or None,
            "username": self._username.text().strip(),
            "password": self._password.text(),
            "extra":    self._extra.text().strip(),
        }
