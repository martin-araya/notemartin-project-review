"""Tests del ground truth de fx-sql-postgres (F06ah)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-sql-postgres"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-sql-postgres"


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
        assert "facturación" in names
        assert "auditoría" in names
        assert "multi-tenant" in names

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
        assert "postgresql" in names
        assert "flyway" in names
        assert "pg_cron" in names
        assert "pgtap" in names

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
            assert tok.startswith("NPRGT-FXSQLPG-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {".pg_data", "Generated"}
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "Makefile",
            "manifest.yml", "Dockerfile.test", "README.md",
            ".gitignore", "flyway.conf", "postgres.conf",
        }
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(p in skip_dirs for p in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".sql", ".sh", ".conf", ".md", ".txt", ".yml", ".yaml"):
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
            where = t.get("file", "")
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
# Postgres structure
# ---------------------------------------------------------------------------


class TestPostgresStructure:
    def test_db_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "db"
        assert d.is_dir()

    def test_db_migration_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "db/migration"
        assert d.is_dir()

    def test_db_seed_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "db/seed"
        assert d.is_dir()

    def test_db_test_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "db/test"
        assert d.is_dir()

    def test_db_schema_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "db/schema"
        assert d.is_dir()

    def test_db_sql_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "db/sql"
        assert d.is_dir()

    def test_v1_init_schema_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V1__init_schema.sql").is_file()

    def test_v2_audit_triggers_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V2__add_audit_triggers.sql").is_file()

    def test_v3_rls_policies_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V3__add_rls_policies.sql").is_file()

    def test_v4_dynamic_sql_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V4__add_dynamic_sql_fn.sql").is_file()

    def test_v5_repeatable_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V5__add_repeatable_migrations.sql").is_file()

    def test_r_recalc_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/R__recalc_factura_totals.sql").is_file()

    def test_v6_cascade_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V6__add_cascade_constraints.sql").is_file()

    def test_v7_pg_cron_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/migration/V7__add_pg_cron_jobs.sql").is_file()

    def test_seed_data_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/seed/seed_data.sql").is_file()

    def test_seed_audit_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/seed/seed_audit.sql").is_file()

    def test_schema_files_exist(self) -> None:
        assert (FIXTURE_ROOT / "db/schema/001_clientes.sql").is_file()
        assert (FIXTURE_ROOT / "db/schema/007_unused_indexes.sql").is_file()

    def test_pgtap_tests_exist(self) -> None:
        for i in range(1, 9):
            fname = f"db/test/{i:02d}_" + (
                "schema_test", "triggers_test", "rls_test", "dynamic_sql_test",
                "repeatable_test", "cascade_test", "pg_cron_test", "deprecated_test"
            )[i - 1] + ".sql"
            assert (FIXTURE_ROOT / fname).is_file(), f"missing {fname}"

    def test_sql_query_files_exist(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/facturas_crud.sql").is_file()
        assert (FIXTURE_ROOT / "db/sql/auditoria_query.sql").is_file()
        assert (FIXTURE_ROOT / "db/sql/tenant_isolation_query.sql").is_file()


# ---------------------------------------------------------------------------
# Migrations config
# ---------------------------------------------------------------------------


class TestMigrationsPresent:
    def test_flyway_conf_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/flyway.conf").is_file()

    def test_postgres_conf_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/postgres.conf").is_file()

    def test_flyway_locations_db_migration(self) -> None:
        content = (FIXTURE_ROOT / "config/flyway.conf").read_text(encoding="utf-8")
        assert "flyway.locations=filesystem:./db/migration" in content

    def test_postgres_shared_preload_libraries(self) -> None:
        content = (FIXTURE_ROOT / "config/postgres.conf").read_text(encoding="utf-8")
        assert "shared_preload_libraries" in content
        assert "pg_cron" in content


# ---------------------------------------------------------------------------
# PgCron configured
# ---------------------------------------------------------------------------


class TestPgCronConfigured:
    def test_dockerfile_installs_pg_cron(self) -> None:
        content = (FIXTURE_ROOT / "Dockerfile.test").read_text(encoding="utf-8")
        assert "pg_cron" in content
        assert "REL1_6_STABLE" in content

    def test_pg_cron_extension_in_v7(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V7__add_pg_cron_jobs.sql").read_text(encoding="utf-8")
        assert "pg_cron" in content
        assert "cron.schedule" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_audit_triggers(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V2__add_audit_triggers.sql").read_text(encoding="utf-8")
        assert "f_audit_factura" in content
        assert "trg_audit_facturas_insert" in content
        assert "trg_audit_facturas_delete" in content

    def test_e2_row_level_security(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V3__add_rls_policies.sql").read_text(encoding="utf-8")
        assert "ROW LEVEL SECURITY" in content
        assert "current_setting" in content
        assert "tenant_id" in content

    def test_e3_dynamic_sql(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V4__add_dynamic_sql_fn.sql").read_text(encoding="utf-8")
        assert "EXECUTE format" in content

    def test_e4_repeatable_migrations(self) -> None:
        r_path = FIXTURE_ROOT / "db/migration/R__recalc_factura_totals.sql"
        assert r_path.is_file()
        content = r_path.read_text(encoding="utf-8")
        assert "TRUNCATE" in content
        assert "INSERT" in content

    def test_e5_on_delete_cascade(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V6__add_cascade_constraints.sql").read_text(encoding="utf-8")
        assert "ON DELETE CASCADE" in content
        assert "DEFERRABLE" in content

    def test_e6_pg_cron_materialized_views(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V7__add_pg_cron_jobs.sql").read_text(encoding="utf-8")
        assert "pg_cron" in content
        assert "MATERIALIZED VIEW" in content
        assert "cron.schedule" in content


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_trigger_new_in_delete(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V2__add_audit_triggers.sql").read_text(encoding="utf-8")
        assert "NEW.id" in content
        assert "TG_OP" in content
        # Find the DELETE branch
        delete_branch_idx = content.index("ELSIF TG_OP = 'DELETE'")
        # The trap: NEW.id in DELETE branch
        delete_branch = content[delete_branch_idx:content.index("END IF", delete_branch_idx)]
        assert "NEW.id" in delete_branch

    def test_p2_rls_no_force(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V3__add_rls_policies.sql").read_text(encoding="utf-8")
        # ENABLE ROW LEVEL SECURITY is present
        assert "ENABLE ROW LEVEL SECURITY" in content
        # FORCE ROW LEVEL SECURITY is NOT present (trampa)
        assert "FORCE ROW LEVEL SECURITY" not in content

    def test_p3_dynamic_sql_no_whitelist(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V4__add_dynamic_sql_fn.sql").read_text(encoding="utf-8")
        # Strip SQL comments
        import re
        no_comments = re.sub(r"--[^\n]*", "", content)
        assert "EXECUTE format" in no_comments
        # No whitelist check
        assert "WHITELIST" not in no_comments.upper()
        assert "IF p_tabla NOT IN" not in no_comments

    def test_p4_repeatable_non_idempotent(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/R__recalc_factura_totals.sql").read_text(encoding="utf-8")
        assert "TRUNCATE" in content
        # No UPSERT
        assert "ON CONFLICT" not in content.upper()

    def test_p5_cascade_silent_delete(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V6__add_cascade_constraints.sql").read_text(encoding="utf-8")
        assert "ON DELETE CASCADE" in content
        # No trigger BEFORE DELETE
        assert "BEFORE DELETE" not in content

    def test_p6_materialized_view_no_soft_delete_filter(self) -> None:
        content = (FIXTURE_ROOT / "db/migration/V7__add_pg_cron_jobs.sql").read_text(encoding="utf-8")
        # Strip SQL comments
        import re
        no_comments = re.sub(r"--[^\n]*", "", content)
        # Find the materialized view definition
        mv_idx = no_comments.index("CREATE MATERIALIZED VIEW")
        mv_end = no_comments.index(";", mv_idx)
        mv_def = no_comments[mv_idx:mv_end]
        # The trap is the mv doesn't filter deleted_at
        assert "WHERE deleted_at IS NULL" not in mv_def


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_export_exists(self) -> None:
        # S1 trap: legacy_export.sql existe pero solo tiene SELECT 'noop'.
        # No se invoca desde ningun flujo (ni en sql/, ni en db/migration/, ni en test/).
        legacy = FIXTURE_ROOT / "db/sql/legacy_export.sql"
        assert legacy.exists(), "S1 trap: legacy_export.sql debe existir (declarado)"
        # Trampa S1: el archivo existe pero solo tiene 'SELECT noop' (no usado).
        assert "SELECT 'noop'" in legacy.read_text(encoding="utf-8")

    def test_s2_unused_indexes_exists(self) -> None:
        unused = FIXTURE_ROOT / "db/schema/007_unused_indexes.sql"
        assert unused.exists(), "S2 trap: 007_unused_indexes.sql should exist"
        content = unused.read_text(encoding="utf-8")
        assert "CREATE INDEX" in content

    def test_s3_deprecated_test_exists(self) -> None:
        deprecated = FIXTURE_ROOT / "db/test/08_deprecated_test.sql"
        assert deprecated.exists(), "S3 trap: 08_deprecated_test.sql should exist"
        content = deprecated.read_text(encoding="utf-8")
        assert "pass" in content  # pgTAP placeholder


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-sql-postgres" in content

    def test_manifest_requires(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "linux" in content

    def test_dockerfile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_makefile_has_test_target(self) -> None:
        content = (FIXTURE_ROOT / "Makefile").read_text(encoding="utf-8")
        assert "test:" in content

    def test_build_history_exists(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()