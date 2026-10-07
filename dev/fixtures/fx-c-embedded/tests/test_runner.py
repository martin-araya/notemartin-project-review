#!/usr/bin/env python3
"""F06y: test_runner.py - compila y ejecuta los tests Unity en host.

Este runner es el equivalente simplificado de Ceedling/Ruby para
nuestro fixture:
  1. Compila cada tests/test_*.c con gcc -DHOST_TEST=1 + unity_internals.c
     + las sources del firmware + hal_host.c + board_host.c.
  2. Ejecuta el binario resultante.
  3. Parsea la salida y reporta los resultados en formato similar a
     `ctest --output-on-failure`.

El runner retorna 0 si todos los tests pasan, distinto de 0 en caso
contrario. Esto permite integrarlo con `make test` y con
`run_fixture_tests.py`.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = FIXTURE_ROOT / "src"
INCLUDE_DIR = FIXTURE_ROOT / "include"
TESTS_DIR = FIXTURE_ROOT / "tests"
BUILD_DIR = FIXTURE_ROOT / "build" / "tests"


def find_test_sources() -> list[Path]:
    """Devuelve la lista de archivos tests/test_*.c."""
    return sorted(TESTS_DIR.glob("test_*.c"))


def compile_test(test_c: Path, unity_c: Path) -> Path:
    """Compila un archivo de test con unity_internals y las sources."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    out = BUILD_DIR / test_c.stem
    cmd = [
        "gcc",
        "-std=c99",
        "-DHOST_TEST=1",
        "-Wno-unused-parameter",
        "-I", str(INCLUDE_DIR),
        "-I", str(INCLUDE_DIR / "tests"),
        "-I", str(SRC_DIR),
        str(test_c),
        str(unity_c),
        str(SRC_DIR / "startup.c"),
        # No linkamos main.c porque cada test_*.c define su propio main().
        str(SRC_DIR / "sensors.c"),
        str(SRC_DIR / "uart_protocol.c"),
        str(SRC_DIR / "power_modes.c"),
        str(SRC_DIR / "command_dispatch.c"),
        str(SRC_DIR / "hal" / "hal_host.c"),
        str(SRC_DIR / "board" / "board_host.c"),
        str(SRC_DIR / "legacy_helpers.c"),
        "-o", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(f"  compile failed for {test_c.name}:\n")
        sys.stderr.write(r.stderr)
        sys.stderr.write("\n")
        raise SystemExit(2)
    return out


def run_test(binary: Path) -> tuple[int, str, str]:
    """Ejecuta el binario de test y devuelve (returncode, stdout, stderr)."""
    r = subprocess.run([str(binary)], capture_output=True, text=True, timeout=20,
                       encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr


def parse_summary(stdout: str) -> tuple[int, int, int]:
    """Parsea la linea 'Unity tests: X failed (...), Y ignored, Z total'."""
    m = re.search(r"Unity tests:\s*(\d+)\s*failed\s*\((\d+)\),\s*(\d+)\s*ignored\s*\((\d+)\),\s*(\d+)\s*total", stdout)
    if not m:
        return 0, 0, 0
    failed = int(m.group(1))
    ignored = int(m.group(3))
    total = int(m.group(5))
    return failed, ignored, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    unity_c = TESTS_DIR / "unity_internals.c"
    if not unity_c.is_file():
        print(f"ERROR: {unity_c} no existe", file=sys.stderr)
        return 2

    test_files = find_test_sources()
    if not test_files:
        print("ERROR: no se encontraron tests/test_*.c", file=sys.stderr)
        return 2

    print(f"F06y test runner: {len(test_files)} archivos de test")
    total_failed = 0
    total_passed = 0
    total_ignored = 0
    grand_total = 0

    for test_c in test_files:
        print(f"\n=== {test_c.name} ===")
        try:
            binary = compile_test(test_c, unity_c)
        except SystemExit:
            total_failed += 1
            grand_total += 1
            continue
        rc, out, err = run_test(binary)
        if args.verbose or rc != 0:
            sys.stdout.write(out)
            if err:
                sys.stderr.write(err)
        failed, ignored, total = parse_summary(out)
        if rc != 0 or failed > 0:
            total_failed += failed
        else:
            total_passed += total
        total_ignored += ignored
        grand_total += total

    print("\n--- resumen ---")
    print(f"Unity tests: {total_failed} failed, {total_passed} passed, {total_ignored} ignored, {grand_total} total")
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
