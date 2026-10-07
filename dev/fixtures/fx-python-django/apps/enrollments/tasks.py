"""Celery tasks for the enrollments app (trampa P04: EAGER en tests)."""
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def procesar_inscripcion(self, enrollment_id: int):
    """Procesa una inscripcion: valida stock y notifica al usuario.

    En dev/tests `CELERY_TASK_ALWAYS_EAGER=True` ejecuta esta funcion
    sincronamente dentro del request. Las excepciones se propagan al
    caller; en prod se ejecutaria en un worker real con reintentos.
    """
    logger.info("procesando inscripcion %s", enrollment_id)
    return f"processed:{enrollment_id}"