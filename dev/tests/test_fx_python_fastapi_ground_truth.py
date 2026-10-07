"""Tests del ground truth de fx-python-fastapi (F06q)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-python-fastapi"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-python-fastapi"


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
        assert "usuarios" in names
        assert "suscripciones" in names
        assert "webhooks" in names

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
        assert "fastapi" in names
        assert "pydantic" in names
        assert "sqlalchemy" in names
        assert "alembic" in names
        assert "celery" in names

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
            assert tok.startswith("NPRGT-FXFAST-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"__pycache__", "node_modules", "dist", ".git", ".pytest_cache", "alembic"}
        skip_files = {"unique_tokens.txt", "pytest.ini", "pyproject.toml",
                      "requirements.txt", "alembic.ini", "conftest.py"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".py", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".ini", ".toml", ".mako"):
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


class TestFastapiStructure:
    def test_main_py(self) -> None:
        assert (FIXTURE_ROOT / "app/main.py").is_file()

    def test_config(self) -> None:
        assert (FIXTURE_ROOT / "app/config.py").is_file()

    def test_database(self) -> None:
        assert (FIXTURE_ROOT / "app/database.py").is_file()

    def test_dependencies(self) -> None:
        assert (FIXTURE_ROOT / "app/dependencies.py").is_file()

    def test_celery_app(self) -> None:
        assert (FIXTURE_ROOT / "app/celery_app.py").is_file()

    def test_decorators(self) -> None:
        assert (FIXTURE_ROOT / "app/decorators.py").is_file()

    def test_models(self) -> None:
        for f in ("user.py", "subscription.py", "webhook.py"):
            assert (FIXTURE_ROOT / "app/models" / f).is_file(), f"missing {f}"

    def test_schemas(self) -> None:
        for f in ("user.py", "subscription.py", "webhook.py"):
            assert (FIXTURE_ROOT / "app/schemas" / f).is_file(), f"missing {f}"

    def test_routers(self) -> None:
        for f in ("users.py", "subscriptions.py", "webhooks.py"):
            assert (FIXTURE_ROOT / "app/routers" / f).is_file(), f"missing {f}"

    def test_services(self) -> None:
        for f in ("user_service.py", "subscription_service.py", "webhook_service.py"):
            assert (FIXTURE_ROOT / "app/services" / f).is_file(), f"missing {f}"

    def test_alembic_env(self) -> None:
        assert (FIXTURE_ROOT / "alembic/env.py").is_file()

    def test_alembic_migrations(self) -> None:
        for f in ("001_initial.py", "002_seed_data.py"):
            assert (FIXTURE_ROOT / "alembic/versions" / f).is_file(), f"missing {f}"

    def test_tests_dir(self) -> None:
        assert (FIXTURE_ROOT / "tests").is_dir()


class TestEcosystemTraps:
    def test_e01_depends_with_yield_chains(self) -> None:
        deps = (FIXTURE_ROOT / "app/dependencies.py").read_text(encoding="utf-8")
        assert "async def get_db" in deps
        assert "yield" in deps
        assert "Depends(get_db)" in deps
        assert "Depends(get_current_user)" in deps

    def test_e02_pydantic_validators_with_business_logic(self) -> None:
        user_schema = (FIXTURE_ROOT / "app/schemas/user.py").read_text(encoding="utf-8")
        sub_schema = (FIXTURE_ROOT / "app/schemas/subscription.py").read_text(encoding="utf-8")
        assert "@field_validator" in user_schema
        assert "@model_validator" in sub_schema

    def test_e03_include_router_with_prefix_and_dependencies(self) -> None:
        users = (FIXTURE_ROOT / "app/routers/users.py").read_text(encoding="utf-8")
        subs = (FIXTURE_ROOT / "app/routers/subscriptions.py").read_text(encoding="utf-8")
        webhooks = (FIXTURE_ROOT / "app/routers/webhooks.py").read_text(encoding="utf-8")
        assert "prefix=\"/users\"" in users
        assert "dependencies=[Depends(get_current_user)]" in users
        assert "prefix=\"/subscriptions\"" in subs
        assert "dependencies=[Depends(get_active_subscription)]" in subs
        assert "prefix=\"/webhooks\"" in webhooks

    def test_e04_lifespan_events(self) -> None:
        main = (FIXTURE_ROOT / "app/main.py").read_text(encoding="utf-8")
        assert "asynccontextmanager" in main
        assert "async def lifespan" in main
        assert "lifespan=lifespan" in main

    def test_e05_custom_decorator_registers_routes(self) -> None:
        decorators = (FIXTURE_ROOT / "app/decorators.py").read_text(encoding="utf-8")
        assert "def track_request" in decorators
        assert "_REGISTERED_ROUTES" in decorators
        assert "_REQUEST_REGISTRY" in decorators

    def test_e06_alembic_data_migration(self) -> None:
        migration = (FIXTURE_ROOT / "alembic/versions/002_seed_data.py").read_text(encoding="utf-8")
        assert "op.execute" in migration
        assert "INSERT INTO" in migration


class TestPackageTraps:
    def test_p01_pydantic_validator_race(self) -> None:
        user_schema = (FIXTURE_ROOT / "app/schemas/user.py").read_text(encoding="utf-8")
        assert "@field_validator" in user_schema
        assert "lower" in user_schema
        assert "FOR UPDATE" not in user_schema
        assert "select_for_update" not in user_schema

    def test_p02_yield_dep_no_rollback_on_error(self) -> None:
        deps = (FIXTURE_ROOT / "app/dependencies.py").read_text(encoding="utf-8")
        bloque_get_db = deps[deps.index("async def get_db"):deps.index("async def get_current_user")]
        assert "yield" in bloque_get_db
        assert "rollback" not in bloque_get_db.lower()

    def test_p03_include_router_order_shadows(self) -> None:
        main = (FIXTURE_ROOT / "app/main.py").read_text(encoding="utf-8")
        idx_users = main.index("users.router")
        idx_subs = main.index("subscriptions.router")
        idx_hooks = main.index("webhooks.router")
        assert idx_users < idx_subs < idx_hooks

    def test_p04_lifespan_exception_swallowed(self) -> None:
        main = (FIXTURE_ROOT / "app/main.py").read_text(encoding="utf-8")
        bloque_startup = main[main.index("try:"):main.index("yield")]
        assert "init_db()" in bloque_startup
        assert "except Exception" in bloque_startup

    def test_p05_custom_decorator_breaks_signature(self) -> None:
        decorators = (FIXTURE_ROOT / "app/decorators.py").read_text(encoding="utf-8")
        assert "functools.wraps" not in decorators

    def test_p06_celery_eager_in_async_context(self) -> None:
        tasks = (FIXTURE_ROOT / "app/tasks/webhook_tasks.py").read_text(encoding="utf-8")
        assert "async def dispatch_webhook_event" in tasks
        assert "@shared_task" in tasks


class TestSuperficialTraps:
    def test_s01_dead_debug_endpoint(self) -> None:
        webhooks = (FIXTURE_ROOT / "app/routers/webhooks.py").read_text(encoding="utf-8")
        assert "debug_webhooks" in webhooks

    def test_s02_dead_pydantic_model(self) -> None:
        legacy = (FIXTURE_ROOT / "app/schemas/legacy.py").read_text(encoding="utf-8")
        assert "class LegacyUsuarioSchema" in legacy

    def test_s03_dead_dependency(self) -> None:
        deps = (FIXTURE_ROOT / "app/dependencies.py").read_text(encoding="utf-8")
        assert "async def get_optional_user" in deps
        for router_file in ("users.py", "subscriptions.py", "webhooks.py"):
            router_text = (FIXTURE_ROOT / "app/routers" / router_file).read_text(encoding="utf-8")
            assert "get_optional_user" not in router_text


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-python-fastapi" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_requirements_has_fastapi(self) -> None:
        requirements = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "fastapi" in requirements
        assert "pydantic" in requirements
        assert "sqlalchemy" in requirements
        assert "alembic" in requirements
        assert "celery" in requirements

    def test_pytest_ini_has_asyncio_mode(self) -> None:
        ini = (FIXTURE_ROOT / "pytest.ini").read_text(encoding="utf-8")
        assert "asyncio_mode" in ini

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25
        for tok in tokens:
            assert tok.startswith("NPRGT-FXFAST-")