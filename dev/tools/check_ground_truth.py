#!/usr/bin/env python3
"""Verificador del ground truth de un fixture (F06a).

Carga dev/ground-truth/<fixture>/ground_truth.json y verifica que cada
referencia `archivo:linea` (con `#symbol` opcional) existe en el fixture
y que el simbolo aparece en la linea o el rango.

CLI:
    python dev/tools/check_ground_truth.py <gt_dir>

Salidas:
- 0 si todo OK
- 2 si hay referencias rotas
- 1 si error de uso
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CITE_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_./-]+):"
    r"(?P<line>\d+)"
    r"(?:-(?P<end>\d+))?"
    r"(?:#(?P<symbol>[A-Za-z_][A-Za-z0-9_.]*))?"
)


def _check_cite(fixture_root: Path, cite: str, where: str) -> list:
    """Devuelve lista de errores; vacia si OK."""
    errs = []
    m = CITE_RE.search(cite)
    if not m:
        errs.append(f"{where}: cite mal formado: {cite!r}")
        return errs
    rel = m.group("path")
    line = int(m.group("line"))
    end = int(m.group("end")) if m.group("end") else line
    symbol = m.group("symbol")

    target = fixture_root / rel
    if not target.is_file():
        errs.append(f"{where}: archivo inexistente: {rel}")
        return errs

    try:
        text = target.read_text(encoding="utf-8")
    except OSError as exc:
        errs.append(f"{where}: no se pudo leer {rel}: {exc}")
        return errs

    lines = text.splitlines()
    if line < 1 or line > len(lines):
        errs.append(f"{where}: linea {line} fuera de rango en {rel} (1..{len(lines)})")
        return errs
    if end > len(lines):
        errs.append(f"{where}: linea final {end} fuera de rango en {rel}")
        return errs

    if symbol:
        haystack = "\n".join(lines[line - 1:end])
        if symbol not in haystack:
            errs.append(
                f"{where}: simbolo {symbol!r} no encontrado en {rel}:{line}-{end}"
            )

    return errs


def check(gt_dir: Path, fixture_root: Path) -> list:
    """Devuelve lista de errores del ground truth."""
    errs = []
    gt_path = gt_dir / "ground_truth.json"
    if not gt_path.is_file():
        return [f"no existe {gt_path}"]

    try:
        gt = json.loads(gt_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{gt_path} no es JSON valido: {exc}"]

    features = gt.get("features", [])
    if len(features) < 3:
        errs.append(f"features: solo {len(features)} (<3 minimo por paquete)")

    for fi, feature in enumerate(features):
        fid = feature.get("id", f"<feature[{fi}]>")
        for si, step in enumerate(feature.get("traces", [])):
            cite = step.get("cite", "")
            errs.extend(_check_cite(fixture_root, cite, f"{fid}/trace[{si}]"))
        for di, dp in enumerate(feature.get("decision_points", [])):
            f = dp.get("file", "")
            ln = dp.get("line", 0)
            target = fixture_root / f
            if not target.is_file():
                errs.append(f"{fid}/dp[{di}]: archivo inexistente {f}")
                continue
            lines = target.read_text(encoding="utf-8").splitlines()
            if ln < 1 or ln > len(lines):
                errs.append(f"{fid}/dp[{di}]: linea {ln} fuera de rango en {f}")

        for oi, outcome in enumerate(feature.get("outcomes", [])):
            if not outcome.get("user_sees"):
                errs.append(f"{fid}/outcome[{oi}]: user_sees vacio")
        if len(feature.get("outcomes", [])) < 6:
            errs.append(f"{fid}: solo {len(feature.get('outcomes', []))} outcomes (<6)")

    for ti, trap in enumerate(gt.get("traps", [])):
        if not trap.get("resolution"):
            errs.append(f"traps[{ti}]: resolution vacia")
    for ti, trap in enumerate(gt.get("package_traps", [])):
        if not trap.get("resolution"):
            errs.append(f"package_traps[{ti}]: resolution vacia")

    if len(gt.get("package_traps", [])) < 6:
        errs.append(f"package_traps: solo {len(gt.get('package_traps', []))} (<6)")

    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida el ground truth de un fixture")
    parser.add_argument("gt_dir", type=Path, help="Directorio con ground_truth.json del fixture")
    args = parser.parse_args()

    if not args.gt_dir.is_dir():
        print(f"ERROR: {args.gt_dir} no existe", file=sys.stderr)
        return 1

    fixture_name = args.gt_dir.name
    fixture_root = args.gt_dir.parent.parent / "fixtures" / fixture_name
    if not fixture_root.is_dir():
        print(f"ERROR: no se encontro el repo del fixture en {fixture_root}", file=sys.stderr)
        return 1

    errs = check(args.gt_dir, fixture_root)
    if errs:
        print(f"FALLO ({len(errs)} problemas):", file=sys.stderr)
        for e in errs:
            print(f"  {e}", file=sys.stderr)
        return 2

    print(f"OK ({args.gt_dir.name})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())