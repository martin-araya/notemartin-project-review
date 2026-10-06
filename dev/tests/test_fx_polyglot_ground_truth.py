"""Tests del ground truth de fx-polyglot (F06f)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-polyglot"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-polyglot"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_3_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) == 3

    def test_features_match_spec(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert names == {"ingesta", "transformacion", "reporte"}

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) == 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) == 6

    def test_each_trap_has_resolution(self) -> None:
        gt = _load_gt()
        for t in gt["traps"] + gt["package_traps"]:
            assert t.get("resolution"), f"trap {t.get('id')} missing resolution"

    def test_outcome_user_sees_present(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert o.get("user_sees"), (
                    f"{f['id']}/{o['id']} missing user_sees"
                )

    def test_entry_points(self) -> None:
        gt = _load_gt()
        kinds = {ep["artifact"] for ep in gt["entry_points"]}
        assert "orchestrator.sh" in kinds
        assert "ingesta" in kinds
        assert "transformacion" in kinds


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXPOLY-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            if "unique_tokens" in rel:
                continue
            if path.suffix not in (".go", ".rs", ".sh", ".toml", ".json", ".md",
                                    ".yml", ".yaml", ".bats", ".txt", ".lock"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for tok in tokens:
                assert tok not in text, f"token {tok} found in {rel}"


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


class TestPolyglotStructure:
    def test_orchestrator_exists(self) -> None:
        assert (FIXTURE_ROOT / "orchestrator.sh").is_file()

    def test_go_module_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/ingesta/go.mod").is_file()

    def test_cargo_toml_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/transformacion/Cargo.toml").is_file()

    def test_go_handlers_files_exist(self) -> None:
        assert (FIXTURE_ROOT / "src/ingesta/handlers.go").is_file()
        assert (FIXTURE_ROOT / "src/ingesta/handlers_legacy.go").is_file()
        assert (FIXTURE_ROOT / "src/ingesta/registry.go").is_file()

    def test_go_build_tag_legacy(self) -> None:
        legacy = (FIXTURE_ROOT / "src/ingesta/handlers_legacy.go").read_text(
            encoding="utf-8"
        )
        assert "//go:build legacy" in legacy

    def test_go_build_tag_current(self) -> None:
        cur = (FIXTURE_ROOT / "src/ingesta/handlers.go").read_text(encoding="utf-8")
        assert "//go:build !legacy" in cur

    def test_cargo_features(self) -> None:
        cargo = (FIXTURE_ROOT / "src/transformacion/Cargo.toml").read_text(
            encoding="utf-8"
        )
        assert "[features]" in cargo
        for feat in ("v1", "v2", "strict", "legacy_compat"):
            assert feat in cargo, f"missing feature {feat}"

    def test_orchestrator_set_euo_pipefail(self) -> None:
        orch = (FIXTURE_ROOT / "orchestrator.sh").read_text(encoding="utf-8")
        assert "set -euo pipefail" in orch

    def test_orchestrator_has_trap(self) -> None:
        orch = (FIXTURE_ROOT / "orchestrator.sh").read_text(encoding="utf-8")
        assert "trap" in orch

    def test_orchestrator_uses_uname(self) -> None:
        orch = (FIXTURE_ROOT / "orchestrator.sh").read_text(encoding="utf-8")
        assert 'uname -s' in orch

    def test_go_init_function_in_handlers(self) -> None:
        cur = (FIXTURE_ROOT / "src/ingesta/handlers.go").read_text(encoding="utf-8")
        legacy = (FIXTURE_ROOT / "src/ingesta/handlers_legacy.go").read_text(
            encoding="utf-8"
        )
        assert "func init()" in cur
        assert "func init()" in legacy

    def test_registry_uses_init_map(self) -> None:
        registry = (FIXTURE_ROOT / "src/ingesta/registry.go").read_text(
            encoding="utf-8"
        )
        assert "handlers" in registry
        assert "Handler" in registry


class TestBatsFilesExist:
    def test_ingesta_bats(self) -> None:
        assert (FIXTURE_ROOT / "tests/ingesta.bats").is_file()

    def test_transformacion_v1_bats(self) -> None:
        assert (FIXTURE_ROOT / "tests/transformacion_v1.bats").is_file()

    def test_transformacion_v2_bats(self) -> None:
        assert (FIXTURE_ROOT / "tests/transformacion_v2.bats").is_file()

    def test_orchestrator_bats(self) -> None:
        assert (FIXTURE_ROOT / "tests/orchestrator.bats").is_file()

    def test_protocolo_exit_codes_bats(self) -> None:
        assert (FIXTURE_ROOT / "tests/protocolo_exit_codes.bats").is_file()

    def test_contrato_json_bats(self) -> None:
        assert (FIXTURE_ROOT / "tests/contrato_json.bats").is_file()

    def test_end_to_end_bats(self) -> None:
        assert (FIXTURE_ROOT / "tests/end_to_end.bats").is_file()

    def test_at_least_6_bats_files(self) -> None:
        files = list((FIXTURE_ROOT / "tests").glob("*.bats"))
        assert len(files) >= 6, f"only {len(files)} bats files"