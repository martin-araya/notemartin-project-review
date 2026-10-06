"""Subcomandos de la CLI `npr`.

Cada modulo expone `add_parser(subparsers)` y `handle(args, ctx) -> int`.
`ALL` lista los modulos en orden alfabetico.
"""
from . import init_cmd, config_cmd, status_cmd, resume_cmd, stubs

ALL = [init_cmd, config_cmd, status_cmd, resume_cmd, stubs]


def register(subparsers) -> None:
    for mod in ALL:
        mod.add_parser(subparsers)