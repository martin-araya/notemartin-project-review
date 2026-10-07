"""Service layer for Webhook."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.webhook import Webhook
from ..schemas.webhook import WebhookCreate


async def register_webhook(db: AsyncSession, payload: WebhookCreate) -> Webhook:
    wh = Webhook(
        url=str(payload.url),
        event_type=payload.event_type,
        secret=payload.secret,
        is_active=payload.is_active,
    )
    db.add(wh)
    await db.commit()
    await db.refresh(wh)
    return wh


async def list_webhooks_for_event(
    db: AsyncSession, event_type: str
) -> list[Webhook]:
    stmt = select(Webhook).where(
        Webhook.event_type == event_type, Webhook.is_active.is_(True)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_webhook(db: AsyncSession, webhook_id: int) -> Webhook | None:
    return await db.get(Webhook, webhook_id)


async def dispatch_event(
    db: AsyncSession, event_type: str, payload: dict
) -> list[int]:
    """Encola una task Celery por cada webhook activo del event_type.

    Trampa P06: la task Celery es 'async def' decorada con @shared_task;
    Celery 5.3 NO soporta coroutines nativamente. En EAGER mode la
    coroutine se retorna sin ejecutarse, perdiendo el dispatch.
    """
    from ..tasks.webhook_tasks import dispatch_webhook_event
    hooks = await list_webhooks_for_event(db, event_type)
    job_ids = []
    for hook in hooks:
        job = dispatch_webhook_event.delay(hook.id, payload)
        job_ids.append(getattr(job, "id", 0) or 0)
    return job_ids