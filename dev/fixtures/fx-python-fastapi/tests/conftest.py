"""Pytest fixtures for the ffx-fastapi fixture (pytest-asyncio, mode=auto).

Nota: pytest-asyncio por defecto crea un nuevo event loop por test
(function scope). Esto rompe aiosqlite porque las conexiones de un
loop se invalidan cuando el loop se cierra. Usamos session-scope para
el engine y el loop compartido.
"""
import asyncio
import os
from typing import AsyncIterator

import pytest
import pytest_asyncio

os.environ.setdefault("TESTING", "1")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_engine.db?cache=shared")

from httpx import ASGITransport, AsyncClient  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from app.celery_app import configure_for_testing  # noqa: E402
from app.database import get_session  # noqa: E402
from app.main import app  # noqa: E402
from app.models.base import Base  # noqa: E402


configure_for_testing()


@pytest.fixture(scope="session")
def event_loop():
    """Event loop compartido para que las conexiones aiosqlite persistan."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    eng = create_async_engine(
        "sqlite+aiosqlite:///./test_engine.db?cache=shared",
        echo=False,
        future=True,
    )
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture(loop_scope="session")
async def db_session(engine) -> AsyncIterator[AsyncSession]:
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        # Limpiar datos previos entre tests.
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
        yield session


@pytest_asyncio.fixture(loop_scope="session")
async def client(engine) -> AsyncIterator[AsyncClient]:
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def _override_session() -> AsyncIterator[AsyncSession]:
        async with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = _override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


AUTH_HEADER = {"Authorization": "Bearer stub-token"}


@pytest_asyncio.fixture(loop_scope="session")
async def auth_client(client, db_session) -> AsyncIterator[AsyncClient]:
    """Client con Authorization Bearer + un user sembrado."""
    from app.models.user import User  # noqa: E402
    from datetime import datetime, timezone  # noqa: E402
    user = User(
        email="seed@fxfast.com",
        hashed_password="hashed_seed",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Inyectar el header en cada request.
    class AuthedClientWrapper:
        def __init__(self, base_client: AsyncClient, header: dict):
            self._base = base_client
            self._header = header

        def __getattr__(self, name):
            return getattr(self._base, name)

        async def get(self, url, **kwargs):
            headers = {**self._header, **kwargs.pop("headers", {})}
            return await self._base.get(url, headers=headers, **kwargs)

        async def post(self, url, **kwargs):
            headers = {**self._header, **kwargs.pop("headers", {})}
            return await self._base.post(url, headers=headers, **kwargs)

        async def patch(self, url, **kwargs):
            headers = {**self._header, **kwargs.pop("headers", {})}
            return await self._base.patch(url, headers=headers, **kwargs)

        async def delete(self, url, **kwargs):
            headers = {**self._header, **kwargs.pop("headers", {})}
            return await self._base.delete(url, headers=headers, **kwargs)

        async def request(self, method, url, **kwargs):
            headers = {**self._header, **kwargs.pop("headers", {})}
            return await self._base.request(method, url, headers=headers, **kwargs)

    yield AuthedClientWrapper(client, AUTH_HEADER)