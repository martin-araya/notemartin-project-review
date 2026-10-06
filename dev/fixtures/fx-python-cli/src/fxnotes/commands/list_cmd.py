"""fxnotes list command.

Trampa plantada: catch vacio que convierte DB error en exito silencioso.
Cuando la BD falla por alguna razon (locked persistente, archivo no
legible, etc.), la excepcion se traga y se imprime "0 entries" como si
la BD estuviera vacia. Esto oculta errores al usuario.

Tambien expone dos filtros opcionales (--tag, --sort-by).
"""
from __future__ import annotations

import argparse

from .. import FXNotesError
from ..events import emit


def add_parser(sub):
    p = sub.add_parser("list", help="List notes")
    p.add_argument("--tag", default=None)
    p.add_argument("--sort-by", default=None, choices=["created_at", "key", "tag"])
    p.add_argument("--include-deleted", action="store_true")
    return p


def run(args, ctx) -> int:
    cfg = ctx["config"]
    db = ctx["db"]

    sql = "SELECT key, value, tag, created_at, deleted FROM notes"
    params: list = []
    where = []
    if not args.include_deleted:
        where.append("deleted = 0")
    if args.tag:
        where.append("tag = ?")
        params.append(args.tag)
    if where:
        sql += " WHERE " + " AND ".join(where)
    sort_key = args.sort_by or cfg["list_default_sort"]
    sql += f" ORDER BY {sort_key} ASC"

    try:
        with db.cursor() as cur:
            rows = cur.execute(sql, tuple(params)).fetchall()
    except FXNotesError:
        rows = []

    if not rows:
        print("0 entries.")
        return 0

    emit("note_listed", count=len(rows))
    for row in rows:
        marker = " (deleted)" if row["deleted"] else ""
        print(f"{row['key']}\t{row['tag'] or '-'}\t{row['value'][:60]}{marker}")
    return 0