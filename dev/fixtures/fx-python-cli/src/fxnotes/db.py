"""SQLite wrapper for fxnotes.

The `connect`/`close` pair gives a context-managed connection. `execute`
retries on OperationalError (database is locked) up to 3 times with a
short backoff; after that the call raises DatabaseError.

The `add_note` path contains a race-condition trap: two concurrent
inserts with the same key both pass the existence check, but only one
wins at the UNIQUE constraint. The loser sees an IntegrityError that is
mapped to DatabaseError("duplicate key").
"""
from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

from . import DatabaseError


LOCK_RETRIES = 3
LOCK_BACKOFF_S = 0.01


class Database:
    def __init__(self, path: str):
        self.path = path
        self.conn: sqlite3.Connection | None = None

    def connect(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, timeout=5.0, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "  key TEXT PRIMARY KEY, value TEXT NOT NULL, "
            "  tag TEXT, created_at REAL NOT NULL, deleted INTEGER NOT NULL DEFAULT 0)"
        )

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    @contextmanager
    def cursor(self):
        assert self.conn is not None, "database not connected"
        cur = self.conn.cursor()
        try:
            yield cur
        finally:
            cur.close()

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        last_exc: sqlite3.OperationalError | None = None
        for attempt in range(LOCK_RETRIES):
            try:
                return self.conn.execute(sql, params)
            except sqlite3.OperationalError as exc:
                last_exc = exc
                if "locked" not in str(exc).lower():
                    raise DatabaseError(str(exc)) from exc
                time.sleep(LOCK_BACKOFF_S * (attempt + 1))
        raise DatabaseError(f"database locked after {LOCK_RETRIES} retries: {last_exc}")