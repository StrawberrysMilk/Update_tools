"""Global stylesheet and palette for UpdateTools.

Minimalist dark theme — warm charcoal tones, soft blue accent,
generous spacing, clean typography.
"""
from __future__ import annotations

from PySide6 import QtGui, QtWidgets

# ── Colour tokens ──────────────────────────────────────────────────────────
BG_BASE       = "#191919"   # deepest background
BG_SURFACE    = "#1e1e1e"   # cards / panels
BG_ELEVATED   = "#262626"   # toolbar / header / inputs
BG_HOVER      = "#2e2e2e"   # hover state
BORDER        = "#333333"   # subtle dividers
BORDER_LIGHT  = "#3a3a3a"   # slightly lighter border

ACCENT        = "#4e8cff"   # soft blue
ACCENT_HOVER  = "#6ba0ff"
ACCENT_DIM    = "#2a5db0"
ACCENT_BG     = "rgba(78,140,255,0.08)"  # very subtle accent wash

SUCCESS       = "#34c759"
WARNING       = "#f5a623"
DANGER        = "#ff453a"
INFO          = "#5ac8fa"

TEXT_PRIMARY   = "#e8e8e8"
TEXT_SECONDARY = "#8e8e93"
TEXT_DISABLED  = "#48484a"

RADIUS    = "10px"
RADIUS_SM = "6px"
RADIUS_LG = "14px"

