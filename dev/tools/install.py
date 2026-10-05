#!/usr/bin/env python3
"""Stub de `install.py` para F00. La versión completa se escribe en F87."""
import argparse
import sys
from pathlib import Path

PATHS = {
    "hermes": Path.home() / ".hermes" / "skills" / "software-development" / "notemartin-project-review",
    "cline": Path.home() / ".cline" / "skills" / "notemartin-project-review",
    "kilo": Path.home() / ".kilo" / "skills" / "notemartin-project-review",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala la skill en un runtime (stub F00)")
    parser.add_argument("--runtime", choices=list(PATHS), required=True)
    parser.add_argument("--src", type=Path, default=Path("skills/notemartin-project-review"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    dst = PATHS[args.runtime]
    print(f"Destino propuesto: {dst}")
    print(f"Origen: {args.src}")
    if args.dry_run:
        print("dry-run: no se copia nada")
        return 0
    print("Stub F00: la instalación real se escribe en F87", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())