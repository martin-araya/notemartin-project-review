"""FastAPI router for Webhook (trampa E03, S01).

Trampa E03: este router NO tiene `dependencies=` en APIRouter; los
webhooks son publicos. La skill debe notar el contraste con users
y subscriptions.

Trampa S01: GET /debug es una ruta dead que no se usa en tests.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..schemas.webhook import WebhookCreate, WebhookOut
from ..services import webhook_service


router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
    # NOT having `dependencies=[]` is the contrast: webhooks are public.
)


@router.post("/", response_model=WebhookOut, status_code=status.HTTP_201_CREATED)
async def register_webhook(
    payload: WebhookCreate,
    db: AsyncSession = Depends(get_db),
) -> WebhookOut:
    wh = await webhook_service.register_webhook(db, payload)
    return WebhookOut.model_validate(wh)


@router.get("/", response_model=list[WebhookOut])
async def list_webhooks(
    event_type: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[WebhookOut]:
    if event_type:
        hooks = await webhook_service.list_webhooks_for_event(db, event_type)
    else:
        from sqlalchemy import select
        from ..models.webhook import Webhook
        stmt = select(Webhook)
        result = await db.execute(stmt)
        hooks = list(result.scalars().all())
    return [WebhookOut.model_validate(h) for h in hooks]


@router.post("/dispatch", response_model=dict)
async def dispatch_webhook(
    event_type: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
) -> dict:
    job_ids = await webhook_service.dispatch_event(db, event_type, payload)
    return {"dispatched": len(job_ids), "job_ids": job_ids}


@router.get("/debug", response_model=dict)
async def debug_webhooks() -> dict:
    """Endpoint dead (trampa S01): retorna 200 OK literal sin logica.

    Ningun test lo invoca. La skill debe detectarlo via grep.
    """
    return {"status": "ok"}