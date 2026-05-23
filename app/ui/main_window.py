"""Main window – full implementation.

Layout:
    [ systems list ] | [ TabWidget: 连接条目 | 更新方式 | 更新历史 ]
"""
from __future__ import annotations

from PySide6 import QtCore, QtWidgets

from ..crypto import decrypt, encrypt
from ..db import get_conn
from ..launcher import (
    launch_browser,
    launch_custom,
    launch_rdp,
    launch_ssh,
    launch_ssh_command,
)
import json
from .connection_dialog import ConnectionDialog
from .method_dialog import MethodDialog
from .record_dialog import RecordDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, key: bytes) -> None:
        super().__init__()
        self.key = key
        self._current_system_id: int | None = None
        self.setWindowTitle("更新管理工具")
        self.resize(1280, 800)

        self._build_toolbar()
        self._build_central()
        self._build_statusbar()
        self._refresh_systems()

    def _build_statusbar(self) -> None:
        sb = self.statusBar()
        sb.setStyleSheet("background:#f5f7fa; color:#666; padding:4px;")
        sb.showMessage("就绪 · 数据已加密存储")

    # ==================================================================
    # UI Construction
    # ==================================================================

    def _build_toolbar(self) -> None:
        tb = self.addToolBar("main")
        tb.setMovable(False)

        act_add = tb.addAction("+ 新增系统")
        act_add.triggered.connect(self._add_system)

        act_del = tb.addAction("- 删除系统")
        act_del.triggered.connect(self._delete_system)

        tb.addSeparator()

        act_import = tb.addAction("导入 Excel")
        act_import.triggered.connect(self._import_excel)

        tb.addSeparator()

        act_lock = tb.addAction("锁定")
        act_lock.triggered.connect(self._lock)

    def _build_central(self) -> None:
        splitter = QtWidgets.QSplitter()

        # Left panel: search + system list
        left = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(6)

        self._search = QtWidgets.QLineEdit()
        self._search.setPlaceholderText("🔍 搜索系统...")
        self._search.textChanged.connect(self._filter_systems)
        left_layout.addWidget(self._search)

        self._system_list = QtWidgets.QListWidget()
        self._system_list.currentItemChanged.connect(self._on_system_selected)
        left_layout.addWidget(self._system_list)

        splitter.addWidget(left)

        # Right panel: tabs (with margins)
        right = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(8, 8, 8, 8)

        self._tabs = QtWidgets.QTabWidget()
        self._build_connections_tab()
        self._build_methods_tab()
        self._build_records_tab()
        right_layout.addWidget(self._tabs)

        splitter.addWidget(right)

        splitter.setSizes([280, 1000])
        self.setCentralWidget(splitter)

    def _filter_systems(self, text: str) -> None:
        """Hide list items not matching the search text."""
        text = text.lower().strip()
        for i in range(self._system_list.count()):
            item = self._system_list.item(i)
            item.setHidden(text not in item.text().lower() if text else False)

    # ---- Connections Tab -------------------------------------------------

    def _build_connections_tab(self) -> None:
        w = QtWidgets.QWidget()
        vl = QtWidgets.QVBoxLayout(w)

        # Toolbar for connections
        hl = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("新增连接")
        btn_add.clicked.connect(self._add_connection)
        btn_edit = QtWidgets.QPushButton("编辑")
        btn_edit.clicked.connect(self._edit_connection)
        btn_del = QtWidgets.QPushButton("删除")
        btn_del.clicked.connect(self._delete_connection)
        btn_open = QtWidgets.QPushButton("一键打开")
        btn_open.clicked.connect(self._launch_connection)
        btn_open.setStyleSheet("font-weight:bold; color:#0066cc;")
        hl.addWidget(btn_add)
        hl.addWidget(btn_edit)
        hl.addWidget(btn_del)
        hl.addStretch()
        hl.addWidget(btn_open)
        vl.addLayout(hl)

        # Table
        self._conn_table = QtWidgets.QTableWidget()
        self._conn_table.setColumnCount(6)
        self._conn_table.setHorizontalHeaderLabels(
            ["标签", "类型", "地址", "端口", "用户名", "备注"]
        )
        self._conn_table.horizontalHeader().setStretchLastSection(True)
        self._conn_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self._conn_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self._conn_table.doubleClicked.connect(self._launch_connection)
        vl.addWidget(self._conn_table)

        self._tabs.addTab(w, "连接条目")

    # ---- Methods Tab -----------------------------------------------------

    def _build_methods_tab(self) -> None:
        w = QtWidgets.QWidget()
        vl = QtWidgets.QVBoxLayout(w)

        hl = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("新增更新方式")
        btn_add.clicked.connect(self._add_method)
        btn_edit = QtWidgets.QPushButton("编辑")
        btn_edit.clicked.connect(self._edit_method)
        btn_del = QtWidgets.QPushButton("删除")
        btn_del.clicked.connect(self._delete_method)
        btn_exec = QtWidgets.QPushButton("▶ 执行")
        btn_exec.clicked.connect(self._execute_method)
        btn_exec.setStyleSheet("font-weight:bold; color:#cc6600;")
        hl.addWidget(btn_add)
        hl.addWidget(btn_edit)
        hl.addWidget(btn_del)
        hl.addStretch()
        hl.addWidget(btn_exec)
        vl.addLayout(hl)

        self._method_table = QtWidgets.QTableWidget()
        self._method_table.setColumnCount(4)
        self._method_table.setHorizontalHeaderLabels(["名称", "类型", "执行内容", "备注"])
        self._method_table.horizontalHeader().setStretchLastSection(True)
        self._method_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self._method_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        vl.addWidget(self._method_table)

        self._tabs.addTab(w, "更新方式")

    # ---- Records Tab -----------------------------------------------------

    def _build_records_tab(self) -> None:
        w = QtWidgets.QWidget()
        vl = QtWidgets.QVBoxLayout(w)

        hl = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("记录一次更新")
        btn_add.clicked.connect(self._add_record)
        hl.addWidget(btn_add)
        hl.addStretch()
        vl.addLayout(hl)

        self._record_table = QtWidgets.QTableWidget()
        self._record_table.setColumnCount(6)
        self._record_table.setHorizontalHeaderLabels(
            ["时间", "版本", "操作人", "状态", "更新方式", "备注"]
        )
        self._record_table.horizontalHeader().setStretchLastSection(True)
        self._record_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self._record_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        vl.addWidget(self._record_table)

        self._tabs.addTab(w, "更新历史")

    # ==================================================================
    # System List Actions
    # ==================================================================

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
        self._current_system_id = None
        self._refresh_systems()
        self._clear_detail_tables()

    def _on_system_selected(
        self,
        current: QtWidgets.QListWidgetItem | None,
        _previous: QtWidgets.QListWidgetItem | None,
    ) -> None:
        if current is None:
            self._current_system_id = None
            self._clear_detail_tables()
            return
        self._current_system_id = current.data(QtCore.Qt.UserRole)
        self._refresh_connections()
        self._refresh_methods()
        self._refresh_records()

    def _clear_detail_tables(self) -> None:
        self._conn_table.setRowCount(0)
        self._method_table.setRowCount(0)
        self._record_table.setRowCount(0)

    # ==================================================================
    # Connection CRUD + Launch
    # ==================================================================

    def _refresh_connections(self) -> None:
        self._conn_table.setRowCount(0)
        if self._current_system_id is None:
            return
        with get_conn() as c:
            rows = c.execute(
                "SELECT id, label, type, address, port, username, extra "
                "FROM connections WHERE system_id = ? ORDER BY sort_order, id",
                (self._current_system_id,),
            ).fetchall()
        self._conn_table.setRowCount(len(rows))
        type_labels = {"rdp": "RDP", "ssh": "SSH", "browser": "浏览器", "custom": "自定义"}
        for i, row in enumerate(rows):
            self._conn_table.setItem(i, 0, QtWidgets.QTableWidgetItem(row["label"] or ""))
            self._conn_table.setItem(i, 1, QtWidgets.QTableWidgetItem(type_labels.get(row["type"], row["type"])))
            self._conn_table.setItem(i, 2, QtWidgets.QTableWidgetItem(row["address"] or ""))
            self._conn_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(row["port"]) if row["port"] else ""))
            self._conn_table.setItem(i, 4, QtWidgets.QTableWidgetItem(row["username"] or ""))
            self._conn_table.setItem(i, 5, QtWidgets.QTableWidgetItem(row["extra"] or ""))
            # Store ID in first column item
            self._conn_table.item(i, 0).setData(QtCore.Qt.UserRole, row["id"])
        self._conn_table.resizeColumnsToContents()

    def _selected_conn_id(self) -> int | None:
        row = self._conn_table.currentRow()
        if row < 0:
            return None
        item = self._conn_table.item(row, 0)
        return item.data(QtCore.Qt.UserRole) if item else None

    def _add_connection(self) -> None:
        if self._current_system_id is None:
            QtWidgets.QMessageBox.information(self, "提示", "请先在左侧选择一个系统")
            return
        dlg = ConnectionDialog(self)
        if dlg.exec() != QtWidgets.QDialog.Accepted:
            return
        d = dlg.get_data()
        pw_enc = encrypt(d["password"], self.key) if d["password"] else ""
        with get_conn() as c:
            c.execute(
                "INSERT INTO connections(system_id, label, type, address, port, username, password_enc, extra) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (
                    self._current_system_id,
                    d["label"],
                    d["type"],
                    d["address"],
                    d["port"],
                    d["username"],
                    pw_enc,
                    d["extra"],
                ),
            )
        self._refresh_connections()

    def _edit_connection(self) -> None:
        conn_id = self._selected_conn_id()
        if conn_id is None:
            return
        with get_conn() as c:
            row = c.execute(
                "SELECT label, type, address, port, username, password_enc, extra "
                "FROM connections WHERE id = ?",
                (conn_id,),
            ).fetchone()
        if row is None:
            return
        data = {
            "label": row["label"],
            "type": row["type"],
            "address": row["address"],
            "port": row["port"],
            "username": row["username"],
            "password": decrypt(row["password_enc"], self.key) if row["password_enc"] else "",
            "extra": row["extra"],
        }
        dlg = ConnectionDialog(self, data=data)
        if dlg.exec() != QtWidgets.QDialog.Accepted:
            return
        d = dlg.get_data()
        pw_enc = encrypt(d["password"], self.key) if d["password"] else ""
        with get_conn() as c:
            c.execute(
                "UPDATE connections SET label=?, type=?, address=?, port=?, username=?, password_enc=?, extra=? "
                "WHERE id=?",
                (d["label"], d["type"], d["address"], d["port"], d["username"], pw_enc, d["extra"], conn_id),
            )
        self._refresh_connections()

    def _delete_connection(self) -> None:
        conn_id = self._selected_conn_id()
        if conn_id is None:
            return
        if (
            QtWidgets.QMessageBox.question(self, "确认", "删除该连接条目？")
            != QtWidgets.QMessageBox.Yes
        ):
            return
        with get_conn() as c:
            c.execute("DELETE FROM connections WHERE id = ?", (conn_id,))
        self._refresh_connections()

    def _launch_connection(self) -> None:
        conn_id = self._selected_conn_id()
        if conn_id is None:
            QtWidgets.QMessageBox.information(self, "提示", "请先选择一个连接条目")
            return
        with get_conn() as c:
            row = c.execute(
                "SELECT type, address, port, username, password_enc FROM connections WHERE id = ?",
                (conn_id,),
            ).fetchone()
        if row is None:
            return
        conn_type = row["type"]
        address = row["address"] or ""
        port = row["port"] or 0
        username = row["username"] or ""
        password = decrypt(row["password_enc"], self.key) if row["password_enc"] else ""

        try:
            if conn_type == "rdp":
                launch_rdp(address, username, password)
            elif conn_type == "ssh":
                launch_ssh(address, port or 22, username)
            elif conn_type == "browser":
                launch_browser(address)
            elif conn_type == "custom":
                launch_custom(address)
            else:
                QtWidgets.QMessageBox.warning(self, "错误", f"未知连接类型: {conn_type}")
                return
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "启动失败", str(e))

    # ==================================================================
    # Update Methods CRUD
    # ==================================================================

    def _refresh_methods(self) -> None:
        self._method_table.setRowCount(0)
        if self._current_system_id is None:
            return
        with get_conn() as c:
            rows = c.execute(
                "SELECT id, name, kind, payload, notes FROM update_methods WHERE system_id = ? ORDER BY id",
                (self._current_system_id,),
            ).fetchall()
        kind_labels = {"ssh_command": "SSH 命令", "sftp_push": "SFTP", "manual_rdp": "手工 RDP", "custom": "自定义"}
        self._method_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self._method_table.setItem(i, 0, QtWidgets.QTableWidgetItem(row["name"]))
            self._method_table.setItem(i, 1, QtWidgets.QTableWidgetItem(kind_labels.get(row["kind"], row["kind"])))
            self._method_table.setItem(i, 2, QtWidgets.QTableWidgetItem(row["payload"] or ""))
            self._method_table.setItem(i, 3, QtWidgets.QTableWidgetItem(row["notes"] or ""))
            self._method_table.item(i, 0).setData(QtCore.Qt.UserRole, row["id"])
        self._method_table.resizeColumnsToContents()

    def _selected_method_id(self) -> int | None:
        row = self._method_table.currentRow()
        if row < 0:
            return None
        item = self._method_table.item(row, 0)
        return item.data(QtCore.Qt.UserRole) if item else None

    def _add_method(self) -> None:
        if self._current_system_id is None:
            QtWidgets.QMessageBox.information(self, "提示", "请先在左侧选择一个系统")
            return
        dlg = MethodDialog(self)
        if dlg.exec() != QtWidgets.QDialog.Accepted:
            return
        d = dlg.get_data()
        with get_conn() as c:
            c.execute(
                "INSERT INTO update_methods(system_id, name, kind, payload, notes) VALUES(?,?,?,?,?)",
                (self._current_system_id, d["name"], d["kind"], d["payload"], d["notes"]),
            )
        self._refresh_methods()

    def _edit_method(self) -> None:
        mid = self._selected_method_id()
        if mid is None:
            return
        with get_conn() as c:
            row = c.execute(
                "SELECT name, kind, payload, notes FROM update_methods WHERE id = ?", (mid,)
            ).fetchone()
        if row is None:
            return
        dlg = MethodDialog(self, data=dict(row))
        if dlg.exec() != QtWidgets.QDialog.Accepted:
            return
        d = dlg.get_data()
        with get_conn() as c:
            c.execute(
                "UPDATE update_methods SET name=?, kind=?, payload=?, notes=? WHERE id=?",
                (d["name"], d["kind"], d["payload"], d["notes"], mid),
            )
        self._refresh_methods()

    def _delete_method(self) -> None:
        mid = self._selected_method_id()
        if mid is None:
            return
        if (
            QtWidgets.QMessageBox.question(self, "确认", "删除该更新方式？")
            != QtWidgets.QMessageBox.Yes
        ):
            return
        with get_conn() as c:
            c.execute("DELETE FROM update_methods WHERE id = ?", (mid,))
        self._refresh_methods()

    def _execute_method(self) -> None:
        """Execute the selected update method and optionally log to ledger."""
        mid = self._selected_method_id()
        if mid is None:
            QtWidgets.QMessageBox.information(self, "提示", "请先选择一个更新方式")
            return
        with get_conn() as c:
            row = c.execute(
                "SELECT name, kind, payload, notes FROM update_methods WHERE id = ?", (mid,)
            ).fetchone()
        if row is None:
            return

        kind = row["kind"]
        payload = row["payload"] or ""
        method_name = row["name"]

        try:
            if kind == "ssh_command":
                # Need an SSH connection for this system to get host/port/user
                self._exec_ssh_method(payload)
            elif kind == "sftp_push":
                # SFTP: open terminal with scp/sftp command
                self._exec_sftp_method(payload)
            elif kind == "manual_rdp":
                # Just open RDP for the first RDP connection of this system
                self._exec_manual_rdp_method()
            elif kind == "custom":
                launch_custom(payload)
            else:
                QtWidgets.QMessageBox.warning(self, "错误", f"未知更新方式类型: {kind}")
                return
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "执行失败", str(e))
            return

        # Prompt user to record this update in the ledger
        reply = QtWidgets.QMessageBox.question(
            self,
            "记录更新",
            f"已触发「{method_name}」。\n是否立即记录到更新历史台账？",
        )
        if reply == QtWidgets.QMessageBox.Yes:
            with get_conn() as c:
                methods = [
                    (r["id"], r["name"])
                    for r in c.execute(
                        "SELECT id, name FROM update_methods WHERE system_id = ?",
                        (self._current_system_id,),
                    ).fetchall()
                ]
            dlg = RecordDialog(self, methods=methods)
            # Pre-select the method we just executed
            for i in range(dlg._method_combo.count()):
                if dlg._method_combo.itemData(i) == mid:
                    dlg._method_combo.setCurrentIndex(i)
                    break
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                d = dlg.get_data()
                with get_conn() as c:
                    c.execute(
                        "INSERT INTO update_records(system_id, method_id, version, operator, status, notes) "
                        "VALUES(?,?,?,?,?,?)",
                        (
                            self._current_system_id,
                            d["method_id"],
                            d["version"],
                            d["operator"],
                            d["status"],
                            d["notes"],
                        ),
                    )
                self._refresh_records()

    def _exec_ssh_method(self, payload: str) -> None:
        """Execute an SSH command method using the first SSH connection of the system."""
        # Parse payload: can be plain command or JSON {"cmd": "..."}
        cmd = payload.strip()
        if cmd.startswith("{"):
            try:
                data = json.loads(cmd)
                cmd = data.get("cmd", cmd)
            except (json.JSONDecodeError, TypeError):
                pass

        # Find SSH connection for this system
        with get_conn() as c:
            conn_row = c.execute(
                "SELECT address, port, username, password_enc FROM connections "
                "WHERE system_id = ? AND type = 'ssh' ORDER BY sort_order, id LIMIT 1",
                (self._current_system_id,),
            ).fetchone()
        if conn_row is None:
            raise RuntimeError(
                "该系统没有配置 SSH 连接条目，请先在「连接条目」中添加一个 SSH 类型的连接。"
            )
        address = conn_row["address"] or ""
        port = conn_row["port"] or 22
        username = conn_row["username"] or ""
        launch_ssh_command(address, port, username, cmd)

    def _exec_sftp_method(self, payload: str) -> None:
        """Execute an SFTP push method — opens terminal with sftp/scp command."""
        # Parse payload: JSON {"local": "...", "remote": "..."} or plain sftp command
        local_path = ""
        remote_path = ""
        if payload.strip().startswith("{"):
            try:
                data = json.loads(payload)
                local_path = data.get("local", "")
                remote_path = data.get("remote", "")
            except (json.JSONDecodeError, TypeError):
                pass

        # Find SSH connection
        with get_conn() as c:
            conn_row = c.execute(
                "SELECT address, port, username FROM connections "
                "WHERE system_id = ? AND type = 'ssh' ORDER BY sort_order, id LIMIT 1",
                (self._current_system_id,),
            ).fetchone()
        if conn_row is None:
            raise RuntimeError("该系统没有配置 SSH 连接条目，无法进行 SFTP 推送。")

        address = conn_row["address"] or ""
        port = conn_row["port"] or 22
        username = conn_row["username"] or ""
        target = f"{username}@{address}" if username else address

        if local_path and remote_path:
            cmd = f'scp -P {port} "{local_path}" {target}:"{remote_path}"'
        else:
            # Fallback: just open an sftp session
            cmd = f"sftp -P {port} {target}"

        from ..launcher import _open_in_terminal
        _open_in_terminal(cmd, keep_open=True)

    def _exec_manual_rdp_method(self) -> None:
        """Open the first RDP connection of this system."""
        with get_conn() as c:
            conn_row = c.execute(
                "SELECT address, username, password_enc FROM connections "
                "WHERE system_id = ? AND type = 'rdp' ORDER BY sort_order, id LIMIT 1",
                (self._current_system_id,),
            ).fetchone()
        if conn_row is None:
            raise RuntimeError("该系统没有配置 RDP 连接条目。")
        address = conn_row["address"] or ""
        username = conn_row["username"] or ""
        password = decrypt(conn_row["password_enc"], self.key) if conn_row["password_enc"] else ""
        launch_rdp(address, username, password)

    # ==================================================================
    # Update Records (台账)
    # ==================================================================

    def _refresh_records(self) -> None:
        self._record_table.setRowCount(0)
        if self._current_system_id is None:
            return
        with get_conn() as c:
            rows = c.execute(
                "SELECT r.created_at, r.version, r.operator, r.status, r.notes, "
                "       m.name AS method_name "
                "FROM update_records r "
                "LEFT JOIN update_methods m ON m.id = r.method_id "
                "WHERE r.system_id = ? ORDER BY r.created_at DESC",
                (self._current_system_id,),
            ).fetchall()
        self._record_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self._record_table.setItem(i, 0, QtWidgets.QTableWidgetItem(row["created_at"] or ""))
            self._record_table.setItem(i, 1, QtWidgets.QTableWidgetItem(row["version"] or ""))
            self._record_table.setItem(i, 2, QtWidgets.QTableWidgetItem(row["operator"] or ""))
            self._record_table.setItem(i, 3, QtWidgets.QTableWidgetItem(row["status"] or ""))
            self._record_table.setItem(i, 4, QtWidgets.QTableWidgetItem(row["method_name"] or ""))
            self._record_table.setItem(i, 5, QtWidgets.QTableWidgetItem(row["notes"] or ""))
        self._record_table.resizeColumnsToContents()

    def _add_record(self) -> None:
        if self._current_system_id is None:
            QtWidgets.QMessageBox.information(self, "提示", "请先在左侧选择一个系统")
            return
        # Get available methods for this system
        with get_conn() as c:
            methods = [
                (row["id"], row["name"])
                for row in c.execute(
                    "SELECT id, name FROM update_methods WHERE system_id = ?",
                    (self._current_system_id,),
                ).fetchall()
            ]
        dlg = RecordDialog(self, methods=methods)
        if dlg.exec() != QtWidgets.QDialog.Accepted:
            return
        d = dlg.get_data()
        with get_conn() as c:
            c.execute(
                "INSERT INTO update_records(system_id, method_id, version, operator, status, notes) "
                "VALUES(?,?,?,?,?,?)",
                (
                    self._current_system_id,
                    d["method_id"],
                    d["version"],
                    d["operator"],
                    d["status"],
                    d["notes"],
                ),
            )
        self._refresh_records()

    # ==================================================================
    # Excel Import
    # ==================================================================

    def _import_excel(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择 Excel 文件", "", "Excel Files (*.xlsx *.xls)"
        )
        if not path:
            return
        try:
            from openpyxl import load_workbook

            wb = load_workbook(path, read_only=True, data_only=True)
            ws = wb.active
            rows = list(ws.iter_rows(min_row=2, values_only=True))
            wb.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "导入失败", f"读取文件出错：{e}")
            return

        imported = 0
        with get_conn() as c:
            for row in rows:
                if not row or not row[0]:
                    continue
                # Expected columns: A=系统, B=远程地址, C=浏览器运维地址,
                # D=运维账号, E=运维密码, F=远程账号, G=远程密码, H=系统账号, I=系统密码
                system_name = str(row[0]).strip() if row[0] else ""
                if not system_name:
                    continue

                # Find or create system
                existing = c.execute(
                    "SELECT id FROM systems WHERE name = ?", (system_name,)
                ).fetchone()
                if existing:
                    sys_id = existing["id"]
                else:
                    c.execute("INSERT INTO systems(name) VALUES(?)", (system_name,))
                    sys_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]

                remote_addr = str(row[1]).strip() if len(row) > 1 and row[1] else ""
                browser_addr = str(row[2]).strip() if len(row) > 2 and row[2] else ""
                ops_user = str(row[3]).strip() if len(row) > 3 and row[3] else ""
                ops_pass = str(row[4]).strip() if len(row) > 4 and row[4] else ""
                remote_user = str(row[5]).strip() if len(row) > 5 and row[5] else ""
                remote_pass = str(row[6]).strip() if len(row) > 6 and row[6] else ""
                sys_user = str(row[7]).strip() if len(row) > 7 and row[7] else ""
                sys_pass = str(row[8]).strip() if len(row) > 8 and row[8] else ""

                # Add RDP connection if remote address exists
                if remote_addr:
                    c.execute(
                        "INSERT INTO connections(system_id, label, type, address, username, password_enc) "
                        "VALUES(?,?,?,?,?,?)",
                        (
                            sys_id,
                            "远程桌面",
                            "rdp",
                            remote_addr,
                            remote_user,
                            encrypt(remote_pass, self.key) if remote_pass else "",
                        ),
                    )

                # Add browser connection if URL exists
                if browser_addr:
                    c.execute(
                        "INSERT INTO connections(system_id, label, type, address, username, password_enc) "
                        "VALUES(?,?,?,?,?,?)",
                        (
                            sys_id,
                            "运维地址",
                            "browser",
                            browser_addr,
                            ops_user,
                            encrypt(ops_pass, self.key) if ops_pass else "",
                        ),
                    )

                # Add system account as an SSH connection if system user exists
                if sys_user:
                    c.execute(
                        "INSERT INTO connections(system_id, label, type, address, username, password_enc) "
                        "VALUES(?,?,?,?,?,?)",
                        (
                            sys_id,
                            "系统账号",
                            "ssh",
                            remote_addr,
                            sys_user,
                            encrypt(sys_pass, self.key) if sys_pass else "",
                        ),
                    )

                imported += 1

        self._refresh_systems()
        QtWidgets.QMessageBox.information(
            self, "导入完成", f"成功处理 {imported} 行数据。"
        )

    # ==================================================================
    # Lock
    # ==================================================================

    def _lock(self) -> None:
        """Clear key from memory and close — user must re-enter password."""
        self.key = b"\x00" * 32  # overwrite
        self.close()
