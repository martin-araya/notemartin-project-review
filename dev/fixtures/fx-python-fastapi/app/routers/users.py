"""FastAPI router for User (trampa E03).

Trampa E03: APIRouter define prefix='/users' y
dependencies=[Depends(get_current_user)] a nivel de router. Todas
las rutas en este router heredan la auth automaticamente.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user, get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserOut, UserUpdate
from ..services import user_service


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
    responses={401: {"description": "Unauthorized"}},
)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await user_service.create_user(db, payload)
    return UserOut.model_validate(user)


@router.get("/", response_model=list[UserOut])
async def list_users(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> list[UserOut]:
    users = await user_service.list_users(db, limit=limit, offset=offset)
    return [UserOut.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="user not found")
    return UserOut.model_validate(user)


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="user not found")
    updated = await user_service.update_user(db, user, payload)
    return UserOut.model_validate(updated)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="user not found")
    await user_service.delete_user(db, user)