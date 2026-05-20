"""Dialog for recording an update event (台账)."""
from __future__ import annotations

from PySide6 import QtWidgets

STATUS_OPTIONS = ["success", "failed", "rolled_back", "in_progress", "other"]


class RecordDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        methods: list[tuple[int, str]] | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("记录更新")
        self.setMinimumWidth(400)
        self._methods = methods or []
        self._build_ui()

    def _build_ui(self) -> None:
        form = QtWidgets.QFormLayout(self)

        self._method_combo = QtWidgets.QComboBox()
        self._method_combo.addItem("（无 / 不关联）", None)
        for mid, mname in self._methods:
            self._method_combo.addItem(mname, mid)
        form.addRow("关联更新方式：", self._method_combo)

        self._version = QtWidgets.QLineEdit()
        self._version.setPlaceholderText("如 v2.1.0")
        form.addRow("版本号：", self._version)

        self._operator = QtWidgets.QLineEdit()
        self._operator.setPlaceholderText("操作人姓名")
        form.addRow("操作人：", self._operator)

        self._status_combo = QtWidgets.QComboBox()
        for s in STATUS_OPTIONS:
            self._status_combo.addItem(s)
        form.addRow("状态：", self._status_combo)

        self._notes = QtWidgets.QLineEdit()
        self._notes.setPlaceholderText("备注（可选）")
        form.addRow("备注：", self._notes)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btns.accepted.connect(self._on_ok)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def _on_ok(self) -> None:
        if not self._version.text().strip():
            QtWidgets.QMessageBox.warning(self, "提示", "版本号不能为空")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "method_id": self._method_combo.currentData(),
            "version": self._version.text().strip(),
            "operator": self._operator.text().strip(),
            "status": self._status_combo.currentText(),
            "notes": self._notes.text().strip(),
        }
