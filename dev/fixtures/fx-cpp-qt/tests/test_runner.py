#!/usr/bin/env python3
"""F06z: test_runner.py - compila y ejecuta los tests Qt Test.

Patron: usa el harness estandar de CMake + ctest. Este runner es un
wrapper que configura el offscreen platform y parsea el resultado.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = FIXTURE_ROOT / "build"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    env = os.environ.copy()
    env.setdefault("QT_QPA_PLATFORM", "offscreen")

    # 1) Compilar (incremental).
    print("Configurando con CMake...")
    cfg = subprocess.run(
        ["cmake", "-S", str(FIXTURE_ROOT), "-B", str(BUILD_DIR),
         "-DCMAKE_BUILD_TYPE=Debug"],
        capture_output=True, text=True, env=env,
    )
    if cfg.returncode != 0:
        sys.stderr.write(cfg.stdout)
        sys.stderr.write(cfg.stderr)
        return 2
    if args.verbose:
        sys.stdout.write(cfg.stdout)

    print("Compilando...")
    build = subprocess.run(
        ["cmake", "--build", str(BUILD_DIR), "--parallel"],
        capture_output=True, text=True, env=env,
    )
    if build.returncode != 0:
        sys.stderr.write(build.stdout)
        sys.stderr.write(build.stderr)
        return 2
    if args.verbose:
        sys.stdout.write(build.stdout)

    # 2) Ejecutar ctest.
    print("Corriendo ctest...")
    ct = subprocess.run(
        ["ctest", "--test-dir", str(BUILD_DIR), "--output-on-failure"],
        capture_output=True, text=True, env=env,
    )
    sys.stdout.write(ct.stdout)
    if ct.stderr:
        sys.stderr.write(ct.stderr)
    return ct.returncode


if __name__ == "__main__":
    raise SystemExit(main())
