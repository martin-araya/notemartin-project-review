"""Celery application setup with EAGER mode in tests.

Trampa P06: en dev/tests CELERY_TASK_ALWAYS_EAGER=True ejecuta las
tasks sincronamente. Las tareas 'async def' decoradas con @shared_task
de Celery 5.3 NO soportan coroutines nativamente; el resultado se
pierde (la coroutine nunca se ejecuta).
"""
from celery import Celery

from .config import settings


BROKER_URL = "memory://"
RESULT_BACKEND = "cache+memory://"

celery_app = Celery(
    "fxfast",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

celery_app.conf.update(
    task_always_eager=settings.TESTING,
    task_eager_propagates=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)


def configure_for_testing() -> None:
    celery_app.conf.task_always_eager = True