QSS = f"""
/* ── Global ─────────────────────────────────────────────────────────── */
QWidget {{
    background-color: {BG_BASE};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", "Microsoft YaHei UI", sans-serif;
    font-size: 13px;
}}

QMainWindow, QDialog {{
    background-color: {BG_BASE};
}}

/* ── Scrollbars ──────────────────────────────────────────────────────── */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 40px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_SECONDARY};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 6px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER};
    border-radius: 3px;
    min-width: 40px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {TEXT_SECONDARY};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: transparent;
}}

/* ── Toolbar ─────────────────────────────────────────────────────────── */
QToolBar {{
    background-color: {BG_SURFACE};
    border-bottom: 1px solid {BORDER};
    padding: 6px 12px;
    spacing: 4px;
}}
QToolBar QToolButton {{
    background: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    border-radius: {RADIUS_SM};
    padding: 7px 14px;
    font-size: 13px;
}}
QToolBar QToolButton:hover {{
    background-color: {BG_HOVER};
    color: {TEXT_PRIMARY};
}}
QToolBar QToolButton:pressed {{
    background-color: {ACCENT_DIM};
    color: #ffffff;
}}
QToolBar::separator {{
    background: {BORDER};
    width: 1px;
    margin: 6px 8px;
}}

/* ── Splitter ────────────────────────────────────────────────────────── */
QSplitter::handle {{
    background: {BORDER};
    width: 1px;
}}

/* ── List Widget (left panel) ────────────────────────────────────────── */
QListWidget {{
    background-color: {BG_SURFACE};
    border: none;
    border-right: 1px solid {BORDER};
    outline: none;
    padding: 8px 6px;
    font-size: 13px;
}}
QListWidget::item {{
    padding: 10px 14px;
    border-radius: {RADIUS_SM};
    color: {TEXT_SECONDARY};
    margin: 1px 0;
}}
QListWidget::item:hover {{
    background-color: {BG_HOVER};
    color: {TEXT_PRIMARY};
}}
QListWidget::item:selected {{
    background-color: {ACCENT_BG};
    color: {ACCENT_HOVER};
    border-left: 2px solid {ACCENT};
}}

/* ── Tab Widget ──────────────────────────────────────────────────────── */
QTabWidget::pane {{
    border: none;
    background: {BG_BASE};
}}
QTabBar {{
    background: {BG_SURFACE};
}}
QTabBar::tab {{
    background: transparent;
    color: {TEXT_DISABLED};
    padding: 10px 20px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
}}
QTabBar::tab:hover {{
    color: {TEXT_SECONDARY};
}}
QTabBar::tab:selected {{
    color: {TEXT_PRIMARY};
    border-bottom: 2px solid {ACCENT};
}}

/* ── Table Widget ────────────────────────────────────────────────────── */
QTableWidget {{
    background-color: {BG_SURFACE};
    alternate-background-color: {BG_ELEVATED};
    gridline-color: transparent;
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
    outline: none;
    selection-background-color: {ACCENT_BG};
    selection-color: {TEXT_PRIMARY};
}}
QTableWidget::item {{
    padding: 8px 12px;
    border: none;
}}
QTableWidget::item:hover {{
    background-color: {BG_HOVER};
}}
QHeaderView::section {{
    background-color: {BG_ELEVATED};
    color: {TEXT_SECONDARY};
    padding: 9px 12px;
    border: none;
    border-bottom: 1px solid {BORDER};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}}
QHeaderView::section:last {{
    border-right: none;
}}

/* ── Push Buttons ────────────────────────────────────────────────────── */
QPushButton {{
    background-color: {BG_ELEVATED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 7px 18px;
    font-size: 13px;
}}
QPushButton:hover {{
    background-color: {BG_HOVER};
    border-color: {BORDER_LIGHT};
}}
QPushButton:pressed {{
    background-color: {BORDER};
}}
QPushButton:disabled {{
    color: {TEXT_DISABLED};
    border-color: {BORDER};
}}

QPushButton#btn_primary {{
    background-color: {ACCENT};
    color: #ffffff;
    border: none;
    font-weight: 600;
}}
QPushButton#btn_primary:hover {{
    background-color: {ACCENT_HOVER};
}}
QPushButton#btn_primary:pressed {{
    background-color: {ACCENT_DIM};
}}

QPushButton#btn_danger {{
    background-color: transparent;
    color: {DANGER};
    border: 1px solid rgba(255,69,58,0.3);
}}
QPushButton#btn_danger:hover {{
    background-color: rgba(255,69,58,0.1);
    border-color: {DANGER};
}}

QPushButton#btn_success {{
    background-color: transparent;
    color: {SUCCESS};
    border: 1px solid rgba(52,199,89,0.3);
    font-weight: 600;
}}
QPushButton#btn_success:hover {{
    background-color: rgba(52,199,89,0.1);
    border-color: {SUCCESS};
}}

QPushButton#btn_ghost {{
    background: transparent;
    border: none;
    color: {TEXT_SECONDARY};
    padding: 7px 12px;
}}
QPushButton#btn_ghost:hover {{
    color: {TEXT_PRIMARY};
    background: {BG_HOVER};
}}

/* ── Line Edit / Spin Box / Combo Box ────────────────────────────────── */
QLineEdit, QSpinBox, QComboBox, QTextEdit, QPlainTextEdit {{
    background-color: {BG_ELEVATED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 7px 12px;
    selection-background-color: {ACCENT_DIM};
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus {{
    border-color: {ACCENT};
}}
QLineEdit::placeholder, QTextEdit::placeholder {{
    color: {TEXT_DISABLED};
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {TEXT_SECONDARY};
    width: 0;
    height: 0;
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {BG_ELEVATED};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    selection-background-color: {ACCENT_BG};
    selection-color: {TEXT_PRIMARY};
    outline: none;
    padding: 4px;
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background: transparent;
    border: none;
    width: 16px;
}}

/* ── CheckBox ────────────────────────────────────────────────────────── */
QCheckBox {{
    color: {TEXT_SECONDARY};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1.5px solid {BORDER_LIGHT};
    border-radius: 4px;
    background: {BG_ELEVATED};
}}
QCheckBox::indicator:checked {{
    background-color: {ACCENT};
    border-color: {ACCENT};
}}

/* ── Dialog Buttons ──────────────────────────────────────────────────── */
QDialogButtonBox QPushButton {{
    min-width: 80px;
}}

/* ── Message Box ─────────────────────────────────────────────────────── */
QMessageBox {{
    background-color: {BG_SURFACE};
}}
QMessageBox QLabel {{
    color: {TEXT_PRIMARY};
}}

/* ── Label ───────────────────────────────────────────────────────────── */
QLabel {{
    background: transparent;
    color: {TEXT_PRIMARY};
}}
QLabel#label_hint {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
}}
QLabel#label_title {{
    font-size: 20px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
}}
QLabel#label_subtitle {{
    font-size: 13px;
    color: {TEXT_SECONDARY};
}}

/* ── Status badge labels ─────────────────────────────────────────────── */
QLabel#badge_success {{
    background-color: rgba(52,199,89,0.12);
    color: {SUCCESS};
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 12px;
}}
QLabel#badge_failed {{
    background-color: rgba(255,69,58,0.12);
    color: {DANGER};
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 12px;
}}
QLabel#badge_warning {{
    background-color: rgba(245,166,35,0.12);
    color: {WARNING};
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 12px;
}}

/* ── Input Dialog ────────────────────────────────────────────────────── */
QInputDialog {{
    background-color: {BG_SURFACE};
}}

/* ── Tooltip ─────────────────────────────────────────────────────────── */
QToolTip {{
    background-color: {BG_ELEVATED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 5px 10px;
}}
"""


def apply(app: QtWidgets.QApplication) -> None:
    """Apply the minimalist dark theme to the whole application."""
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window,          QtGui.QColor(BG_BASE))
    palette.setColor(QtGui.QPalette.WindowText,      QtGui.QColor(TEXT_PRIMARY))
    palette.setColor(QtGui.QPalette.Base,            QtGui.QColor(BG_ELEVATED))
    palette.setColor(QtGui.QPalette.AlternateBase,   QtGui.QColor(BG_SURFACE))
    palette.setColor(QtGui.QPalette.ToolTipBase,     QtGui.QColor(BG_ELEVATED))
    palette.setColor(QtGui.QPalette.ToolTipText,     QtGui.QColor(TEXT_PRIMARY))
    palette.setColor(QtGui.QPalette.Text,            QtGui.QColor(TEXT_PRIMARY))
    palette.setColor(QtGui.QPalette.Button,          QtGui.QColor(BG_ELEVATED))
    palette.setColor(QtGui.QPalette.ButtonText,      QtGui.QColor(TEXT_PRIMARY))
    palette.setColor(QtGui.QPalette.Highlight,       QtGui.QColor(ACCENT_DIM))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#ffffff"))
    palette.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor(TEXT_DISABLED))
    app.setPalette(palette)
