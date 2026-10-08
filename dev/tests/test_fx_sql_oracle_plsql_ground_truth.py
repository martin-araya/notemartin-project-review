"""Tests del ground truth de fx-sql-oracle-plsql (F06ai)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-sql-oracle-plsql"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-sql-oracle-plsql"


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
        assert "apertura-de-cuenta" in names
        assert "cálculo-de-intereses" in names
        assert "cierre-de-mes" in names

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
        assert "oracle-database-free" in names
        assert "liquibase" in names
        assert "pl-sql" in names
        assert "utplsql" in names

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
            assert tok.startswith("NPRGT-FXORAPL-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {".oracle_data", "Generated"}
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "Makefile",
            "manifest.yml", "Dockerfile.test", "README.md",
            ".gitignore", "liquibase.properties", "tnsnames.ora",
        }
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(p in skip_dirs for p in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".sql", ".sh", ".conf", ".md", ".txt", ".yml", ".yaml", ".xml"):
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
# Oracle structure
# ---------------------------------------------------------------------------


class TestOracleStructure:
    def test_db_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "db").is_dir()

    def test_changelog_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog").is_dir()

    def test_changelog_master_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/changelog-master.xml").is_file()

    def test_v1_init_schema_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/001-init-schema.sql").is_file()

    def test_v2_accounts_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/002-accounts-package.sql").is_file()

    def test_v3_interest_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/003-interest-package.sql").is_file()

    def test_v4_autonomous_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/004-autonomous-trigger.sql").is_file()

    def test_v5_instead_of_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/005-instead-of-trigger.sql").is_file()

    def test_v6_scheduler_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/006-scheduler-jobs.sql").is_file()

    def test_v7_db_link_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/changelog/007-db-link.sql").is_file()

    def test_packages_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "db/packages"
        assert d.is_dir()

    def test_pkg_accounts_spec_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/packages/pkg_accounts_spec.sql").is_file()

    def test_pkg_accounts_body_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/packages/pkg_accounts_body.sql").is_file()

    def test_pkg_interest_spec_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/packages/pkg_interest_spec.sql").is_file()

    def test_pkg_interest_body_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/packages/pkg_interest_body.sql").is_file()

    def test_pkg_monthly_close_spec_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/packages/pkg_monthly_close_spec.sql").is_file()

    def test_pkg_monthly_close_body_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/packages/pkg_monthly_close_body.sql").is_file()

    def test_pkg_legacy_spec_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/packages/pkg_legacy_spec.sql").is_file()

    def test_sql_synonyms_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/synonyms.sql").is_file()

    def test_sql_views_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/views.sql").is_file()

    def test_sql_legacy_synonym_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/sql/legacy_synonym.sql").is_file()

    def test_seed_data_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/seed/seed-data.sql").is_file()

    def test_seed_accounts_exists(self) -> None:
        assert (FIXTURE_ROOT / "db/seed/seed-accounts.sql").is_file()

    def test_pgtap_tests_exist(self) -> None:
        expected = [
            "01-accounts-test.sql",
            "02-interest-test.sql",
            "03-monthly-close-test.sql",
            "04-triggers-test.sql",
            "05-scheduler-test.sql",
            "06-trap-ecosystem-test.sql",
            "07-deprecated-test.sql",
        ]
        for name in expected:
            f = FIXTURE_ROOT / "db/test" / name
            assert f.is_file(), f"missing {f}"


# ---------------------------------------------------------------------------
# Liquibase configured
# ---------------------------------------------------------------------------


class TestLiquibaseConfigured:
    def test_liquibase_properties_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/liquibase.properties").is_file()

    def test_liquibase_locations_changelog(self) -> None:
        content = (FIXTURE_ROOT / "config/liquibase.properties").read_text(encoding="utf-8")
        assert "changelog-master.xml" in content

    def test_dockerfile_installs_liquibase(self) -> None:
        content = (FIXTURE_ROOT / "Dockerfile.test").read_text(encoding="utf-8")
        assert "liquibase" in content.lower()
        assert "liquibase-4.27.0" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_spec_vs_body(self) -> None:
        # E1 trap: the spec (pkg_accounts_spec.sql) NO declares private procedures.
        # The body (pkg_accounts_body.sql) declares p_internal_validate (private).
        body = (FIXTURE_ROOT / "db/packages/pkg_accounts_body.sql").read_text(encoding="utf-8")
        # Body declares p_internal_validate (E1 trap: only in body)
        assert "p_internal_validate" in body
        assert "FUNCTION p_internal_validate" in body
        # p_internal_validate is marked as the private procedure (E1 trap)
        assert "RETURN BOOLEAN" in body  # boolean return type, distinct from public functions

    def test_e2_public_synonyms(self) -> None:
        content = (FIXTURE_ROOT / "db/sql/synonyms.sql").read_text(encoding="utf-8")
        assert "CREATE OR REPLACE PUBLIC SYNONYM" in content
        assert "accounts FOR ORAFI.accounts" in content

    def test_e3_execute_immediate(self) -> None:
        content = (FIXTURE_ROOT / "db/packages/pkg_interest_body.sql").read_text(encoding="utf-8")
        assert "EXECUTE IMMEDIATE" in content

    def test_e4_autonomous_tx(self) -> None:
        content = (FIXTURE_ROOT / "db/changelog/004-autonomous-trigger.sql").read_text(encoding="utf-8")
        assert "PRAGMA AUTONOMOUS_TRANSACTION" in content

    def test_e5_instead_of(self) -> None:
        content = (FIXTURE_ROOT / "db/changelog/005-instead-of-trigger.sql").read_text(encoding="utf-8")
        assert "INSTEAD OF UPDATE" in content

    def test_e6_scheduler_and_db_links(self) -> None:
        scheduler = (FIXTURE_ROOT / "db/changelog/006-scheduler-jobs.sql").read_text(encoding="utf-8")
        assert "DBMS_SCHEDULER.CREATE_JOB" in scheduler
        db_link = (FIXTURE_ROOT / "db/changelog/007-db-link.sql").read_text(encoding="utf-8")
        assert "CREATE DATABASE LINK" in db_link


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_autonomous_no_others(self) -> None:
        content = (FIXTURE_ROOT / "db/packages/pkg_accounts_body.sql").read_text(encoding="utf-8")
        # Strip SQL comments
        import re
        no_comments = re.sub(r"--[^\n]*", "", content)
        assert "PRAGMA AUTONOMOUS_TRANSACTION" in no_comments
        assert "WHEN OTHERS" not in no_comments.upper()

    def test_p2_synonym_invalid_table(self) -> None:
        content = (FIXTURE_ROOT / "db/sql/synonyms.sql").read_text(encoding="utf-8")
        assert "legacy_table FOR ORAFI" in content
        # Verify the target does NOT exist in the schema (it's a trap)
        assert "legacy_does_not_exist" in content

    def test_p3_dynamic_sql_unsafe(self) -> None:
        content = (FIXTURE_ROOT / "db/packages/pkg_interest_body.sql").read_text(encoding="utf-8")
        assert "EXECUTE IMMEDIATE" in content
        assert "calculate_for_table" in content
        # No whitelist
        assert "WHITELIST" not in content.upper()

    def test_p4_trigger_no_others_handler(self) -> None:
        # Strip SQL comments for clean check
        import re
        content = (FIXTURE_ROOT / "db/changelog/004-autonomous-trigger.sql").read_text(encoding="utf-8")
        no_comments = re.sub(r"--[^\n]*", "", content)
        assert "BEGIN" in no_comments
        # No EXCEPTION WHEN OTHERS between BEGIN and END
        no_comments_upper = no_comments.upper()
        assert "WHEN OTHERS" not in no_comments_upper

    def test_p5_instead_of_missing_column(self) -> None:
        content = (FIXTURE_ROOT / "db/changelog/005-instead-of-trigger.sql").read_text(encoding="utf-8")
        # Update statement should NOT include opened_at
        update_section_start = content.index("UPDATE accounts")
        update_section_end = content.index(";", update_section_start)
        update_sql = content[update_section_start:update_section_end]
        # Trampa P5: opened_at is missing from the UPDATE
        assert "opened_at" not in update_sql

    def test_p6_scheduler_job_disabled(self) -> None:
        content = (FIXTURE_ROOT / "db/changelog/006-scheduler-jobs.sql").read_text(encoding="utf-8")
        assert "DBMS_SCHEDULER.CREATE_JOB" in content
        # Verify that JOB_MONTHLY_CLOSE_AUTOMATION has enabled => FALSE
        # Find the JOB_MONTHLY block specifically
        import re
        match = re.search(
            r"job_name\s+=>\s*'JOB_MONTHLY_CLOSE_AUTOMATION'.*?enabled\s+=>\s+(\w+)",
            content,
            re.DOTALL,
        )
        assert match is not None, "JOB_MONTHLY_CLOSE_AUTOMATION block not found"
        assert match.group(1).upper() == "FALSE"


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_package_exists(self) -> None:
        legacy = FIXTURE_ROOT / "db/packages/pkg_legacy_spec.sql"
        assert legacy.exists()

    def test_s2_legacy_synonym_exists(self) -> None:
        legacy = FIXTURE_ROOT / "db/sql/legacy_synonym.sql"
        assert legacy.exists()

    def test_s3_deprecated_test_exists(self) -> None:
        deprecated = FIXTURE_ROOT / "db/test/07-deprecated-test.sql"
        assert deprecated.exists()


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-sql-oracle-plsql" in content

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