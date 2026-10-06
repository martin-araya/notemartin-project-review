"""Tests para F06a: fixture fx-python-cli + ground truth + verificador."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = ROOT / "dev" / "fixtures" / "fx-python-cli"
GT_DIR = ROOT / "dev" / "ground-truth" / "fx-python-cli"
GT_JSON = GT_DIR / "ground_truth.json"
GT_MD = GT_DIR / "GROUND_TRUTH.md"


def _run(args, cwd=None, env=None):
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=str(cwd or Path.cwd()),
        capture_output=True, text=True,
        env={**os.environ, **(env or {})},
    )
    return proc


def test_01_check_ground_truth_passes_for_fx_python_cli():
    proc = _run(
        [str(ROOT / "dev" / "tools" / "check_ground_truth.py"), str(GT_DIR)],
    )
    assert proc.returncode == 0, f"stdout={proc.stdout!r} stderr={proc.stderr!r}"


def test_02_fixture_has_no_unique_tokens():
    tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
    assert tokens, "unique_tokens.txt vacio"
    leak = []
    for p in FIXTURE.rglob("*"):
        if p.is_file() and p.name == "unique_tokens.txt":
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for tok in tokens:
            if tok in text:
                leak.append((p.relative_to(FIXTURE), tok))
    assert not leak, f"tokens leaked: {leak}"


def test_03_ground_truth_every_feature_has_min_6_outcomes():
    gt = json.loads(GT_JSON.read_text())
    for feat in gt["features"]:
        n = len(feat.get("outcomes", []))
        assert n >= 6, f"{feat['id']}: solo {n} outcomes (<6)"


def test_04_all_six_specific_traps_present():
    gt = json.loads(GT_JSON.read_text())
    package_traps = gt.get("package_traps", [])
    kinds = {t["kind"] for t in package_traps}
    required = {
        "combination_two_settings",
        "empty_catch_swallows_error",
        "timeout_retry",
        "race_condition",
        "dead_branch",
        "user_rejection",
    }
    missing = required - kinds
    assert not missing, f"faltan trampas: {missing}"


def test_05_pytest_on_fixture_passes():
    proc = _run(
        ["-m", "pytest", "tests/"],
        cwd=FIXTURE,
        env={"PYTHONPATH": str(FIXTURE / "src")},
    )
    assert proc.returncode == 0, f"pytest fallo:\n{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}"


def test_06_every_cite_in_ground_truth_resolves():
    proc = _run(
        [str(ROOT / "dev" / "tools" / "check_ground_truth.py"), str(GT_DIR)],
    )
    assert proc.returncode == 0, f"referencias rotas: {proc.stderr}"


def test_07_build_history_script_creates_commits(tmp_path):
    import shutil
    clone = tmp_path / "fx"
    shutil.copytree(FIXTURE, clone)
    proc = subprocess.run(
        ["bash", str(clone / "build-history.sh")],
        cwd=clone, capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"build-history fallo: {proc.stderr}"
    proc = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"], cwd=clone, capture_output=True, text=True,
    )
    n = int(proc.stdout.strip())
    assert n >= 8, f"solo {n} commits (>=8 requeridos)"


def test_08_fixture_does_not_mention_ground_truth():
    forbidden = ["ground_truth", "NPRGT-FXNOTES", "ground-truth", "trampas plantadas"]
    leak = []
    for p in FIXTURE.rglob("*"):
        if p.is_file() and p.name == "unique_tokens.txt":
            continue
        if p.suffix in (".db", ".pyc", ".png", ".jpg"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for word in forbidden:
            if word in text:
                leak.append((p.relative_to(FIXTURE), word))
    assert not leak, f"fixture menciona ground truth: {leak}"


def test_09_ground_truth_traps_have_resolution():
    gt = json.loads(GT_JSON.read_text())
    for trap in gt.get("traps", []) + gt.get("package_traps", []):
        assert trap.get("resolution"), f"{trap.get('id')}: resolution vacia"


def test_10_ground_truth_minimum_features_and_surfaces():
    gt = json.loads(GT_JSON.read_text())
    assert len(gt["features"]) >= 3, f"solo {len(gt['features'])} features"
    assert len(gt["surfaces"]) >= 1, f"surfaces vacias"
    assert len(gt.get("package_traps", [])) >= 6, "package_traps < 6"