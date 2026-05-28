"""Dialog for recording an update event (台账)."""
from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from .style import ACCENT, BG_ELEVATED, BORDER, DANGER, TEXT_PRIMARY, TEXT_SECONDARY

STATUS_OPTIONS = [
    ("success",     "成功"),
    ("failed",      "失败"),
    ("rolled_back", "已回滚"),
    ("in_progress", "进行中"),
    ("other",       "其他"),
]


class RecordDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        methods: list[tuple[int, str]] | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("记录更新")
        self.setMinimumWidth(440)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self._methods = methods or []
        self._build_ui()

    def _build_ui(self) -> None:
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 24)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────
        title = QtWidgets.QLabel("记录更新")
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

        # Method
        self._method_combo = QtWidgets.QComboBox()
        self._method_combo.setFixedHeight(38)
        self._method_combo.addItem("（不关联）", None)
        for mid, mname in self._methods:
            self._method_combo.addItem(mname, mid)
        form.addRow(_lbl("更新方式"), self._method_combo)

        # Version
        self._version = QtWidgets.QLineEdit()
        self._version.setPlaceholderText("如 v2.1.0")
        self._version.setFixedHeight(38)
        form.addRow(_lbl("版本号"), self._version)

        # Operator
        self._operator = QtWidgets.QLineEdit()
        self._operator.setPlaceholderText("操作人")
        self._operator.setFixedHeight(38)
        form.addRow(_lbl("操作人"), self._operator)

        # Status
        self._status_combo = QtWidgets.QComboBox()
        self._status_combo.setFixedHeight(38)
        for value, display in STATUS_OPTIONS:
            self._status_combo.addItem(display, value)
        form.addRow(_lbl("状态"), self._status_combo)

        # Notes
        self._notes = QtWidgets.QLineEdit()
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

        btn_ok = QtWidgets.QPushButton("提交")
        btn_ok.setObjectName("btn_primary")
        btn_ok.setFixedHeight(38)
        btn_ok.setMinimumWidth(80)
        btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_ok.clicked.connect(self._on_ok)
        btn_row.addWidget(btn_ok)

        root.addLayout(btn_row)

    def _on_ok(self) -> None:
        if not self._version.text().strip():
            self._version.setStyleSheet(f"border: 1px solid {DANGER}; border-radius: 6px;")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "method_id": self._method_combo.currentData(),
            "version":   self._version.text().strip(),
            "operator":  self._operator.text().strip(),
            "status":    self._status_combo.currentData(),
            "notes":     self._notes.text().strip(),
        }
