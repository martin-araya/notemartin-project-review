"""Service layer for Subscription."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.subscription import Subscription, SubscriptionStatus
from ..schemas.subscription import SubscriptionCreate


async def create_subscription(db: AsyncSession, payload: SubscriptionCreate) -> Subscription:
    sub = Subscription(
        user_id=payload.user_id,
        plan=payload.plan,
        started_at=payload.started_at,
        ends_at=payload.ends_at,
        status=SubscriptionStatus.ACTIVE.value,
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub


async def cancel_subscription(db: AsyncSession, sub: Subscription) -> Subscription:
    sub.status = SubscriptionStatus.CANCELED.value
    await db.commit()
    await db.refresh(sub)
    return sub


async def get_subscription(db: AsyncSession, sub_id: int) -> Subscription | None:
    return await db.get(Subscription, sub_id)


async def list_subscriptions_for_user(db: AsyncSession, user_id: int) -> list[Subscription]:
    stmt = select(Subscription).where(Subscription.user_id == user_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())