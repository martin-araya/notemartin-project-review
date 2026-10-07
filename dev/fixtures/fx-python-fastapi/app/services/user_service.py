"""Service layer for User (basic CRUD + hashing)."""
import hashlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


def _hash_password(password: str) -> str:
    """Stub de hashing (NO usar en produccion)."""
    return hashlib.sha256(password.encode()).hexdigest()


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    """Crea un nuevo usuario con email hasheado."""
    user = User(
        email=payload.email,
        hashed_password=_hash_password(payload.password),
        is_active=payload.is_active,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession, limit: int = 50, offset: int = 0) -> list[User]:
    stmt = select(User).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_user(db: AsyncSession, user: User, payload: UserUpdate) -> User:
    if payload.email is not None:
        user.email = payload.email
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.password is not None:
        user.hashed_password = _hash_password(payload.password)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()