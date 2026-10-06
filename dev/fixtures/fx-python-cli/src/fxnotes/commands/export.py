"""fxnotes export command."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from .. import FXNotesError


def add_parser(sub):
    p = sub.add_parser("export", help="Export notes")
    p.add_argument("path", help="Output file path (- for stdout)")
    p.add_argument("--format", choices=["json", "csv"], default="json")
    p.add_argument("--include-deleted", action="store_true")
    return p


def run(args, ctx) -> int:
    db = ctx["db"]

    sql = "SELECT key, value, tag, created_at, deleted FROM notes"
    if not args.include_deleted:
        sql += " WHERE deleted = 0"
    sql += " ORDER BY created_at ASC"

    try:
        with db.cursor() as cur:
            rows = cur.execute(sql).fetchall()
    except FXNotesError as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1

    payload = [dict(r) for r in rows]

    if args.format == "csv":
        _write_csv(payload, args.path)
    else:
        text = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.path == "-":
            print(text)
        else:
            Path(args.path).write_text(text, encoding="utf-8")

    print(f"Exported {len(payload)} notes.", file=sys.stderr)
    return 0


def _write_csv(payload: list, path: str) -> None:
    if not payload:
        if path == "-":
            return
        Path(path).write_text("", encoding="utf-8")
        return

    fieldnames = list(payload[0].keys())
    if path == "-":
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for row in payload:
            writer.writerow(row)
    else:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for row in payload:
                writer.writerow(row)