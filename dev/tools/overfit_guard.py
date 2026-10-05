#!/usr/bin/env python3
"""Stub de `overfit_guard.py` para F00. La versión completa se escribe en F57."""
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Anti-sobreajuste (stub F00)")
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    args = parser.parse_args()

    if not args.skills_dir.is_dir():
        print(f"ERROR: {args.skills_dir} no existe", file=sys.stderr)
        return 1
    print(f"Stub F00: el guardián real se escribe en F57 (skills_dir={args.skills_dir})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())