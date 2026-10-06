"""Subcomando `npr resume` (stub; implementado en F76)."""
from __future__ import annotations

from .. import errors_catalog


COMMAND = "resume"


def add_parser(sub):
    p = sub.add_parser(COMMAND, help="Reanuda un analisis desde el ultimo checkpoint (stub F76)")
    return p


def handle(args, ctx) -> int:
    print(errors_catalog.format_error("NPR-E113", command="resume", fase="F76"), file=__import__("sys").stderr)
    return 0