"""Pydantic v2 schemas for Webhook."""
from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class WebhookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: AnyHttpUrl
    event_type: str = Field(min_length=1, max_length=64)
    secret: str = Field(min_length=16, max_length=128)
    is_active: bool = True


class WebhookCreate(WebhookBase):
    pass


class WebhookOut(WebhookBase):
    id: int
    created_at: datetime