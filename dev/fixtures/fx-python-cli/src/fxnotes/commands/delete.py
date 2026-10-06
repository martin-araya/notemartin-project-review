"""fxnotes delete command.

Trampas plantadas:
- Dead branch: --archived se acepta pero no hace nada (rama muerta).
- Resultado solo con combinacion: --no-undo + confirm=False -> "deleted
  permanently".
- Resultado solo cuando el usuario rechaza una aprobacion: si
  confirm=ask y el usuario responde "no", resultado "cancelled by user".
"""
from __future__ import annotations

import argparse
import sys

from .. import NotFoundError, CancelledError, ValidationError
from ..events import emit


def add_parser(sub):
    p = sub.add_parser("delete", help="Delete a note")
    p.add_argument("key")
    p.add_argument("--no-undo", action="store_true",
                   help="Hard-delete: bypass soft delete")
    p.add_argument("--archived", action="store_true",
                   help="Deprecated; does nothing")
    p.add_argument("--yes", action="store_true",
                   help="Skip confirmation (confirm=False)")
    return p


def _ask_user(key: str) -> bool:
    """Ask the user interactively. Returns True if confirmed."""
    sys.stdout.write(f"Delete '{key}'? [y/N]: ")
    sys.stdout.flush()
    try:
        answer = input().strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes")


def run(args, ctx) -> int:
    cfg = ctx["config"]
    db = ctx["db"]

    key = args.key.strip()
    if not key:
        raise ValidationError("key cannot be empty")

    if args.archived:
        print(f"--archived is deprecated; '{key}' was not deleted.")
        return 0

    with db.cursor() as cur:
        cur.execute("SELECT deleted FROM notes WHERE key = ?", (key,))
        row = cur.fetchone()
        if row is None:
            raise NotFoundError(f"key not found: {key!r}")

    confirm_mode = cfg["confirm"]
    if confirm_mode == "ask" and not args.yes:
        if not _ask_user(key):
            raise CancelledError(f"delete of {key!r} cancelled by user")

    permanent = (confirm_mode is False) or args.no_undo or args.yes

    if permanent:
        db.execute("DELETE FROM notes WHERE key = ?", (key,))
        emit("note_deleted", key=key, soft=False)
        print(f"Note '{key}' deleted permanently.")
        return 0

    db.execute("UPDATE notes SET deleted = 1 WHERE key = ?", (key,))
    emit("note_deleted", key=key, soft=True)
    print(f"Note '{key}' deleted (soft; recoverable within 30 days).")
    return 0