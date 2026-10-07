"""Tests for the 3 superficial traps planted in the fixture."""
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


def test_s01_dead_debug_endpoint():
    webhooks = (FIXTURE_ROOT / "app/routers/webhooks.py").read_text(encoding="utf-8")
    assert 'MapGet' not in webhooks  # only FastAPI router used here
    assert "debug_webhooks" in webhooks


def test_s02_dead_pydantic_model():
    legacy = (FIXTURE_ROOT / "app/schemas/legacy.py").read_text(encoding="utf-8")
    assert "class LegacyUsuarioSchema" in legacy


def test_s03_dead_dependency():
    deps = (FIXTURE_ROOT / "app/dependencies.py").read_text(encoding="utf-8")
    assert "async def get_optional_user" in deps
    # Asegurar que no se usa en ningun router.
    for router_file in ("users.py", "subscriptions.py", "webhooks.py"):
        router_text = (FIXTURE_ROOT / "app/routers" / router_file).read_text(encoding="utf-8")
        assert "get_optional_user" not in router_text