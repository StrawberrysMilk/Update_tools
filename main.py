"""Application entry point.

    python main.py
"""
from __future__ import annotations

import sys

from PySide6 import QtWidgets

from app.db import init_schema
from app.ui.main_window import MainWindow
from app.ui.style import apply as apply_style
from app.ui.unlock import UnlockDialog


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    apply_style(app)
    init_schema()

    unlock = UnlockDialog()
    if unlock.exec() != QtWidgets.QDialog.Accepted or unlock.key is None:
        return 0

    win = MainWindow(unlock.key)
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
