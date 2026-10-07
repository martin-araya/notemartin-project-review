"""Tests del ground truth de fx-rust-axum (F06t)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-rust-axum"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-rust-axum"


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
        assert "catalogo" in names
        assert "precios" in names
        assert "sincronizacion" in names

    def test_each_feature_has_at_least_7_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 7, f"{f['id']}: expected >=7, got {n}"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) == 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) == 6

    def test_has_3_superficial_traps(self) -> None:
        gt = _load_gt()
        assert len(gt.get("superficial_traps", [])) == 3

    def test_each_trap_has_resolution(self) -> None:
        gt = _load_gt()
        for t in gt["traps"] + gt["package_traps"] + gt["superficial_traps"]:
            assert t.get("resolution"), f"trap {t.get('id')} missing resolution"

    def test_outcome_user_sees_present(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert o.get("user_sees"), f"{f['id']}/{o['id']} missing user_sees"

    def test_dependencies_listed(self) -> None:
        gt = _load_gt()
        names = {d["name"] for d in gt.get("dependencies", [])}
        assert "axum" in names
        assert "tokio" in names
        assert "sqlx" in names
        assert "serde" in names
        assert "thiserror" in names

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 12


class TestUniqueTokensFile:
    def test_at_least_25_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXRUST-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"target", "Cargo.lock", ".git", "tests"}
        skip_files = {"unique_tokens.txt", "Cargo.toml", "rust-toolchain.toml"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".rs", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".ini", ".toml", ".sql"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
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

    def test_all_decision_points_resolve(self) -> None:
        gt = _load_gt()
        errors = []
        for f in gt["features"]:
            fid = f["id"]
            for di, dp in enumerate(f.get("decision_points", [])):
                cite = f"{dp['file']}:{dp['line']}"
                errs = check_cite(FIXTURE_ROOT, cite)
                for e in errs:
                    errors.append(f"{fid}/dp[{di}]: {e}")
        if errors:
            pytest.fail("\n".join(errors[:20]))


class TestRustStructure:
    def test_main_rs(self) -> None:
        assert (FIXTURE_ROOT / "src/main.rs").is_file()

    def test_server_bin(self) -> None:
        assert (FIXTURE_ROOT / "src/bin/server.rs").is_file()

    def test_lib_rs(self) -> None:
        assert (FIXTURE_ROOT / "src/lib.rs").is_file()

    def test_cargo_toml(self) -> None:
        assert (FIXTURE_ROOT / "Cargo.toml").is_file()

    def test_rust_toolchain(self) -> None:
        assert (FIXTURE_ROOT / "rust-toolchain.toml").is_file()

    def test_derive_macro(self) -> None:
        for f in ("derive-macro/Cargo.toml", "derive-macro/src/lib.rs"):
            assert (FIXTURE_ROOT / f).is_file(), f"missing {f}"

    def test_build_rs(self) -> None:
        assert (FIXTURE_ROOT / "build.rs").is_file()

    def test_infra(self) -> None:
        for f in ("db.rs", "error.rs", "config.rs", "blanket_impl.rs"):
            assert (FIXTURE_ROOT / f"src/infra/{f}").is_file(), f"missing {f}"

    def test_features(self) -> None:
        for feature in ("catalog", "pricing", "sync"):
            for f in ("mod.rs", "entity.rs", "service.rs", "handler.rs"):
                assert (FIXTURE_ROOT / f"src/{feature}/{f}").is_file(), f"missing {feature}/{f}"

    def test_features_legacy(self) -> None:
        assert (FIXTURE_ROOT / "src/features_legacy.rs").is_file()

    def test_unsafe_ffi(self) -> None:
        assert (FIXTURE_ROOT / "src/unsafe_ffi.rs").is_file()

    def test_debug(self) -> None:
        assert (FIXTURE_ROOT / "src/debug.rs").is_file()

    def test_migrations(self) -> None:
        assert (FIXTURE_ROOT / "migrations/001_initial.sql").is_file()

    def test_tests_dir(self) -> None:
        for f in ("catalog_test.rs", "pricing_test.rs", "sync_test.rs",
                 "traps_ecosystem_test.rs", "traps_package_test.rs",
                 "traps_superficial_test.rs"):
            assert (FIXTURE_ROOT / "tests" / f).is_file(), f"missing {f}"


class TestEcosystemTraps:
    def test_e01_proc_macro_derive(self) -> None:
        derive = (FIXTURE_ROOT / "derive-macro/src/lib.rs").read_text(encoding="utf-8")
        assert "proc_macro_derive" in derive
        catalog = (FIXTURE_ROOT / "src/catalog/entity.rs").read_text(encoding="utf-8")
        assert "#[derive(Entity" in catalog

    def test_e02_blanket_impl(self) -> None:
        blanket = (FIXTURE_ROOT / "src/infra/blanket_impl.rs").read_text(encoding="utf-8")
        assert "impl<T> Json for T" in blanket
        assert "T: Serialize" in blanket

    def test_e03_cargo_features(self) -> None:
        cargo = (FIXTURE_ROOT / "Cargo.toml").read_text(encoding="utf-8")
        assert "[features]" in cargo
        assert "legacy" in cargo
        legacy = (FIXTURE_ROOT / "src/features_legacy.rs").read_text(encoding="utf-8")
        assert "#[cfg(feature" in legacy

    def test_e04_axum_extractors(self) -> None:
        catalog = (FIXTURE_ROOT / "src/catalog/handler.rs").read_text(encoding="utf-8")
        assert "State(pool)" in catalog
        assert "Json(req)" in catalog
        assert "Path(id)" in catalog

    def test_e05_error_flow_question(self) -> None:
        error = (FIXTURE_ROOT / "src/infra/error.rs").read_text(encoding="utf-8")
        assert "#[from]" in error
        assert "thiserror" in error
        service = (FIXTURE_ROOT / "src/catalog/service.rs").read_text(encoding="utf-8")
        assert "?" in service

    def test_e06_build_rs_and_unsafe_ffi(self) -> None:
        build_rs = (FIXTURE_ROOT / "build.rs").read_text(encoding="utf-8")
        assert "fn main()" in build_rs
        unsafe_ffi = (FIXTURE_ROOT / "src/unsafe_ffi.rs").read_text(encoding="utf-8")
        assert "extern \"C\"" in unsafe_ffi
        assert "unsafe" in unsafe_ffi


class TestPackageTraps:
    def test_p01_proc_macro_generates_wrong_impl(self) -> None:
        derive = (FIXTURE_ROOT / "derive-macro/src/lib.rs").read_text(encoding="utf-8")
        assert "fn entity_derive" in derive

    def test_p02_blanket_impl_no_conflict(self) -> None:
        blanket = (FIXTURE_ROOT / "src/infra/blanket_impl.rs").read_text(encoding="utf-8")
        assert "impl<T> Json for T" in blanket

    def test_p03_cargo_feature_typo(self) -> None:
        cargo = (FIXTURE_ROOT / "Cargo.toml").read_text(encoding="utf-8")
        assert "legacy = []" in cargo
        assert "lagacy" not in cargo

    def test_p04_axum_extractor_order(self) -> None:
        catalog = (FIXTURE_ROOT / "src/catalog/handler.rs").read_text(encoding="utf-8")
        state_pos = catalog.find("State(pool)")
        json_pos = catalog.find("Json(req)")
        assert state_pos is not None and json_pos is not None
        assert state_pos < json_pos, "State debe ir antes que Json"

    def test_p05_from_impl_no_cycles(self) -> None:
        error = (FIXTURE_ROOT / "src/infra/error.rs").read_text(encoding="utf-8")
        assert "From<AppError>" not in error, "AppError no debe tener From para si mismo (ciclo)"

    def test_p06_build_rs_executes(self) -> None:
        build_rs = (FIXTURE_ROOT / "build.rs").read_text(encoding="utf-8")
        assert "fn main()" in build_rs


class TestSuperficialTraps:
    def test_s01_dead_debug_helper(self) -> None:
        debug = (FIXTURE_ROOT / "src/debug.rs").read_text(encoding="utf-8")
        assert "debug_println" in debug

    def test_s02_dead_legacy_feature(self) -> None:
        legacy = (FIXTURE_ROOT / "src/features_legacy.rs").read_text(encoding="utf-8")
        assert "LegacyEvent" in legacy
        assert "#[cfg(feature" in legacy

    def test_s03_dead_unused_function(self) -> None:
        legacy = (FIXTURE_ROOT / "src/features_legacy.rs").read_text(encoding="utf-8")
        assert "pub fn hash" in legacy


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-rust-axum" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_cargo_toml_has_deps(self) -> None:
        cargo = (FIXTURE_ROOT / "Cargo.toml").read_text(encoding="utf-8")
        assert "axum" in cargo
        assert "tokio" in cargo
        assert "sqlx" in cargo
        assert "serde" in cargo
        assert "thiserror" in cargo

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25
        for tok in tokens:
            assert tok.startswith("NPRGT-FXRUST-")