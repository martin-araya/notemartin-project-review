# Ground truth de fx-python-fastapi (F06q)

API **FastAPI 0.115** asincrona con **Pydantic v2**,
**SQLAlchemy 2 async** sobre **SQLite (aiosqlite)**,
**Alembic** con data migration, **Celery** (modo EAGER en tests).
Plantada para que la skill tenga que rastrear las trampas clasicas
del ecosistema FastAPI.

## Features

1. **usuarios** (FEAT-001): crear, obtener, listar, actualizar,
   eliminar via DRF + router-level `get_current_user` dep + Pydantic
   validator que normaliza email (sin lock en unicidad, trampa P01).
   7 R-NN.
2. **suscripciones** (FEAT-002): crear, listar, cancelar via
   `/subscriptions/` + router-level `get_active_subscription` dep
   (dependencia anidada) + `@model_validator(mode='after')` para
   validar `ends_at > started_at`. 7 R-NN.
3. **webhooks** (FEAT-003): registrar, listar, dispatch via
   `/webhooks/` (publico, sin router-level dep, contraste con
   users/subscriptions) + Celery EAGER task que es `async def`
   (perdida por trampa P06). 7 R-NN.

## Trampas del ecosistema (CC-06)

1. `depends_yield_chains`: `get_db` -> `get_current_user` ->
   `get_active_subscription` (anidada via `Depends`).
2. `pydantic_validator_with_business_logic`:
   `@field_validator('email')` y `@model_validator(mode='after')`.
3. `include_router_prefix_and_dependencies`: cada router define
   `prefix=` y opcionalmente `dependencies=` a nivel de router.
4. `lifespan_events`: `@asynccontextmanager async def lifespan`
   con startup (init_db + try/except que swallowea, P04) y shutdown
   (close_db).
5. `custom_decorator_registers_routes`: `@track_request` registra
   en `_REQUEST_REGISTRY` y `_REGISTERED_ROUTES`.
6. `alembic_migration_with_data`: `002_seed_data.py` con
   `op.execute('INSERT INTO ...')` ademas de schema.

## Trampas del paquete (CC-04)

1. `pydantic_validator_race`: `@field_validator` no consulta DB;
   la unicidad se valida en `user_service.create_user` sin lock.
2. `yield_dep_no_rollback_on_error`: `get_db` cierra la sesion sin
   `await session.rollback()` en caso de excepcion.
4. `lifespan_exception_swallowed`: `try/except Exception` en
   startup silencia `init_db` failures.
5. `custom_decorator_breaks_signature`: `track_request` no usa
   `functools.wraps(func)`, pierde `__name__`/`__doc__`.
6. `celery_eager_in_async_context`: `dispatch_webhook_event` es
   `async def` con `@shared_task`; EAGER pierde la coroutine.

## Trampas superficiales (CC-05)

1. `dead_route`: `GET /webhooks/debug` retorna `{"status":"ok"}`.
2. `dead_pydantic_model`: `LegacyUsuarioSchema` no se importa.
3. `dead_dependency`: `get_optional_user` no se usa en routers.

## Decisiones tecnicas (ver DECISIONS.md D-230..D-238)

- D-230: Python 3.11 + FastAPI 0.115 + Pydantic 2.9 + Pydantic-Settings
  + SQLAlchemy 2.0.36 async + Alembic 1.13 + aiosqlite + Celery 5.3
  + httpx 0.27 + pytest 8.2 + pytest-asyncio 0.24 + email-validator.
- D-231: Routers en ingles (users, subscriptions, webhooks); URLs en
  ingles (`/users`, `/subscriptions`, `/webhooks`).
- D-232: Celery en modo EAGER en dev/tests; broker `memory://`.
- D-233: pytest-asyncio `asyncio_mode = auto` + `loop_scope = session`
  en fixtures async (aiosqlite requiere event loop compartido).
- D-234: Prefijo `NPRGT-FXFAST-` para 29 unique tokens.
- D-235: `Makefile` envuelve `pytest -q`.
- D-236: Imagen Docker `python:3.11-slim` + `apt-get install make`.
- D-237: `requires: [linux, macos, windows]`.
- D-238: `fixtures_matrix.py` y `target_matrix.yml` extendidos.