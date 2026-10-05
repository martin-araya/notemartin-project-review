#!/usr/bin/env python3
"""Stub de `check_thresholds.py` para F00. La versión completa se escribe en F66."""
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica umbrales de calidad (stub F00)")
    parser.add_argument("--thresholds", type=Path, default=Path("dev/evals/thresholds.json"))
    args = parser.parse_args()

    if not args.thresholds.is_file():
        print(f"INFO: {args.thresholds} no existe todavía; stub F00 devuelve 0", file=sys.stderr)
        return 0
    print(f"Stub F00: el verificador real se escribe en F66 ({args.thresholds})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())