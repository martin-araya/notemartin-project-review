"""Tests del ground truth de fx-dbt-airflow (F06ak)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-dbt-airflow"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-dbt-airflow"


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
        assert "ventas" in names
        assert "clientes" in names
        assert "metricas" in names

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
        assert "dbt-core" in names
        assert "dbt-duckdb" in names
        assert "apache-airflow" in names
        assert "duckdb" in names

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
            assert tok.startswith("NPRGT-FXDBAIR-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {".duckdb", "Generated", "dbt_packages", "target", "logs", ".airflow", ".pytest"}
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "Makefile",
            "manifest.yml", "Dockerfile.test", "README.md",
            ".gitignore", "entrypoint.sh", "requirements.txt",
            ".airflowignore", "profiles.yml", ".dockerignore",
        }
        skip_ext = (".pyc",)
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(p in skip_dirs for p in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix in skip_ext:
                continue
            if path.suffix not in (".sql", ".sh", ".py", ".yml", ".yaml", ".md", ".txt", ".csv"):
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
            f = ep.get("file", "")
            if not f:
                continue
            cite = f if ":" in f else f"{f}:1"
            errs = check_cite(FIXTURE_ROOT, cite)
            if errs:
                errors.append(f"entry_point {ep['id']}: {errs}")
        if errors:
            pytest.fail("\n".join(errors[:10]))


# ---------------------------------------------------------------------------
# dbt + Airflow structure
# ---------------------------------------------------------------------------


class TestDbtAirflowStructure:
    def test_dbt_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt").is_dir()

    def test_dbt_project_yml_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/dbt_project.yml").is_file()

    def test_dbt_packages_yml_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/packages.yml").is_file()

    def test_dbt_sources_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/staging/_sources.yml").is_file()

    def test_dbt_stg_ventas_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/staging/stg_ventas.sql").is_file()

    def test_dbt_stg_clientes_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/staging/stg_clientes.sql").is_file()

    def test_dbt_int_ventas_clientes_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/intermediate/int_ventas_clientes.sql").is_file()

    def test_dbt_ventas_diarias_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/marts/marts_ventas/ventas_diarias.sql").is_file()

    def test_dbt_ventas_mensuales_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/marts/marts_ventas/ventas_mensuales.sql").is_file()

    def test_dbt_clientes_top_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/marts/marts_clientes/clientes_top.sql").is_file()

    def test_dbt_metricas_diarias_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/marts/marts_metricas/metricas_diarias.sql").is_file()

    def test_dbt_ventas_diarias_incremental_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/marts/marts_incremental/ventas_diarias_incremental.sql").is_file()

    def test_dbt_ventas_diarias_incremental_buggy_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/marts/marts_incremental/ventas_diarias_incremental_buggy.sql").is_file()

    def test_dbt_macro_centros_normalizados_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/macros/centros_normalizados.sql").is_file()

    def test_dbt_macro_centros_concat_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/macros/centros_concat.sql").is_file()

    def test_dbt_macro_legacy_helper_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/macros/legacy_helper.sql").is_file()

    def test_dbt_seed_clientes_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/seeds/seed_clientes.csv").is_file()

    def test_dbt_seed_catalogo_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/seeds/seed_catalogo.csv").is_file()

    def test_dbt_seed_cliente_venta_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/seeds/seed_cliente_venta.csv").is_file()

    def test_dbt_ventas_raw_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/seeds/ventas_raw.csv").is_file()

    def test_dbt_singular_assert_ventas_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/tests/singular/assert_ventas_positivas.sql").is_file()

    def test_dbt_singular_assert_clientes_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/tests/singular/assert_clientes_activos.sql").is_file()

    def test_dbt_generic_freshness_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/tests/generic/freshness_24h.sql").is_file()

    def test_dbt_snapshots_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/snapshots/snap_ventas.sql").is_file()

    def test_airflow_dags_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/dags").is_dir()

    def test_airflow_etl_dag_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/dags/etl_dag.py").is_file()

    def test_airflow_dag_factory_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/dags/dag_factory.py").is_file()

    def test_airflow_etl_config_yaml_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/dags/etl_config.yaml").is_file()

    def test_airflow_generated_etl_dag_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/dags/generated_etl_dag.py").is_file()

    def test_airflow_transform_xcom_implicit_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/dags/transform_xcom_implicit.py").is_file()

    def test_airflow_legacy_purge_dag_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/legacy_purge_dag.py").is_file()

    def test_airflow_tests_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/tests").is_dir()

    def test_airflow_tests_files_exist(self) -> None:
        expected = [
            "conftest.py",
            "test_etl_dag.py",
            "test_dag_factory.py",
            "test_xcom_explicit.py",
            "test_xcom_implicit.py",
            "test_traps_ecosystem.py",
            "test_traps_package.py",
            "test_deprecated.py",
        ]
        for name in expected:
            f = FIXTURE_ROOT / "airflow/tests" / name
            assert f.is_file(), f"missing airflow/tests/{name}"


# ---------------------------------------------------------------------------
# Models present
# ---------------------------------------------------------------------------


class TestModelsPresent:
    def test_staging_intermediate_marts_subdirs_exist(self) -> None:
        for sub in ("staging", "intermediate", "marts"):
            assert (FIXTURE_ROOT / "dbt/models" / sub).is_dir(), f"missing models/{sub}"

    def test_marts_incremental_subdir_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/models/marts/marts_incremental").is_dir()
        buggy = FIXTURE_ROOT / "dbt/models/marts/marts_incremental/ventas_diarias_incremental_buggy.sql"
        assert buggy.is_file()


# ---------------------------------------------------------------------------
# DAG configured
# ---------------------------------------------------------------------------


class TestDagConfigured:
    def test_etl_dag_contains_dag_keyword(self) -> None:
        content = (FIXTURE_ROOT / "airflow/dags/etl_dag.py").read_text(encoding="utf-8")
        assert "DAG(" in content
        assert "xcom_push" in content
        assert "xcom_pull" in content

    def test_dag_factory_contains_yaml_safe_load(self) -> None:
        content = (FIXTURE_ROOT / "airflow/dags/dag_factory.py").read_text(encoding="utf-8")
        assert "yaml.safe_load" in content
        assert "BashOperator" in content
        assert "PythonOperator" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_ref_source(self) -> None:
        content = (FIXTURE_ROOT / "dbt/models/staging/stg_ventas.sql").read_text(encoding="utf-8")
        assert "{{ source(" in content
        content = (FIXTURE_ROOT / "dbt/models/intermediate/int_ventas_clientes.sql").read_text(encoding="utf-8")
        assert "{{ ref(" in content

    def test_e2_jinja_macros(self) -> None:
        content = (FIXTURE_ROOT / "dbt/macros/centros_normalizados.sql").read_text(encoding="utf-8")
        assert "{% macro" in content or "{%- macro" in content
        assert "{{ estado }}" in content

    def test_e3_is_incremental(self) -> None:
        content = (FIXTURE_ROOT / "dbt/models/marts/marts_incremental/ventas_diarias_incremental.sql").read_text(encoding="utf-8")
        assert "is_incremental()" in content
        assert "occurred_at >" in content

    def test_e4_materialization_per_folder(self) -> None:
        content = (FIXTURE_ROOT / "dbt/dbt_project.yml").read_text(encoding="utf-8")
        assert "+materialized: view" in content
        assert "+materialized: table" in content
        assert "+materialized: incremental" in content

    def test_e5_dag_factory_from_yaml(self) -> None:
        content = (FIXTURE_ROOT / "airflow/dags/dag_factory.py").read_text(encoding="utf-8")
        assert "yaml.safe_load" in content
        yaml_content = (FIXTURE_ROOT / "airflow/dags/etl_config.yaml").read_text(encoding="utf-8")
        assert "dag_id:" in yaml_content
        assert "tasks:" in yaml_content

    def test_e6_xcom_explicit(self) -> None:
        content = (FIXTURE_ROOT / "airflow/dags/etl_dag.py").read_text(encoding="utf-8")
        assert "xcom_push" in content
        assert "xcom_pull" in content


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_concat_macro_sqli(self) -> None:
        content = (FIXTURE_ROOT / "dbt/macros/centros_concat.sql").read_text(encoding="utf-8")
        assert "~" in content

    def test_p2_is_incremental_no_where(self) -> None:
        content = (FIXTURE_ROOT / "dbt/models/marts/marts_incremental/ventas_diarias_incremental_buggy.sql").read_text(encoding="utf-8")
        assert "is_incremental()" in content
        assert "where 1=1" in content

    def test_p3_dead_macro_helper(self) -> None:
        # legacy_helper existe en macros/ pero no se invoca en ningun modelo
        # Construir concatenacion excluyendo el archivo de definicion del macro.
        body_without_def = ""
        for path in (FIXTURE_ROOT / "dbt").rglob("*.sql"):
            if "dbt_packages" in path.parts or "target" in path.parts or "logs" in path.parts:
                continue
            if path.name == "legacy_helper.sql":
                continue
            body_without_def += path.read_text(encoding="utf-8", errors="replace")
        # legacy_helper is referenced ONLY inside its own definition file
        assert "legacy_helper" not in body_without_def

    def test_p4_materialization_inconsistency(self) -> None:
        content = (FIXTURE_ROOT / "dbt/dbt_project.yml").read_text(encoding="utf-8")
        assert "marts_incremental" in content
        assert "+unique_key:" in content

    def test_p5_legacy_purge_disabled(self) -> None:
        content = (FIXTURE_ROOT / "airflow/legacy_purge_dag.py").read_text(encoding="utf-8")
        assert "catchup=False" in content
        assert "start_date=datetime(2019" in content

    def test_p6_xcom_implicit_return_dict(self) -> None:
        content = (FIXTURE_ROOT / "airflow/dags/transform_xcom_implicit.py").read_text(encoding="utf-8")
        assert "return {" in content
        assert "xcom_push" not in content


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_helper_exists(self) -> None:
        assert (FIXTURE_ROOT / "dbt/macros/legacy_helper.sql").is_file()

    def test_s2_legacy_purge_dag_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/legacy_purge_dag.py").is_file()

    def test_s3_deprecated_test_exists(self) -> None:
        assert (FIXTURE_ROOT / "airflow/tests/test_deprecated.py").is_file()


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-dbt-airflow" in content

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

    def test_dockerfile_uses_python_slim(self) -> None:
        content = (FIXTURE_ROOT / "Dockerfile.test").read_text(encoding="utf-8")
        assert "python:3.11-slim" in content

    def test_dockerfile_installs_dbt_and_airflow(self) -> None:
        content = (FIXTURE_ROOT / "Dockerfile.test").read_text(encoding="utf-8")
        assert "dbt-core" in content or "dbt-duckdb" in content
        assert "apache-airflow" in content

    def test_makefile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_makefile_has_test_target(self) -> None:
        content = (FIXTURE_ROOT / "Makefile").read_text(encoding="utf-8")
        assert "test:" in content

    def test_build_history_exists(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_entrypoint_exists(self) -> None:
        assert (FIXTURE_ROOT / "entrypoint.sh").is_file()

    def test_profiles_yml_exists(self) -> None:
        assert (FIXTURE_ROOT / "profiles.yml").is_file()

    def test_airflowignore_exists(self) -> None:
        assert (FIXTURE_ROOT / ".airflowignore").is_file()

    def test_requirements_txt_exists(self) -> None:
        assert (FIXTURE_ROOT / "requirements.txt").is_file()

    def test_tools_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "tools").is_dir()

    def test_tools_scripts_exist(self) -> None:
        for name in ("run_dbt.sh", "run_airflow_tests.sh", "reset_workspace.sh", "wait_for_duckdb.sh"):
            assert (FIXTURE_ROOT / "tools" / name).is_file(), f"missing tools/{name}"