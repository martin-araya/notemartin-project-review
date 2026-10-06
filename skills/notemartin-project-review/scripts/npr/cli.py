"""CLI principal de `npr`.

Construye argparse, resuelve SKILL_DIR, carga configuracion efectiva,
dispatch al handler del subcomando. Errores NPR-Exxx se formatean
desde `errors_catalog`.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import errors_catalog, paths, config as cfg, logging_setup
from .subcommands import register as register_subcommands


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="npr",
        description="notemartin-project-review CLI: analisis exhaustivo de repos",
    )
    p.add_argument("--skill-dir", default=None, help="Ruta absoluta a la skill (sobrescribe deteccion)")
    p.add_argument("--repo", default=None, help="Repo a analizar")
    p.add_argument("--out", default=None, help="Carpeta del workspace (default: <repo>/.project-review)")
    p.add_argument("--json", dest="as_json", action="store_true", help="Salida JSON cuando aplique")
    p.add_argument("--verbose", "-v", action="store_true", help="Logging DEBUG")
    p.add_argument("--lang", default=None, choices=["es", "en"], help="Idioma de reportes")
    p.add_argument("--config", default=None, help="Archivo de configuracion adicional")
    p.add_argument("--set", action="append", default=[], help="Override inline: --set clave=valor")
    sub = p.add_subparsers(dest="command", required=True, metavar="COMMAND")
    register_subcommands(sub)
    return p


def _resolve_workspace(args, skill_dir: Path, effective: dict) -> Path | None:
    if args.command in {"init"}:
        return None
    ws_dir_name = effective.get("workspace.dir", ".project-review")
    repo = Path(args.repo).expanduser().resolve() if args.repo else Path.cwd()
    workspace = repo / ws_dir_name
    return workspace.resolve() if workspace.is_dir() else None


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    skill_dir = paths.resolve_skill_dir(args.skill_dir)
    os.environ["NPR_HOME"] = str(skill_dir)

    try:
        workspace = _resolve_workspace(args, skill_dir, {"workspace.dir": ".project-review"})
    except Exception:
        workspace = None

    logger = logging_setup.setup(workspace)
    if args.verbose:
        logging.getLogger("npr").setLevel(logging.DEBUG)

    try:
        effective, origin = cfg.load_effective(
            skill_dir, workspace, args.config, args.set,
        )
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 1

    ctx = (skill_dir, workspace, effective, origin, logger)

    from .subcommands import init_cmd, config_cmd, status_cmd, resume_cmd, stubs

    handler_map = {
        "init": init_cmd,
        "config": config_cmd,
        "status": status_cmd,
        "resume": resume_cmd,
    }
    for name, _ in stubs.STUB_COMMANDS:
        handler_map[name] = stubs

    handler = handler_map.get(args.command)
    if handler is None:
        print(errors_catalog.format_error("NPR-E102", command=args.command), file=sys.stderr)
        return 1

    try:
        return handler.handle(args, ctx)
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 1


if __name__ == "__main__":
    raise SystemExit(main())