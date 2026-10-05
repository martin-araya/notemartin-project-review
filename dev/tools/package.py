#!/usr/bin/env python3
"""Stub de `package.py` para F00. La versión completa se escribe en F73."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_SRC = ROOT / "skills" / "notemartin-project-review"
DST = ROOT / "dist" / "notemartin-project-review"


def main() -> int:
    if not SKILL_SRC.is_dir():
        print(f"ERROR: no existe {SKILL_SRC}", file=sys.stderr)
        return 1
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SKILL_SRC, DST)
    print(f"Empaquetado en {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())