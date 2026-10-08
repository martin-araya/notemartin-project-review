"""Tests del ground truth de fx-python-ml (F06al)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-python-ml"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-python-ml"


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
        assert "entrenamiento" in names
        assert "evaluacion" in names
        assert "inferencia" in names

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
        assert "scikit-learn" in names
        assert "hydra-core" in names
        assert "dvc" in names
        assert "mlflow" in names
        assert "fastapi" in names

    def test_entry_points_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("entry_points", [])) >= 30

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
            assert tok.startswith("NPRGT-FXPML-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {".dvc", "mlruns", "mlartifacts", "__pycache__", ".pytest_cache", ".ipynb_checkpoints"}
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "Makefile",
            "manifest.yml", "Dockerfile.test", "README.md",
            ".gitignore", "entrypoint.sh", "requirements.txt",
            "pyproject.toml", "pytest.ini",
        }
        skip_ext = (".pyc", ".pkl", ".duckdb", ".csv", ".json", ".log")
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
            if path.suffix not in (".sql", ".sh", ".py", ".yml", ".yaml", ".md", ".txt", ".ipynb"):
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
# Python ML structure
# ---------------------------------------------------------------------------


class TestPythonMlStructure:
    def test_data_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "data").is_dir()

    def test_iris_csv_exists(self) -> None:
        assert (FIXTURE_ROOT / "data/iris.csv").is_file()

    def test_conf_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf").is_dir()

    def test_conf_config_yaml_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/config.yaml").is_file()

    def test_conf_entrenamiento_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/entrenamiento").is_dir()

    def test_conf_evaluacion_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/evaluacion").is_dir()

    def test_conf_inferencia_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/inferencia").is_dir()

    def test_conf_entrenamiento_default_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/entrenamiento/default.yaml").is_file()

    def test_conf_entrenamiento_rf_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/entrenamiento/random_forest.yaml").is_file()

    def test_conf_evaluacion_default_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/evaluacion/default.yaml").is_file()

    def test_conf_evaluacion_f1_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/evaluacion/f1.yaml").is_file()

    def test_conf_inferencia_default_exists(self) -> None:
        assert (FIXTURE_ROOT / "conf/inferencia/default.yaml").is_file()

    def test_notebooks_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "notebooks").is_dir()

    def test_notebooks_core_exist(self) -> None:
        for nb in ('00_setup.ipynb', '01_exploratorio.ipynb', '02_features.ipynb',
                    '03_entrenamiento.ipynb', '04_evaluacion.ipynb', '05_inferencia.ipynb'):
            assert (FIXTURE_ROOT / 'notebooks' / nb).is_file(), f'missing {nb}'

    def test_notebook_traps_exist(self) -> None:
        assert (FIXTURE_ROOT / 'notebooks' / '04_evaluacion_legacy.ipynb').is_file()
        assert (FIXTURE_ROOT / 'notebooks' / '06_setup_with_delete.ipynb').is_file()

    def test_src_init_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/__init__.py").is_file()

    def test_src_config_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/config.py").is_file()

    def test_src_features_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/features.py").is_file()

    def test_src_train_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/train.py").is_file()

    def test_src_evaluate_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/evaluate.py").is_file()

    def test_src_register_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/register.py").is_file()

    def test_src_legacy_train_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/legacy_train.py").is_file()

    def test_src_app_init_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/app/__init__.py").is_file()

    def test_src_app_main_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/app/main.py").is_file()

    def test_dvc_yaml_exists(self) -> None:
        assert (FIXTURE_ROOT / "dvc.yaml").is_file()

    def test_params_yaml_exists(self) -> None:
        assert (FIXTURE_ROOT / "params.yaml").is_file()

    def test_tests_dir_exists(self) -> None:
        assert (FIXTURE_ROOT / "tests").is_dir()

    def test_test_files_exist(self) -> None:
        expected = [
            "conftest.py",
            "test_train.py",
            "test_evaluate.py",
            "test_inference.py",
            "test_hydra_config.py",
            "test_dvc_pipeline.py",
            "test_mlflow_registry.py",
            "test_reproducibility.py",
            "test_features_divergence.py",
            "test_traps_ecosystem.py",
            "test_traps_package.py",
            "test_traps_superficial.py",
            "test_deprecated.py",
        ]
        for name in expected:
            f = FIXTURE_ROOT / "tests" / name
            assert f.is_file(), f"missing tests/{name}"


# ---------------------------------------------------------------------------
# Models present
# ---------------------------------------------------------------------------


class TestModelsPresent:
    def test_notebooks_have_8_files(self) -> None:
        nbs = list((FIXTURE_ROOT / "notebooks").glob("*.ipynb"))
        assert len(nbs) >= 6, f"expected >=6 notebooks, got {len(nbs)}"

    def test_conf_subdirs_exist(self) -> None:
        for sub in ("entrenamiento", "evaluacion", "inferencia"):
            assert (FIXTURE_ROOT / "conf" / sub).is_dir(), f"missing conf/{sub}"


# ---------------------------------------------------------------------------
# DVC configured
# ---------------------------------------------------------------------------


class TestDvcConfigured:
    def test_dvc_yaml_has_stages(self) -> None:
        content = (FIXTURE_ROOT / "dvc.yaml").read_text(encoding="utf-8")
        assert "stages:" in content
        assert "train:" in content
        assert "evaluate:" in content
        assert "register:" in content

    def test_dvc_yaml_has_deps_and_outs(self) -> None:
        content = (FIXTURE_ROOT / "dvc.yaml").read_text(encoding="utf-8")
        assert "deps:" in content
        assert "outs:" in content
        assert "metrics:" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_notebooks_in_order(self) -> None:
        notebooks = sorted((FIXTURE_ROOT / "notebooks").glob("*.ipynb"))
        assert len(notebooks) >= 6
        for nb in notebooks:
            assert nb.name[0].isdigit(), f"notebook {nb.name} sin prefijo numerico"

    def test_e2_hydra_compose(self) -> None:
        content = (FIXTURE_ROOT / "conf/config.yaml").read_text(encoding="utf-8")
        assert "@package" in content or "_global_" in content
        assert "defaults:" in content

    def test_e2_hydra_subconfigs(self) -> None:
        for sub in ['entrenamiento/default.yaml', 'entrenamiento/random_forest.yaml',
                    'evaluacion/default.yaml', 'evaluacion/f1.yaml', 'inferencia/default.yaml']:
            assert (FIXTURE_ROOT / 'conf' / sub).is_file()

    def test_e3_dvc_yaml_stages(self) -> None:
        content = (FIXTURE_ROOT / "dvc.yaml").read_text(encoding="utf-8")
        assert "stages:" in content
        assert "train:" in content
        assert "evaluate:" in content
        assert "register:" in content

    def test_e4_mlflow_iris_clf_name(self) -> None:
        nb_content = (FIXTURE_ROOT / "notebooks/03_entrenamiento.ipynb").read_text(encoding="utf-8")
        assert "iris_clf" in nb_content
        config_content = (FIXTURE_ROOT / "conf/inferencia/default.yaml").read_text(encoding="utf-8")
        assert "iris_clf" in config_content

    def test_e5_feature_engineering_duplicated(self) -> None:
        src = (FIXTURE_ROOT / "src/features.py").read_text(encoding="utf-8")
        nb = (FIXTURE_ROOT / "notebooks/02_features.ipynb").read_text(encoding="utf-8")
        assert "StandardScaler" in src
        assert "MinMaxScaler" in nb

    def test_e6_random_state(self) -> None:
        content = (FIXTURE_ROOT / "src/train.py").read_text(encoding="utf-8")
        assert "random_state" in content


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_delete_state_notebook(self) -> None:
        content = (FIXTURE_ROOT / "notebooks/06_setup_with_delete.ipynb").read_text(encoding="utf-8")
        assert "del df" in content

    def test_p2_hydra_config_exists(self) -> None:
        """P2 trap: el override puede apuntar a un config que no existe (smoke test)."""
        assert (FIXTURE_ROOT / "conf/entrenamiento/default.yaml").is_file()

    def test_p3_dvc_register_stage(self) -> None:
        content = (FIXTURE_ROOT / "dvc.yaml").read_text(encoding="utf-8")
        assert "register:" in content
        assert "outs:" in content

    def test_p4_legacy_notebook_wrong_name(self) -> None:
        content = (FIXTURE_ROOT / "notebooks/04_evaluacion_legacy.ipynb").read_text(encoding="utf-8")
        assert "iris_classifier_legacy" in content

    def test_p5_features_divergence(self) -> None:
        src = (FIXTURE_ROOT / "src/features.py").read_text(encoding="utf-8")
        nb = (FIXTURE_ROOT / "notebooks/02_features.ipynb").read_text(encoding="utf-8")
        assert "StandardScaler" in src
        assert "MinMaxScaler" in nb
        assert "StandardScaler" not in nb

    def test_p6_legacy_train_no_random_state(self) -> None:
        content = (FIXTURE_ROOT / "src/legacy_train.py").read_text(encoding="utf-8")
        assert "def legacy_train" in content
        assert "random_state" not in content


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_train_module_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/legacy_train.py").is_file()

    def test_s2_setup_notebook_only_imports(self) -> None:
        content = (FIXTURE_ROOT / "notebooks/00_setup.ipynb").read_text(encoding="utf-8")
        assert "engineer_features" not in content
        assert "train_model" not in content

    def test_s3_deprecated_test_uses_pytest_skip(self) -> None:
        content = (FIXTURE_ROOT / "tests/test_deprecated.py").read_text(encoding="utf-8")
        # Acepta tanto `pytest.skip(...)` como `@pytest.mark.skip(...)`
        assert ("pytest.skip(" in content) or ("@pytest.mark.skip" in content)


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-python-ml" in content

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

    def test_dockerfile_installs_deps(self) -> None:
        content = (FIXTURE_ROOT / "Dockerfile.test").read_text(encoding="utf-8")
        assert "pip install" in content
        assert "dvc init" in content or "dvc" in content

    def test_makefile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_makefile_has_test_target(self) -> None:
        content = (FIXTURE_ROOT / "Makefile").read_text(encoding="utf-8")
        assert "test:" in content

    def test_build_history_exists(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_entrypoint_exists(self) -> None:
        assert (FIXTURE_ROOT / "entrypoint.sh").is_file()

    def test_requirements_txt_exists(self) -> None:
        assert (FIXTURE_ROOT / "requirements.txt").is_file()

    def test_requirements_has_scikit_learn(self) -> None:
        content = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "scikit-learn" in content

    def test_requirements_has_mlflow(self) -> None:
        content = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "mlflow" in content

    def test_requirements_has_dvc(self) -> None:
        content = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "dvc" in content

    def test_requirements_has_fastapi(self) -> None:
        content = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "fastapi" in content

    def test_requirements_has_hydra(self) -> None:
        content = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "hydra" in content

    def test_requirements_has_nbval(self) -> None:
        content = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "nbval" in content