"""FastAPI router for Subscription (trampa E03).

Trampa E03: APIRouter define prefix='/subscriptions' y
dependencies=[Depends(get_active_subscription)] a nivel de router.
Esto hace que CADA endpoint requiera una suscripcion activa, lo que
no es evidente sin leer el router.
"""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_active_subscription, get_db
from ..models.subscription import Subscription
from ..schemas.subscription import SubscriptionCreate, SubscriptionOut
from ..services import subscription_service


router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    dependencies=[Depends(get_active_subscription)],
)


@router.post("/", response_model=SubscriptionOut, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    payload: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
) -> SubscriptionOut:
    sub = await subscription_service.create_subscription(db, payload)
    return SubscriptionOut.model_validate(sub)


@router.get("/{sub_id}", response_model=SubscriptionOut)
async def get_subscription(
    sub_id: int,
    db: AsyncSession = Depends(get_db),
) -> SubscriptionOut:
    sub = await subscription_service.get_subscription(db, sub_id)
    if sub is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="subscription not found")
    return SubscriptionOut.model_validate(sub)


@router.get("/", response_model=list[SubscriptionOut])
async def list_my_subscriptions(
    sub: Subscription = Depends(get_active_subscription),
    db: AsyncSession = Depends(get_db),
) -> list[SubscriptionOut]:
    subs = await subscription_service.list_subscriptions_for_user(db, sub.user_id)
    return [SubscriptionOut.model_validate(s) for s in subs]


@router.post("/{sub_id}/cancel", response_model=SubscriptionOut)
async def cancel_my_subscription(
    sub_id: int,
    db: AsyncSession = Depends(get_db),
) -> SubscriptionOut:
    sub = await subscription_service.get_subscription(db, sub_id)
    if sub is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="subscription not found")
    canceled = await subscription_service.cancel_subscription(db, sub)
    return SubscriptionOut.model_validate(canceled)