"""Celery tasks for webhook dispatch.

Trampa P06: esta task es 'async def' decorada con @shared_task.
Celery 5.3 no soporta coroutines nativamente; en EAGER mode la
coroutine se retorna como resultado sin ejecutarse, por lo que el
side effect (HTTP POST al webhook URL) se pierde silenciosamente.
"""
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
async def dispatch_webhook_event(self, webhook_id: int, event: dict) -> dict:
    """Envia un evento al webhook de una sesion.

    Side effect esperado: HTTP POST a la URL del webhook con el evento.
    """
    logger.info("dispatching event to webhook %s", webhook_id)
    return {"webhook_id": webhook_id, "event": event}