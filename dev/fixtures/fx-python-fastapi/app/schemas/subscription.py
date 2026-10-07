"""Pydantic v2 schemas for Subscription (trampa E02).

SubscriptionCreate usa @model_validator(mode='after') para verificar
que ends_at > started_at (parte de la validacion esperada) y ademas
comprueba business logic: limites del plan activo del usuario.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class SubscriptionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plan: str = "basic"
    started_at: datetime
    ends_at: datetime


class SubscriptionCreate(SubscriptionBase):
    user_id: int

    @model_validator(mode="after")
    def validate_dates_and_plan(self) -> "SubscriptionCreate":
        """Validador que verifica fechas y limites del plan.

        Trampa E02: este @model_validator consulta la DB para verificar
        si el usuario ya tiene un subscription activo del mismo plan.
        El validador depende de un estado global (DB) sin declararlo
        en la firma.
        """
        if self.ends_at <= self.started_at:
            raise ValueError("ends_at debe ser posterior a started_at")
        return self


class SubscriptionOut(SubscriptionBase):
    id: int
    user_id: int
    status: str