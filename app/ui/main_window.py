"""Main window (skeleton).

Layout:
    [ systems list ] | [ detail placeholder ]

Subsequent iterations will fill the detail panel with:
    - Connections table + 一键打开 buttons
    - Update methods editor
    - Update history (台账)
    - Excel import
"""
from __future__ import annotations

from PySide6 import QtCore, QtWidgets

from ..db import get_conn


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, key: bytes) -> None:
        super().__init__()
        self.key = key  # held in memory for this session only
        self.setWindowTitle("更新管理工具")
        self.resize(1100, 700)

        self._build_toolbar()
        self._build_central()
        self._refresh_systems()

    # ---- UI construction --------------------------------------------------

    def _build_toolbar(self) -> None:
        tb = self.addToolBar("main")
        tb.setMovable(False)

        act_add = tb.addAction("新增系统")
        act_add.triggered.connect(self._add_system)

        act_del = tb.addAction("删除系统")
        act_del.triggered.connect(self._delete_system)

        tb.addSeparator()
        # Placeholders, wired up in later iterations.
        for label in ("导入 Excel", "更新历史", "锁定"):
            a = tb.addAction(label)
            a.setEnabled(False)

    def _build_central(self) -> None:
        splitter = QtWidgets.QSplitter()

        self._system_list = QtWidgets.QListWidget()
        self._system_list.currentItemChanged.connect(self._on_system_selected)
        splitter.addWidget(self._system_list)

        self._detail = QtWidgets.QWidget()
        dl = QtWidgets.QVBoxLayout(self._detail)
        dl.setContentsMargins(16, 16, 16, 16)
        self._detail_label = QtWidgets.QLabel(
            "骨架版本\n\n"
            "下一步会接入：\n"
            "  • 连接条目（RDP / SSH / 浏览器 / 自定义）+ 一键打开\n"
            "  • 更新方式（SSH 命令 / SFTP / 手工 等）\n"
            "  • 更新历史台账\n"
            "  • Excel 导入"
        )
        self._detail_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        dl.addWidget(self._detail_label)
        dl.addStretch(1)
        splitter.addWidget(self._detail)

        splitter.setSizes([280, 820])
        self.setCentralWidget(splitter)

    # ---- actions ----------------------------------------------------------

    def _refresh_systems(self) -> None:
        self._system_list.clear()
        with get_conn() as c:
            for row in c.execute("SELECT id, name FROM systems ORDER BY name"):
                item = QtWidgets.QListWidgetItem(row["name"])
                item.setData(QtCore.Qt.UserRole, row["id"])
                self._system_list.addItem(item)

    def _add_system(self) -> None:
        name, ok = QtWidgets.QInputDialog.getText(self, "新增系统", "系统名称：")
        if not (ok and name.strip()):
            return
        with get_conn() as c:
            c.execute("INSERT INTO systems(name) VALUES(?)", (name.strip(),))
        self._refresh_systems()

    def _delete_system(self) -> None:
        item = self._system_list.currentItem()
        if item is None:
            return
        sys_id = item.data(QtCore.Qt.UserRole)
        if (
            QtWidgets.QMessageBox.question(
                self,
                "确认删除",
                f"确定要删除系统「{item.text()}」及其所有连接、更新方式和历史吗？",
            )
            != QtWidgets.QMessageBox.Yes
        ):
            return
        with get_conn() as c:
            c.execute("DELETE FROM systems WHERE id = ?", (sys_id,))
        self._refresh_systems()

    def _on_system_selected(
        self,
        current: QtWidgets.QListWidgetItem | None,
        _previous: QtWidgets.QListWidgetItem | None,
    ) -> None:
        if current is None:
            self._detail_label.setText("（未选择系统）")
            return
        sys_id = current.data(QtCore.Qt.UserRole)
        with get_conn() as c:
            row = c.execute(
                "SELECT name, notes, created_at FROM systems WHERE id = ?",
                (sys_id,),
            ).fetchone()
        if row is None:
            return
        self._detail_label.setText(
            f"系统：{row['name']}\n"
            f"创建时间：{row['created_at']}\n"
            f"备注：{row['notes'] or '（无）'}\n\n"
            "（详情面板将在下一轮迭代填充）"
        )
