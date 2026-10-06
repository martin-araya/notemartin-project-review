"""Subcomando `npr init`."""
from __future__ import annotations

import sys
from pathlib import Path

from .. import workspace, config as cfg


COMMAND = "init"


def add_parser(sub):
    p = sub.add_parser(COMMAND, help="Inicializa el workspace .project-review/ en un repo")
    p.add_argument("repo", nargs="?", default=None, help="Ruta al repo a analizar")
    p.add_argument("--out", default=None, help="Carpeta del workspace (default: <repo>/.project-review)")
    p.add_argument("--force", action="store_true", help="Reescribir aunque el workspace exista")
    return p


def handle(args, ctx) -> int:
    skill_dir, workspace_dir, effective, origin, logger = ctx

    repo = Path(args.repo).expanduser().resolve() if args.repo else Path.cwd()
    out = Path(args.out).expanduser().resolve() if args.out else None

    ws = workspace.init(repo=repo, out=out, force=args.force, lang=effective.get("lang", "es"), skill_dir=skill_dir)
    cfg.write_to_state(ws, effective)

    logger.info("workspace inicializado repo=%s workspace=%s", repo, ws)
    if effective.get("lang", "es") != "es":
        print(f"workspace inicializado en {ws}", file=sys.stdout)
    else:
        print(f"workspace inicializado en {ws}")
    return 0