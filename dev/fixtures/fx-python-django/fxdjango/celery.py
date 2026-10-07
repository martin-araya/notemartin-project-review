"""Celery app for fxdjango project.

Trampa P04: en dev/tests `CELERY_TASK_ALWAYS_EAGER=True` hace que las
tasks se ejecuten sincronamente dentro del request. Las excepciones se
propagan al caller; en prod el comportamiento es asincrono con un
worker real contra un broker.
"""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fxdjango.settings.dev")

BROKER_URL = "memory://"
RESULT_BACKEND = "cache+memory://"

app = Celery(
    "fxdjango",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()