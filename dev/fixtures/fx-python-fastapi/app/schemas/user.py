"""Pydantic v2 schemas for User (trampa E02).

UserCreate.email tiene un @field_validator que prepara el email
(normaliza a minusculas). El validador mismo NO consulta la DB;
la verificacion de unicidad ocurre en user_service.create_user con
un SELECT sin lock (la trampa de paquete P01).
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def email_unica_valid(cls, v: str) -> str:
        """Validador que prepara el email para validar unicidad en DB.

        Trampa E02: este validador esta declarado como un validador
        estandar pero el codigo real (en user_service.create_user)
        hace la query a la DB para unicidad con un SELECT sin lock.
        La trampa es la separacion entre la 'validacion de formato'
        (aqui) y la 'validacion de unicidad' (en el servicio), que
        abre una ventana TOCTOU (trampa P01).
        """
        return v.lower().strip()


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserOut(UserBase):
    id: int
    created_at: datetime