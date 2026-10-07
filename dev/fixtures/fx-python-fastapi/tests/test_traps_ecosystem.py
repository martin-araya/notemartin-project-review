"""Tests for the 6 ecosystem traps planted in the fixture."""
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


def test_e01_depends_with_yield_chains():
    deps = (FIXTURE_ROOT / "app/dependencies.py").read_text(encoding="utf-8")
    assert "async def get_db" in deps
    assert "yield" in deps
    assert "Depends(get_db)" in deps
    assert "Depends(get_current_user)" in deps


def test_e02_pydantic_validators_with_business_logic():
    user_schema = (FIXTURE_ROOT / "app/schemas/user.py").read_text(encoding="utf-8")
    sub_schema = (FIXTURE_ROOT / "app/schemas/subscription.py").read_text(encoding="utf-8")
    assert "@field_validator" in user_schema
    assert "@model_validator" in sub_schema


def test_e03_include_router_with_prefix_and_dependencies():
    users = (FIXTURE_ROOT / "app/routers/users.py").read_text(encoding="utf-8")
    subs = (FIXTURE_ROOT / "app/routers/subscriptions.py").read_text(encoding="utf-8")
    webhooks = (FIXTURE_ROOT / "app/routers/webhooks.py").read_text(encoding="utf-8")
    assert "prefix=\"/users\"" in users
    assert "dependencies=[Depends(get_current_user)]" in users
    assert "prefix=\"/subscriptions\"" in subs
    assert "dependencies=[Depends(get_active_subscription)]" in subs
    assert "prefix=\"/webhooks\"" in webhooks
    # webhooks router NO tiene dependencies= (es publico).
    assert "prefix=\"/webhooks\"" in webhooks and "dependencies=[Depends" not in webhooks.split("router = APIRouter")[1].split(")")[0]


def test_e04_lifespan_events():
    main = (FIXTURE_ROOT / "app/main.py").read_text(encoding="utf-8")
    assert "asynccontextmanager" in main
    assert "async def lifespan" in main
    assert "lifespan=lifespan" in main


def test_e05_custom_decorator_registers_routes():
    decorators = (FIXTURE_ROOT / "app/decorators.py").read_text(encoding="utf-8")
    assert "def track_request" in decorators
    assert "_REGISTERED_ROUTES" in decorators
    assert "_REQUEST_REGISTRY" in decorators


def test_e06_alembic_data_migration():
    migration = (FIXTURE_ROOT / "alembic/versions/002_seed_data.py").read_text(encoding="utf-8")
    assert "op.execute" in migration
    assert "INSERT INTO" in migration