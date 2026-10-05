#!/usr/bin/env python3
"""Stub de `check_docs.py` para F00. La versión completa se escribe en F88."""
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida documentación (stub F00)")
    parser.add_argument("--docs-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    if not args.docs_dir.is_dir():
        print(f"ERROR: {args.docs_dir} no existe", file=sys.stderr)
        return 1
    print(f"Stub F00: el verificador real se escribe en F88 (docs_dir={args.docs_dir})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())