"""Tests del ground truth de fx-go-service (F06s)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-go-service"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-go-service"


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
        assert "ingesta-de-eventos" in names
        assert "agregacion" in names
        assert "exportacion" in names

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
        assert "go-chi/chi/v5" in names
        assert "google/wire" in names
        assert "mattn/go-sqlite3" in names

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
            assert tok.startswith("NPRGT-FXGO-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"node_modules", "coverage", ".git", "vendor", "stub-davecheney"}
        skip_files = {"unique_tokens.txt"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".go", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".ini", ".mod", ".sum", ".toml",
                                    ".tmpl", ".sql"):
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


class TestGoStructure:
    def test_main_ts(self) -> None:
        assert (FIXTURE_ROOT / "cmd/server/main.go").is_file()

    def test_legacy_main(self) -> None:
        assert (FIXTURE_ROOT / "cmd/legacy/main.go").is_file()

    def test_go_mod(self) -> None:
        assert (FIXTURE_ROOT / "go.mod").is_file()

    def test_sqlc_yaml(self) -> None:
        assert (FIXTURE_ROOT / "sqlc.yaml").is_file()

    def test_queries_sql(self) -> None:
        assert (FIXTURE_ROOT / "queries.sql").is_file()

    def test_wire_go(self) -> None:
        assert (FIXTURE_ROOT / "wire.go").is_file()

    def test_domain(self) -> None:
        for f in ("event.go", "repo.go"):
            assert (FIXTURE_ROOT / "internal/domain" / f).is_file(), f"missing {f}"

    def test_repo_sqlite(self) -> None:
        for f in ("sqlite.go", "driver.go", "init.go"):
            assert (FIXTURE_ROOT / "internal/repo/sqlite" / f).is_file(), f"missing {f}"

    def test_repo_sqlc_stub(self) -> None:
        assert (FIXTURE_ROOT / "internal/repo/sqlc/db.go").is_file()

    def test_services(self) -> None:
        for f in ("ingest_service.go", "aggregate_service.go", "export_service.go"):
            assert (FIXTURE_ROOT / "internal/service" / f).is_file(), f"missing {f}"

    def test_http(self) -> None:
        for f in ("handlers.go", "server.go", "legacy_export.go"):
            assert (FIXTURE_ROOT / "internal/http" / f).is_file(), f"missing {f}"

    def test_worker(self) -> None:
        assert (FIXTURE_ROOT / "internal/worker/pool.go").is_file()

    def test_config(self) -> None:
        assert (FIXTURE_ROOT / "internal/config/config.go").is_file()

    def test_debug(self) -> None:
        assert (FIXTURE_ROOT / "internal/debug.go").is_file()

    def test_migrations(self) -> None:
        assert (FIXTURE_ROOT / "migrations/001_initial.up.sql").is_file()

    def test_embedded_template(self) -> None:
        assert (FIXTURE_ROOT / "internal/service/templates/export.tmpl").is_file()

    def test_tests_dir(self) -> None:
        for f in ("ingest_test.go", "aggregate_test.go", "export_test.go",
                 "traps_ecosystem_test.go", "traps_package_test.go",
                 "traps_superficial_test.go"):
            assert (FIXTURE_ROOT / "tests" / f).is_file(), f"missing {f}"


class TestEcosystemTraps:
    def test_e01_implicit_interfaces_no_implements_keyword(self) -> None:
        domain = (FIXTURE_ROOT / "internal/domain/repo.go").read_text(encoding="utf-8")
        assert "type EventRepository interface" in domain
        assert "type Exporter interface" in domain
        sqlite = (FIXTURE_ROOT / "internal/repo/sqlite/sqlite.go").read_text(encoding="utf-8")
        # Buscamos la keyword 'implements' como statement (no en comentarios).
        code_lines = [
            ln for ln in sqlite.split("\n")
            if not ln.strip().startswith("//")
        ]
        assert not any("implements " in ln for ln in code_lines), (
            "SQLiteEventRepository NO debe usar keyword 'implements'"
        )

    def test_e02_init_function_and_blank_imports(self) -> None:
        driver = (FIXTURE_ROOT / "internal/repo/sqlite/driver.go").read_text(encoding="utf-8")
        init_ = (FIXTURE_ROOT / "internal/repo/sqlite/init.go").read_text(encoding="utf-8")
        main = (FIXTURE_ROOT / "cmd/server/main.go").read_text(encoding="utf-8")
        assert "func init()" in driver
        assert '_ "github.com/mattn/go-sqlite3"' in init_
        assert "github.com/mattn/go-sqlite3" in main

    def test_e03_go_generate_code(self) -> None:
        sqlc_yaml = (FIXTURE_ROOT / "sqlc.yaml").read_text(encoding="utf-8")
        db_stub = (FIXTURE_ROOT / "internal/repo/sqlc/db.go").read_text(encoding="utf-8")
        wire = (FIXTURE_ROOT / "wire.go").read_text(encoding="utf-8")
        assert "version:" in sqlc_yaml
        assert "sqlc" in db_stub
        assert "wire" in wire.lower() or "Wire" in wire

    def test_e04_goroutines_channels_select(self) -> None:
        pool = (FIXTURE_ROOT / "internal/worker/pool.go").read_text(encoding="utf-8")
        assert "go p.worker()" in pool
        assert "chan int" in pool
        assert "select {" in pool
        assert "case <-p.ctx.Done()" in pool
        assert "case jobID, ok := <-p.jobs" in pool

    def test_e05_build_tags(self) -> None:
        legacy = (FIXTURE_ROOT / "internal/http/legacy_export.go").read_text(encoding="utf-8")
        assert "//go:build legacy" in legacy

    def test_e06_go_embed(self) -> None:
        export_svc = (FIXTURE_ROOT / "internal/service/export_service.go").read_text(encoding="utf-8")
        assert "//go:embed" in export_svc
        assert "templates/*.tmpl" in export_svc
        assert "embed.FS" in export_svc


class TestPackageTraps:
    def test_p01_race_condition_in_worker_pool(self) -> None:
        pool = (FIXTURE_ROOT / "internal/worker/pool.go").read_text(encoding="utf-8")
        assert "p.processed++" in pool
        # Verificar que NO hay mutex.
        assert "sync.Mutex" not in pool

    def test_p02_goroutine_leak_on_shutdown(self) -> None:
        pool = (FIXTURE_ROOT / "internal/worker/pool.go").read_text(encoding="utf-8")
        assert "case <-p.ctx.Done()" in pool
        assert "if !ok {" in pool

    def test_p03_implicit_interface_mismatch(self) -> None:
        sqlite = (FIXTURE_ROOT / "internal/repo/sqlite/sqlite.go").read_text(encoding="utf-8")
        agg = (FIXTURE_ROOT / "internal/service/aggregate_service.go").read_text(encoding="utf-8")
        # Trampa P03: el exporter usa type="default" en vez del type del
        # payload.
        assert "ListByType(ctx, \"default\", 1000, 0)" in sqlite or "ListByType(ctx, \"default\"" in sqlite
        assert "ListByType" in agg

    def test_p04_init_side_effects_in_tests(self) -> None:
        driver = (FIXTURE_ROOT / "internal/repo/sqlite/driver.go").read_text(encoding="utf-8")
        assert "fmt.Println" in driver

    def test_p05_channel_deadlock(self) -> None:
        pool = (FIXTURE_ROOT / "internal/worker/pool.go").read_text(encoding="utf-8")
        assert "make(chan int)" in pool
        # No debe haber buffer.
        assert "make(chan int, " not in pool

    def test_p06_build_tag_typo(self) -> None:
        legacy = (FIXTURE_ROOT / "internal/http/legacy_export.go").read_text(encoding="utf-8")
        assert "//go:build legacy" in legacy
        assert "lagacy" not in legacy


class TestSuperficialTraps:
    def test_s01_dead_legacy_export_go(self) -> None:
        legacy = (FIXTURE_ROOT / "internal/http/legacy_export.go").read_text(encoding="utf-8")
        assert "//go:build legacy" in legacy
        assert "LegacyExportHandler" in legacy

    def test_s02_dead_legacy_binary(self) -> None:
        legacy = (FIXTURE_ROOT / "cmd/legacy/main.go").read_text(encoding="utf-8")
        assert "fx-go-service legacy binary - deprecated" in legacy

    def test_s03_dead_debug_helper(self) -> None:
        debug = (FIXTURE_ROOT / "internal/debug.go").read_text(encoding="utf-8")
        assert "func DebugPrintln" in debug
        main = (FIXTURE_ROOT / "cmd/server/main.go").read_text(encoding="utf-8")
        assert "DebugPrintln" not in main


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-go-service" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_go_mod_has_deps(self) -> None:
        mod = (FIXTURE_ROOT / "go.mod").read_text(encoding="utf-8")
        assert "github.com/go-chi/chi/v5" in mod
        assert "github.com/mattn/go-sqlite3" in mod
        assert "github.com/google/wire" in mod

    def test_sqlc_yaml_exists(self) -> None:
        sqlc_yaml = (FIXTURE_ROOT / "sqlc.yaml").read_text(encoding="utf-8")
        assert "sqlite3" in sqlc_yaml
        assert "internal/repo/sqlc" in sqlc_yaml

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25
        for tok in tokens:
            assert tok.startswith("NPRGT-FXGO-")