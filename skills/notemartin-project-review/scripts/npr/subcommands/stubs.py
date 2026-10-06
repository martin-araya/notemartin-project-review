"""Stubs de los subcomandos implementados en fases futuras.

Cada comando imprime [NPR-E113] y sale con codigo 0 (D-147).
"""
from __future__ import annotations

import sys


STUB_COMMANDS = [
    ("recon", "F25"),
    ("inventory", "F08"),
    ("classify", "F09"),
    ("stack", "F10"),
    ("deps", "F11"),
    ("lockfiles", "F12"),
    ("workspaces", "F13"),
    ("imports", "F14"),
    ("symbols", "F15-F16"),
    ("entrypoints", "F17"),
    ("surfaces", "F18"),
    ("env", "F19"),
    ("llm", "F20"),
    ("git", "F21"),
    ("graph", "F22"),
    ("partition", "F23"),
    ("ledger", "F24"),
    ("brief", "F27"),
    ("feature", "F33-F47"),
    ("surface", "F18/F47"),
    ("branches", "F34"),
    ("errors", "F39"),
    ("callgraph", "F42"),
    ("impact", "F46"),
    ("question", "F60"),
    ("claims", "F61"),
    ("verify", "F63"),
    ("lint", "F64"),
    ("gate", "F62"),
    ("openq", "F65"),
    ("report", "F66-F70"),
    ("diff", "F77"),
    ("compare", "F78"),
    ("dyn", "F53"),
    ("re", "F52"),
]


def add_parser(sub) -> None:
    for name, phase in STUB_COMMANDS:
        sub.add_parser(name, help=f"[stub {phase}] {name}")


def handle(args, ctx) -> int:
    name = args.command
    phase = next((p for n, p in STUB_COMMANDS if n == name), "?")
    print(
        f"[NPR-E113] comando '{name}' no disponible en F05; implementar en {phase}\n"
        f"causa: el subcomando esta registrado pero implementado en una fase futura\n"
        f"accion: consulta ROADMAP.md para ver en que fase se implementa",
        file=sys.stderr,
    )
    return 0