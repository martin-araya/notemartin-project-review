# Fixture F06q — fx-python-fastapi

API **FastAPI 0.115** asincrona con **Pydantic v2**, **SQLAlchemy 2 async**
sobre **SQLite (aiosqlite)**, **Alembic** con data migration, **Celery**
(Modo EAGER en tests), validacion via **httpx.AsyncClient** y **pytest-asyncio**.
Plantada para que la skill tenga que rastrear las trampas clasicas
del ecosistema FastAPI:

## Stack

- **Lenguaje:** Python 3.11.
- **Framework web:** FastAPI 0.115 + Pydantic 2.9.
- **Async DB:** SQLAlchemy 2.0 + aiosqlite.
- **Migrations:** Alembic 1.13 (con data migration, trampa E06).
- **Async tasks:** Celery 5.3 (`EAGER` en dev/tests).
- **Tests:** pytest 8.2 + pytest-asyncio 0.23 + httpx 0.27 (ASGITransport).

## Como se ejecutan los tests

```bash
make test           # pytest -q
make build          # alembic upgrade head
make history        # regenera la historia git (8 commits)
```

En contenedor (con Python 3.11 + make):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-python-fastapi --container
```

## Estructura

- `app/main.py`: `FastAPI()` con `lifespan=lifespan` (E04) +
  `include_router` (E03).
- `app/config.py`: `Settings(BaseSettings)` (Pydantic v2).
- `app/database.py`: `engine = create_async_engine(...)` async.
- `app/dependencies.py`: `get_db`, `get_current_user`,
  `get_active_subscription` con `yield` (E01); `get_optional_user`
  dead (S03).
- `app/celery_app.py`: `Celery("fxfast", broker="memory://")` EAGER.
- `app/decorators.py`: `track_request` (E05: registra rutas en
  global registry).
- `app/models/`: `User`, `Subscription`, `Webhook`.
- `app/schemas/`: `UserCreate` con `@field_validator('email')`
  que consulta DB (E02); `SubscriptionCreate` con
  `@model_validator(mode='after')`; `LegacyUsuarioSchema` dead
  (S02).
- `app/services/`: logica de negocio.
- `app/routers/`: `users`, `subscriptions`, `webhooks` con
  `APIRouter(prefix=, dependencies=)` (E03); `webhooks` tiene
  `GET /debug` dead (S01).
- `app/tasks/`: `dispatch_webhook_event` (Celery).
- `alembic/versions/`: `001_initial.py` (schema),
  `002_seed_data.py` (data migration, E06).

## Features

1. **usuarios** (FEAT-001): crear, obtener, listar, validar.
   7 R-NN.
2. **suscripciones** (FEAT-002): crear, cancelar, listar,
   validar fechas. 7 R-NN.
3. **webhooks** (FEAT-003): registrar, dispatch event, validar.
   7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): Depends con yield chains, Pydantic
  validators con logica de negocio, include_router con prefix
  y dependencies a nivel de router, eventos de lifespan,
  decoradores propios que registran rutas, Alembic migrations
  con data migration.
- 6 del paquete (CC-04): Pydantic validator race, yield dep sin
  rollback, include_router order shadows, lifespan exception
  swallowed, custom decorator breaks docstring + ded,
  Celery EAGER en contexto async.
- 3 superficiales (CC-05): dead route `/debug`, dead Pydantic
  model `LegacyUsuarioSchema`, dead dependency
  `get_optional_user`.