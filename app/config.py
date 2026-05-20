"""Paths and constants for the application."""
from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "UpdateTools"


def _app_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    d = base / APP_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


APP_DIR: Path = _app_dir()
DB_PATH: Path = APP_DIR / "data.db"
META_PATH: Path = APP_DIR / "meta.json"
