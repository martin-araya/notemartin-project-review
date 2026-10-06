"""Tests del ground truth de fx-ts-agent-extension (F06b)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-ts-agent-extension"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-ts-agent-extension"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_4_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) >= 4

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) >= 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) >= 6

    def test_messages_ts_is_over_5000_lines(self) -> None:
        path = FIXTURE_ROOT / "src/host/messages.ts"
        assert path.is_file()
        n = len(path.read_text(encoding="utf-8").splitlines())
        assert n >= 5000, f"messages.ts has only {n} lines"

    def test_12_message_types(self) -> None:
        from collections import Counter
        gt = _load_gt()
        msg_types = Counter()
        for s in gt["surfaces"]:
            if s.get("kind") == "webview":
                msg_types[s["name"]] += 1
        assert len([k for k in msg_types if k.startswith("webview/")]) >= 12

    def test_3_modes_listed(self) -> None:
        gt = _load_gt()
        flat = json.dumps(gt)
        for m in ("plan", "code", "ask"):
            assert f'"{m}"' in flat, f"mode {m} not referenced"

    def test_6_tools_listed(self) -> None:
        gt = _load_gt()
        # Cada tool debe aparecer como nombre o como nombre-de-variable camelCase
        # en al menos un lugar del ground truth.
        flat = json.dumps(gt)
        for t in ("read_file", "list_dir", "search_code", "run_terminal_cmd", "ask_user", "propose_plan"):
            camel = t.replace("_", "")
            camel_caps = "".join(p.capitalize() for p in t.split("_"))
            assert t in flat or camel_caps in flat or camel in flat, f"tool {t} not referenced"

    def test_unique_tokens_not_in_src(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXAGENT-")
        # Walk src/ and ensure none of these tokens appear.
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in (".ts", ".tsx", ".json", ".md", ".mjs", ".js", ".css", ".html"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for tok in tokens:
                if tok in text:
                    # allow in tests/ ground truth
                    rel = path.relative_to(FIXTURE_ROOT).as_posix()
                    assert "unique_tokens" in rel, f"token {tok} found in {rel}"


class TestAllCitesValid:
    def test_all_traces_resolve(self) -> None:
        gt = _load_gt()
        errors = []
        for f in gt["features"]:
            fid = f["id"]
            for ti, t in enumerate(f.get("traces", [])):
                cite = t.get("cite", "")
                if not cite:
                    continue
                errs = check_cite(FIXTURE_ROOT, cite)
                for e in errs:
                    errors.append(f"{fid}/trace[{ti}]: {e}")
        if errors:
            pytest.fail("\n".join(errors[:20]))

    def test_all_decision_point_files_exist(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for dp in f.get("decision_points", []):
                p = FIXTURE_ROOT / dp["file"]
                assert p.is_file(), f"dp file missing: {dp['file']}"


class TestUniqueTokensFile:
    def test_at_least_20(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
