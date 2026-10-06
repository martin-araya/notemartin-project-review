"""fxnotes add command.

Trampas plantadas en este feature:
- DB lock con 3 reintentos y backoff (db.execute).
- Condicion de carrera: dos inserts con la misma key; UNIQUE hace que
  solo uno gane; el otro lanza DatabaseError("duplicate key").
"""
from __future__ import annotations

import argparse
import sqlite3
import time

from .. import ValidationError, DatabaseError, FXNotesError
from ..events import emit


def add_parser(sub):
    p = sub.add_parser("add", help="Add a note")
    p.add_argument("key")
    p.add_argument("value")
    p.add_argument("--tag", default=None)
    return p


def run(args, ctx) -> int:
    cfg = ctx["config"]
    db = ctx["db"]

    key = args.key.strip()
    if not key:
        raise ValidationError("key cannot be empty")
    if len(key) > cfg["max_key_len"]:
        raise ValidationError(f"key exceeds {cfg['max_key_len']} characters")
    value = args.value
    if len(value) > cfg["max_value_len"]:
        raise ValidationError(f"value exceeds {cfg['max_value_len']} characters")

    try:
        with db.cursor() as cur:
            cur.execute("SELECT 1 FROM notes WHERE key = ?", (key,))
            if cur.fetchone() is not None:
                raise DatabaseError(f"duplicate key: {key!r}")
            db.execute(
                "INSERT INTO notes(key, value, tag, created_at, deleted) VALUES (?, ?, ?, ?, 0)",
                (key, value, args.tag, time.time()),
            )
    except DatabaseError:
        raise
    except sqlite3.IntegrityError as exc:
        raise DatabaseError(f"duplicate key {key!r} (lost race)") from exc

    emit("note_added", key=key)
    print(f"Note '{key}' added.")
    return 0