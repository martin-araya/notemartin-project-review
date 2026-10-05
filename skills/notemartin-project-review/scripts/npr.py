#!/usr/bin/env python3
"""Stub de la CLI `npr` para F00. La implementación real se escribe desde F05."""
import argparse

__version__ = "0.1.0-rc0"


def main() -> int:
    parser = argparse.ArgumentParser(prog="npr", description="notemartin-project-review CLI (stub)")
    parser.add_argument("--version", action="version", version=f"npr {__version__}")
    args = parser.parse_args()
    print(f"npr {__version__} (stub)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())