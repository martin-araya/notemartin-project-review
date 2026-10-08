"""Tests del ground truth de fx-sql-tsql (F06aj)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-sql-tsql"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-sql-tsql"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_3_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) == 3

    def test_features_match_spec(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert "stock" in names
        assert "reconcile" in names
        assert "dashboard" in names

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


# ---------------------------------------------------------------------------
# Outcomes & citations
# ---------------------------------------------------------------------------


class TestOutcomesAndCitations:
    def test_outcome_user_sees_present(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert o.get("user_sees"), f"{f['id']}/{o['id']} missing user_sees"

    def test_each_outcome_has_reversible(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert "reversible" in o, f"{f['id']}/{o['id']} missing reversible"

    def test_decision_points_have_branches(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for dp in f.get("decision_points", []):
                assert dp.get("branches"), f"{f['id']}/{dp['id']} missing branches"
                assert dp.get("file"), f"{f['id']}/{dp['id']} missing file"
                assert isinstance(dp.get("line"), int), f"{f['id']}/{dp['id']} line must be int"

    def test_dependencies_listed(self) -> None:
        gt = _load_gt()
        names = {d["name"] for d in gt.get("dependencies", [])}
        assert "sql-server-2022" in names
        assert "tsql" in names
        assert "sqlcmd" in names
        assert "sql-agent" in names

    def test_entry_points_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("entry_points", [])) >= 20

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 15


# ---------------------------------------------------------------------------
# Unique tokens
# ---------------------------------------------------------------------------


class TestUniqueTokensFile:
    def test_at_least_30_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 30, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXSQLTS-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {".sqlserver_data", "Generated"}
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "Makefile",
            "manifest.yml", "Dockerfile.test", "README.md",
            ".gitignore", "entrypoint.sh", "msodbcsql.ini",
        }
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(p in skip_dirs for p in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".sql", ".sh", ".conf", ".md", ".txt", ".yml", ".yaml", ".ini"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            for tok in tokens:
                assert tok not in text, f"token {tok} found in {rel}"


# ---------------------------------------------------------------------------
# Cites
# ---------------------------------------------------------------------------


class TestAllCitesValid:
    def test_all_traps_resolve(self) -> None:
        gt = _load_gt()
        errors = []
        for t in gt["traps"] + gt["package_traps"] + gt["superficial_traps"]:
            where = t.get("where", "")
            where_clean = re.split(r":[0-9]+$", where, maxsplit=1)[0]
            full = FIXTURE_ROOT / where_clean
            if not full.is_file():
                errors.append(f"trap {t['id']}: missing file {where_clean}")
        assert not errors, "trap locations with missing files:\n" + "\n".join(errors)

    def test_all_surfaces_have_handler_file(self) -> None:
        gt = _load_gt()
        for s in gt.get("surfaces", []):
            f = s.get("file", "")
            if not f or "/" not in f:
                continue
            f_clean = re.split(r":[0-9]+$", f, maxsplit=1)[0]
            full = FIXTURE_ROOT / f_clean
            assert full.is_file(), f"surface {s.get('id')} missing file {f_clean}"

    def test_entry_point_cites_exist(self) -> None:
        gt = _load_gt()
        errors = []
        for ep in gt.get("entry_points", []):
            f = ep["file"]
            cite = f if ":" in f else f"{f}:1"
            errs = check_cite(FIXTURE_ROOT, cite)
            if errs:
                errors.append(f"entry_point {ep['id']}: {errs}")
        if errors:
            pytest.fail("\n".join(errors[:10]))


# ---------------------------------------------------------------------------
# SQL Server structure
# ---------------------------------------------------------------------------


class TestSqlServerStructure:
    def test_db_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "db").is_dir()

    def test_install_sql_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/install.sql").is_file()

    def test_uninstall_sql_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/uninstall.sql").is_file()

    def test_v1_init_schema_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V001__init_schema.sql").is_file()

    def test_v2_init_triggers_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V002__init_triggers.sql").is_file()

    def test_v3_recursive_cte_bom_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V003__recursive_cte_bom.sql").is_file()

    def test_v4_dynamic_sql_search_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V004__dynamic_sql_search.sql").is_file()

    def test_v5_merge_conciliacion_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V005__merge_conciliacion.sql").is_file()

    def test_v6_global_temp_inventory_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V006__global_temp_inventory.sql").is_file()

    def test_v7_sql_agent_jobs_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V007__sql_agent_jobs.sql").is_file()

    def test_v8_legacy_sprocs_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V008__legacy_sprocs.sql").is_file()

    def test_r_recalc_stock_totals_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/R__recalc_stock_totals.sql").is_file()

    def test_r_rebuild_report_cache_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/R__rebuild_report_cache.sql").is_file()

    def test_sql_views_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/views.sql").is_file()

    def test_sql_synonyms_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/synonyms.sql").is_file()

    def test_sql_functions_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/functions.sql").is_file()

    def test_sql_legacy_artifact_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/legacy_artifact.sql").is_file()

    def test_seed_stock_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/seed/seed_stock.sql").is_file()

    def test_seed_movements_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/seed/seed_movements.sql").is_file()

    def test_seed_bom_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/seed/seed_bom.sql").is_file()

    def test_test_runner_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/test/test_runner.sql").is_file()

    def test_tsql_tests_exist(self) -> None:
        expected = [
            "01_stock_test.sql",
            "02_reconcile_test.sql",
            "03_reports_test.sql",
            "04_triggers_test.sql",
            "05_sql_agent_test.sql",
            "06_trap_ecosystem_test.sql",
            "07_trap_package_test.sql",
            "08_deprecated_test.sql",
        ]
        for name in expected:
            f = FIXTURE_ROOT / "db/test" / name
            assert f.is_file(), f"missing {f}"


# ---------------------------------------------------------------------------
# Migrations present
# ---------------------------------------------------------------------------


class TestMigrationsPresent:
    def test_v001_to_v008_cover_init_triggers_cte_merge_temp_sql_agent_legacy(self) -> None:
        # Sanity check that the migrations cover the 8 ecosystem traps.
        expected = [
            ("V001", "init_schema"),
            ("V002", "init_triggers"),
            ("V003", "recursive_cte_bom"),
            ("V004", "dynamic_sql_search"),
            ("V005", "merge_conciliacion"),
            ("V006", "global_temp_inventory"),
            ("V007", "sql_agent_jobs"),
            ("V008", "legacy_sprocs"),
        ]
        for vname, slug in expected:
            assert (FIXTURE_ROOT / f"db/migration/{vname}__{slug}.sql").is_file(), \
                f"missing {vname}__{slug}.sql"

    def test_repeatable_R__present(self) -> None:
        files = list((FIXTURE_ROOT / "db/migration").glob("R__*.sql"))
        assert len(files) == 2, f"expected 2 R__ files, got {len(files)}"


# ---------------------------------------------------------------------------
# SQL Agent configured
# ---------------------------------------------------------------------------


class TestSqlAgentConfigured:
    def test_sql_agent_jobs_contains_3_jobs(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V007__sql_agent_jobs.sql").read_text(encoding="utf-8")
        assert "JOB_HOURLY_RECALC_TOTALS" in content
        assert "JOB_DAILY_REBUILD_REPORT_CACHE" in content
        assert "JOB_LEGACY_PURGE" in content

    def test_sql_agent_jobs_uses_sp_add_job(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V007__sql_agent_jobs.sql").read_text(encoding="utf-8")
        assert "sp_add_job" in content
        assert "sp_add_schedule" in content
        assert "sp_attach_schedule" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_sp_executesql(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V004__dynamic_sql_search.sql").read_text(encoding="utf-8")
        assert "sp_executesql" in content
        assert "@pattern" in content

    def test_e2_merge_output(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V005__merge_conciliacion.sql").read_text(encoding="utf-8")
        assert "MERGE" in content
        assert "OUTPUT $action" in content
        assert "reconcile_audit" in content

    def test_e3_triggers_after_and_instead_of(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V002__init_triggers.sql").read_text(encoding="utf-8")
        assert "AFTER INSERT" in content
        assert "INSTEAD OF UPDATE" in content

    def test_e4_recursive_cte(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V003__recursive_cte_bom.sql").read_text(encoding="utf-8")
        assert "WITH bom_tree AS" in content
        assert "UNION ALL" in content

    def test_e5_global_temp_table(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V006__global_temp_inventory.sql").read_text(encoding="utf-8")
        assert "##global_stock_temp" in content

    def test_e6_sql_agent_3_jobs(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V007__sql_agent_jobs.sql").read_text(encoding="utf-8")
        # 3 sp_add_job invocations
        count = content.count("sp_add_job\n")
        assert count >= 3, f"expected >=3 sp_add_job invocations, got {count}"


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_dynamic_sql_concat(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V004__dynamic_sql_search.sql").read_text(encoding="utf-8")
        # Strip SQL comments
        no_comments = re.sub(r"--[^\n]*", "", content)
        assert "+ @raw_filter" in no_comments

    def test_p2_merge_missing_not_matched_by_source(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V005__merge_conciliacion.sql").read_text(encoding="utf-8")
        no_comments = re.sub(r"--[^\n]*", "", content)
        # usp_reconcile_partial does NOT have NOT MATCHED BY SOURCE
        assert "usp_reconcile_partial" in content
        # Search for the body of usp_reconcile_partial only
        partial_start = content.index("CREATE OR ALTER PROCEDURE dbo.usp_reconcile_partial")
        partial_end = content.find("GO", partial_start)
        partial_body = content[partial_start:partial_end] if partial_end > 0 else content[partial_start:]
        partial_clean = re.sub(r"--[^\n]*", "", partial_body)
        assert "NOT MATCHED BY SOURCE" not in partial_clean

    def test_p3_instead_of_omits_quantity(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V002__init_triggers.sql").read_text(encoding="utf-8")
        no_comments = re.sub(r"--[^\n]*", "", content)
        # Look at INSTEAD OF UPDATE section
        iot_start = no_comments.index("INSTEAD OF UPDATE")
        iot_body = no_comments[iot_start:]
        iot_end = iot_body.index("END")
        iot_clean = iot_body[:iot_end]
        assert "UPDATE si" in iot_clean
        assert "quantity_on_hand" not in iot_clean

    def test_p4_cte_cycle_in_bom(self) -> None:
        content = (FIXTURE_ROOT / "db/seed/seed_bom.sql").read_text(encoding="utf-8")
        no_comments = re.sub(r"--[^\n]*", "", content)
        # Cycle A->B->C->A: parent SKU-A003, child SKU-A001
        assert "SKU-A003" in no_comments and "SKU-A001" in no_comments

    def test_p5_temp_consume_no_cleanup(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V006__global_temp_inventory.sql").read_text(encoding="utf-8")
        no_comments = re.sub(r"--[^\n]*", "", content)
        # Search only in usp_temp_consume body
        consume_start = no_comments.index("CREATE OR ALTER PROCEDURE dbo.usp_temp_consume")
        consume_body = no_comments[consume_start:]
        consume_end = consume_body.index("END")
        consume_clean = consume_body[:consume_end]
        assert "##global_stock_temp" in consume_clean
        assert "DROP TABLE" not in consume_clean

    def test_p6_job_legacy_purge_disabled(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V007__sql_agent_jobs.sql").read_text(encoding="utf-8")
        no_comments = re.sub(r"--[^\n]*", "", content)
        # Search the JOB_LEGACY_PURGE sp_add_job call
        match = re.search(
            r"sp_add_job\s*@job_name\s*=\s*N'JOB_LEGACY_PURGE'\s*,\s*@enabled\s*=\s*(\d+)",
            no_comments,
        )
        assert match is not None, "JOB_LEGACY_PURGE sp_add_job not found"
        assert match.group(1) == "0"


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_export_exists(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V008__legacy_sprocs.sql").read_text(encoding="utf-8")
        assert "CREATE OR ALTER PROCEDURE dbo.usp_legacy_export" in content

    def test_s2_legacy_purge_references_missing_table(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V008__legacy_sprocs.sql").read_text(encoding="utf-8")
        assert "usp_legacy_purge" in content
        assert "legacy_archive" in content
        # Verify the legacy_artifact.sql also exists
        assert (FIXTURE_ROOT / "db/sql/legacy_artifact.sql").is_file()

    def test_s3_deprecated_test_trivial(self) -> None:
        content = (FIXTURE_ROOT / "db/test/08_deprecated_test.sql").read_text(encoding="utf-8")
        assert "1 = 0" in content or "1=0" in content


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-sql-tsql" in content

    def test_manifest_requires(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "linux" in content
        assert "macos" in content

    def test_manifest_container_enabled(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "container:" in content
        assert "enabled: true" in content

    def test_dockerfile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_dockerfile_uses_mssql_image(self) -> None:
        content = (FIXTURE_ROOT / "Dockerfile.test").read_text(encoding="utf-8")
        assert "mcr.microsoft.com/mssql/server" in content

    def test_dockerfile_installs_mssql_tools18(self) -> None:
        content = (FIXTURE_ROOT / "Dockerfile.test").read_text(encoding="utf-8")
        assert "mssql-tools18" in content

    def test_makefile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_makefile_has_test_target(self) -> None:
        content = (FIXTURE_ROOT / "Makefile").read_text(encoding="utf-8")
        assert "test:" in content

    def test_build_history_exists(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_entrypoint_exists(self) -> None:
        assert (FIXTURE_ROOT / "entrypoint.sh").is_file()

    def test_tools_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "tools").is_dir()

    def test_tools_scripts_exist(self) -> None:
        for name in ("wait_for_sql.sh", "apply_migrations.sh", "run_tests.sh", "reset_db.sh"):
            assert (FIXTURE_ROOT / "tools" / name).is_file(), f"missing tools/{name}"