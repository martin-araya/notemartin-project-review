"""Subcomando `npr config`."""
from __future__ import annotations

import json
import sys

from .. import errors_catalog


COMMAND = "config"


def add_parser(sub):
    p = sub.add_parser(COMMAND, help="Gestiona la configuracion efectiva")
    sub_p = p.add_subparsers(dest="config_action", required=True, metavar="ACTION")
    show = sub_p.add_parser("show", help="Muestra la configuracion efectiva y el origen de cada valor")
    show.add_argument("--json", dest="as_json", action="store_true", help="Salida en JSON")
    return p


def handle(args, ctx) -> int:
    skill_dir, workspace_dir, effective, origin, logger = ctx
    if args.config_action == "show":
        return _show(args, effective, origin)
    print(errors_catalog.format_error("NPR-E102", action=args.config_action), file=sys.stderr)
    return 1


def _show(args, effective, origin) -> int:
    rows = sorted(effective.items(), key=lambda kv: kv[0])
    if getattr(args, "as_json", False):
        payload = {
            "config": effective,
            "origin": origin,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    print("# Configuracion efectiva de npr")
    name_w = max(len(k) for k in effective)
    origin_w = max(len(origin.get(k, "")) for k in effective)
    for k, v in rows:
        print(f"{k:<{name_w}}  {origin.get(k, '?'):<{origin_w}}  {v}")
    return 0