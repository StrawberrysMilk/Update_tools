"""Application-wide QSS stylesheet for a modern, clean look."""

STYLESHEET = """
/* ======== Global ======== */
QMainWindow, QDialog {
    background-color: #f5f7fa;
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    font-size: 13px;
}

/* ======== Toolbar ======== */
QToolBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4a90d9, stop:1 #357abd);
    border: none;
    padding: 4px 8px;
    spacing: 6px;
}
QToolBar QToolButton {
    color: white;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: bold;
}
QToolBar QToolButton:hover {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
QToolBar QToolButton:pressed {
    background: rgba(255, 255, 255, 0.25);
}
QToolBar::separator {
    width: 1px;
    background: rgba(255, 255, 255, 0.3);
    margin: 4px 8px;
}

/* ======== Splitter ======== */
QSplitter::handle {
    background: #dde3ea;
    width: 2px;
}
QSplitter::handle:hover {
    background: #4a90d9;
}

/* ======== Left list ======== */
QListWidget {
    background: #ffffff;
    border: none;
    border-right: 1px solid #e0e4e8;
    padding: 4px;
    outline: none;
}
QListWidget::item {
    padding: 10px 12px;
    border-radius: 6px;
    margin: 2px 4px;
    color: #333;
}
QListWidget::item:selected {
    background: #e8f0fe;
    color: #1a56db;
    font-weight: bold;
}
QListWidget::item:hover:!selected {
    background: #f0f4f8;
}

/* ======== Tabs ======== */
QTabWidget::pane {
    border: none;
    background: #ffffff;
    border-radius: 8px;
    margin-top: -1px;
}
QTabBar::tab {
    background: #eef1f5;
    border: none;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: #555;
    font-weight: 500;
}
QTabBar::tab:selected {
    background: #ffffff;
    color: #1a56db;
    font-weight: bold;
    border-bottom: 2px solid #4a90d9;
}
QTabBar::tab:hover:!selected {
    background: #dfe5ed;
}

/* ======== Tables ======== */
QTableWidget {
    background: #ffffff;
    border: 1px solid #e8ecf0;
    border-radius: 6px;
    gridline-color: #f0f2f5;
    selection-background-color: #e8f0fe;
    selection-color: #1a56db;
}
QTableWidget::item {
    padding: 6px 8px;
}
QHeaderView::section {
    background: #f8fafb;
    border: none;
    border-bottom: 2px solid #e0e4e8;
    padding: 8px 10px;
    font-weight: bold;
    color: #555;
}

/* ======== Buttons ======== */
QPushButton {
    background: #ffffff;
    border: 1px solid #d0d5dd;
    border-radius: 6px;
    padding: 7px 16px;
    color: #344054;
    font-weight: 500;
}
QPushButton:hover {
    background: #f9fafb;
    border-color: #4a90d9;
    color: #1a56db;
}
QPushButton:pressed {
    background: #e8f0fe;
}
QPushButton:disabled {
    background: #f5f5f5;
    color: #aaa;
    border-color: #e0e0e0;
}

/* ======== Input fields ======== */
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background: #ffffff;
    border: 1px solid #d0d5dd;
    border-radius: 6px;
    padding: 7px 10px;
    color: #333;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #4a90d9;
    outline: none;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

/* ======== Dialog ======== */
QDialog {
    background: #ffffff;
}
QLabel {
    color: #344054;
}

/* ======== MessageBox ======== */
QMessageBox {
    background: #ffffff;
}

/* ======== ScrollBar ======== */
QScrollBar:vertical {
    background: #f5f7fa;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #c0c8d4;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #9aa8b8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""
