"""SQLite schema and connection helpers."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager

from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS systems (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    notes       TEXT,
    created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
);

-- A connection entry under a system. Examples:
--   type='rdp'      -> 远程桌面
--   type='ssh'      -> SSH 服务器
--   type='browser'  -> 浏览器运维地址
--   type='custom'   -> 自定义命令（如 iNode 客户端）
CREATE TABLE IF NOT EXISTS connections (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id     INTEGER NOT NULL,
    label         TEXT,
    type          TEXT    NOT NULL,
    address       TEXT,
    port          INTEGER,
    username      TEXT,
    password_enc  TEXT,
    extra         TEXT,            -- JSON blob for additional fields
    sort_order    INTEGER DEFAULT 0,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
);

-- An update method tied to a system (场景 a).
--   kind='ssh_command' / 'sftp_push' / 'manual_rdp' / 'custom'
CREATE TABLE IF NOT EXISTS update_methods (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id   INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    kind        TEXT    NOT NULL,
    payload     TEXT,            -- JSON: command/script/target paths
    notes       TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
);

-- Update history ledger (场景 b).
CREATE TABLE IF NOT EXISTS update_records (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id   INTEGER NOT NULL,
    method_id   INTEGER,
    version     TEXT,
    operator    TEXT,
    status      TEXT,            -- 'success' / 'failed' / 'rolled_back' / ...
    notes       TEXT,
    created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE,
    FOREIGN KEY (method_id) REFERENCES update_methods(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_connections_system    ON connections(system_id);
CREATE INDEX IF NOT EXISTS idx_methods_system        ON update_methods(system_id);
CREATE INDEX IF NOT EXISTS idx_records_system        ON update_records(system_id);
CREATE INDEX IF NOT EXISTS idx_records_created_at    ON update_records(created_at);
"""


def _open() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def get_conn():
    conn = _open()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_schema() -> None:
    with get_conn() as c:
        c.executescript(SCHEMA)
