"""Tests for the 6 package traps planted in the fixture."""
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


def test_p01_pydantic_validator_race():
    """Validador que NO usa SELECT FOR UPDATE."""
    user_schema = (FIXTURE_ROOT / "app/schemas/user.py").read_text(encoding="utf-8")
    assert "@field_validator" in user_schema
    # La trampa P01: el codigo real (en user_service.create_user) hace
    # la query a la DB para unicidad con un SELECT sin lock (TOCTOU).
    # El validador Pydantic SOLO normaliza el email; el servicio es el
    # que valida unicidad sin lock.
    assert "normalize" in user_schema.lower() or "lower" in user_schema
    # Verifica que NO menciona ningun mecanismo de lock
    assert "FOR UPDATE" not in user_schema
    assert "select_for_update" not in user_schema
    assert "with transaction.atomic" not in user_schema


def test_p02_yield_dep_no_rollback_on_error():
    """get_db cierra la sesion pero NO hace rollback."""
    deps = (FIXTURE_ROOT / "app/dependencies.py").read_text(encoding="utf-8")
    bloque_get_db = deps[deps.index("async def get_db"):deps.index("async def get_current_user")]
    assert "yield" in bloque_get_db
    assert "rollback" not in bloque_get_db.lower()


def test_p03_include_router_order_shadows():
    """El orden de include_router esta documentado en el codigo."""
    main = (FIXTURE_ROOT / "app/main.py").read_text(encoding="utf-8")
    # El orden importa: webhooks router se incluye al final
    idx_users = main.index("users.router")
    idx_subs = main.index("subscriptions.router")
    idx_hooks = main.index("webhooks.router")
    assert idx_users < idx_subs < idx_hooks


def test_p04_lifespan_exception_swallowed():
    """El startup tiene try/except que swallowea init_db errors."""
    main = (FIXTURE_ROOT / "app/main.py").read_text(encoding="utf-8")
    bloque_startup = main[main.index("try:"):main.index("yield")]
    assert "init_db()" in bloque_startup
    assert "except Exception" in bloque_startup


def test_p05_custom_decorator_breaks_signature():
    """track_request NO usa functools.wraps."""
    decorators = (FIXTURE_ROOT / "app/decorators.py").read_text(encoding="utf-8")
    assert "functools.wraps" not in decorators


def test_p06_celery_eager_in_async_context():
    """dispatch_webhook_event es async pero @shared_task no soporta async."""
    tasks = (FIXTURE_ROOT / "app/tasks/webhook_tasks.py").read_text(encoding="utf-8")
    assert "async def dispatch_webhook_event" in tasks
    assert "@shared_task" in tasks