"""fxnotes CLI: argparse + dispatch by string."""
from __future__ import annotations

import argparse
import sys
from typing import Callable

from . import __version__, FXNotesError
from .commands import COMMANDS


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fxnotes", description="A small notes CLI (F06a fixture)")
    p.add_argument("--version", action="version", version=f"fxnotes {__version__}")
    p.add_argument("--config", default=None, help="Path to config.toml")
    p.add_argument("--db", default=None, help="Path to SQLite database")
    sub = p.add_subparsers(dest="command", required=True, metavar="COMMAND")
    for name, cmd in COMMANDS.items():
        cmd.add_parser(sub)
    return p


def dispatch(args, ctx: dict) -> int:
    handler = COMMANDS[args.command]
    return handler.run(args, ctx)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    ctx: dict = {}
    try:
        from .config import load_config
        from .db import Database
        ctx["config"] = load_config(args.config)
        ctx["db"] = Database(ctx["config"]["db_path"])
        ctx["db"].connect()
        return dispatch(args, ctx)
    except FXNotesError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())