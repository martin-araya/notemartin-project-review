#!/usr/bin/env python3
"""Stub de `check_ground_truth.py` para F00. La versión completa se escribe en F59."""
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida el ground truth de un fixture (stub F00)")
    parser.add_argument("gt_dir", type=Path)
    args = parser.parse_args()

    if not args.gt_dir.is_dir():
        print(f"ERROR: {args.gt_dir} no existe", file=sys.stderr)
        return 1
    print(f"Stub F00: la validación real se escribe en F59 (gt_dir={args.gt_dir})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())