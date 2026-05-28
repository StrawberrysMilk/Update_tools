"""Dialog for adding / editing an update method."""
from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from .style import ACCENT, BG_ELEVATED, BORDER, DANGER, TEXT_PRIMARY, TEXT_SECONDARY

METHOD_KINDS = [
    ("ssh_command", "SSH 命令"),
    ("sftp_push",   "SFTP 推送"),
    ("manual_rdp",  "手工远程桌面"),
    ("custom",      "自定义"),
]


class MethodDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        data: dict | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("编辑更新方式" if data else "新增更新方式")
        self.setMinimumWidth(480)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self._data = data or {}
        self._build_ui()

    def _build_ui(self) -> None:
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 24)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────
        title = QtWidgets.QLabel("编辑更新方式" if self._data else "新增更新方式")
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

        # Name
        self._name = QtWidgets.QLineEdit(self._data.get("name", ""))
        self._name.setPlaceholderText("如：生产环境部署脚本")
        self._name.setFixedHeight(38)
        form.addRow(_lbl("名称"), self._name)

        # Kind
        self._kind_combo = QtWidgets.QComboBox()
        self._kind_combo.setFixedHeight(38)
        for value, display in METHOD_KINDS:
            self._kind_combo.addItem(display, value)
        idx = next(
            (i for i, (v, _) in enumerate(METHOD_KINDS)
             if v == self._data.get("kind", "ssh_command")), 0,
        )
        self._kind_combo.setCurrentIndex(idx)
        form.addRow(_lbl("类型"), self._kind_combo)

        # Payload
        self._payload = QtWidgets.QTextEdit()
        self._payload.setPlainText(self._data.get("payload", ""))
        self._payload.setPlaceholderText(
            '命令 / 脚本 / JSON 配置\n例：{"cmd": "systemctl restart app"}'
        )
        self._payload.setFixedHeight(120)
        self._payload.setStyleSheet(f"""
            QTextEdit {{
                background-color: {BG_ELEVATED};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 8px 12px;
                color: {TEXT_PRIMARY};
            }}
            QTextEdit:focus {{
                border-color: {ACCENT};
            }}
        """)
        form.addRow(_lbl("执行内容"), self._payload)

        # Notes
        self._notes = QtWidgets.QLineEdit(self._data.get("notes", ""))
        self._notes.setPlaceholderText("备注")
        self._notes.setFixedHeight(38)
        form.addRow(_lbl("备注"), self._notes)

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
        if not self._name.text().strip():
            self._name.setStyleSheet(f"border: 1px solid {DANGER}; border-radius: 6px;")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "name":    self._name.text().strip(),
            "kind":    self._kind_combo.currentData(),
            "payload": self._payload.toPlainText().strip(),
            "notes":   self._notes.text().strip(),
        }
