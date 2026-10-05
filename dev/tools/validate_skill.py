#!/usr/bin/env python3
"""Stub de `validate_skill.py` para F00. La versión completa se escribe en F72."""
import argparse
import sys
from pathlib import Path

REQUIRED = ["SKILL.md", "scripts/npr.py"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida una instalación de la skill (stub F00)")
    parser.add_argument("skill_dir", type=Path, help="Carpeta de la skill")
    args = parser.parse_args()

    missing = [p for p in REQUIRED if not (args.skill_dir / p).is_file()]
    if missing:
        print(f"ERROR: faltan archivos obligatorios: {', '.join(missing)}", file=sys.stderr)
        return 2
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())