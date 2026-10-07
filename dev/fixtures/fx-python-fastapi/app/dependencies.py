"""FastAPI dependencies with yield chains (trampa E01).

Cadena: get_db -> get_current_user -> get_active_subscription.
La skill debe leer este archivo para entender la cadena completa,
no saltar directamente a los endpoints.

Trampa P02: get_db cierra la sesion pero NO hace rollback si hay
excepcion; los cambios pendientes pueden quedar antes del close.
"""
from typing import AsyncIterator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .models.subscription import Subscription
from .models.user import User


async def get_db() -> AsyncIterator[AsyncSession]:
    async for session in get_session():
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(default=None),
) -> User:
    """Extrae el usuario actual.

    Stub: en un fixture real esto validaria un JWT. Aqui simplemente
    devuelve el primer usuario activo de la DB si authorization empieza
    con 'Bearer stub-token', o lanza 401.
    """
    if not authorization or not authorization.startswith("Bearer stub-token"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    user = await db.get(User, 1)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    return user


async def get_active_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Subscription:
    """Devuelve la suscripcion activa del usuario."""
    from sqlalchemy import select  # local para evitar ciclo
    stmt = select(Subscription).where(
        Subscription.user_id == user.id, Subscription.status == "active"
    )
    result = await db.execute(stmt)
    sub = result.scalar_one_or_none()
    if sub is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="no active subscription")
    return sub


async def get_optional_user(db: AsyncSession = Depends(get_db)) -> User | None:
    """Dependencia muerta (trampa S03): no se usa en ningun router."""
    return None