"""Resolucion de SKILL_DIR (NPR_HOME) segun D-120/D-145.

Algoritmo:
1. Si --skill-dir en CLI y validar -> ejecutar.
2. Si NPR_HOME en env y validar -> ejecutar.
3. Si HERMES_HOME en env -> ejecutar.
4. Probar rutas canonicas (proyecto, global, heredada, Windows).
   Validar con scripts/.npr-marker.
5. Si ninguna funciona -> NPR-E101.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _has_marker(path: Path) -> bool:
    return (path / "scripts" / ".npr-marker").is_file()


def resolve_skill_dir(cli_skill_dir: str | None) -> Path:
    """Devuelve la ruta absoluta de la skill. Lanza SystemExit(2) si no se puede."""
    candidates: list = []

    if cli_skill_dir:
        candidates.append(Path(cli_skill_dir).resolve())

    env_home = os.environ.get("NPR_HOME")
    if env_home:
        candidates.append(Path(env_home).resolve())

    hermes_home = os.environ.get("HERMES_HOME")
    if hermes_home:
        candidates.append(Path(hermes_home) / "skills" / "software-development" / "notemartin-project-review")

    cwd = Path.cwd()
    candidates.extend([
        cwd / ".hermes" / "skills" / "software-development" / "notemartin-project-review",
        cwd / ".kilo" / "skills" / "notemartin-project-review",
        cwd / ".cline" / "skills" / "notemartin-project-review",
        cwd / ".clinerules" / "skills" / "notemartin-project-review",
        cwd / ".agents" / "skills" / "notemartin-project-review",
        cwd / ".claude" / "skills" / "notemartin-project-review",
    ])
    home = Path.home()
    candidates.extend([
        home / ".hermes" / "skills" / "software-development" / "notemartin-project-review",
        home / ".kilo" / "skills" / "notemartin-project-review",
        home / ".cline" / "skills" / "notemartin-project-review",
        home / ".claude" / "skills" / "notemartin-project-review",
        home / ".agents" / "skills" / "notemartin-project-review",
    ])
    win = os.environ.get("LOCALAPPDATA")
    if win:
        candidates.append(Path(win) / "hermes" / "skills" / "software-development" / "notemartin-project-review")

    seen: set = set()
    for c in candidates:
        try:
            rp = c.resolve()
        except OSError:
            continue
        if rp in seen:
            continue
        seen.add(rp)
        if _has_marker(rp):
            os.environ["NPR_HOME"] = str(rp)
            return rp

    print(
        "[NPR-E101] no se pudo resolver SKILL_DIR\n"
        "causa: ninguna ruta candidata contiene scripts/.npr-marker\n"
        "accion: verifica la instalacion o usa --skill-dir para apuntar a la carpeta de la skill",
        file=sys.stderr,
    )
    sys.exit(2)