"""FastAPI application entrypoint with lifespan (trampa E04).

Trampa E04: los side effects de startup/shutdown (init_db, registro
de metricas) viven en el contextmanager lifespan, no en los endpoints.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import close_db, init_db
from .routers import subscriptions, users, webhooks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # E04: side effects en startup.
    try:
        await init_db()
    except Exception:
        # Trampa P04: la excepcion se swallowa con try/except en vez de
        # re-levantar; la app arranca con DB no inicializada y los
        # endpoints fallan con errores cripticos.
        import logging
        logging.getLogger("fxfast.lifespan").warning(
            "init_db failed at startup; continuing without schema",
            exc_info=True,
        )
    yield
    # E04: side effects en shutdown.
    await close_db()


app = FastAPI(
    title="fxfast",
    version="1.0.0",
    lifespan=lifespan,
)


# E03: include_router con prefix y dependencies a nivel de router.
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(webhooks.router)