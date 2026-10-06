#!/usr/bin/env python3
"""Entry point de la CLI `npr`.

Permite ejecutar `python scripts/npr.py ...` desde la raiz de la skill.
Tambien expone el modulo para `python -m npr`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from npr.cli import main

if __name__ == "__main__":
    raise SystemExit(main())