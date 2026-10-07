"""Signals for the enrollments app (trampa E01).

Conectados en apps.EnrollmentsConfig.ready() — la skill debe saltar de
apps.py a este archivo para entender el side effect post_save.
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Enrollment
from .tasks import procesar_inscripcion

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Enrollment, dispatch_uid="apps.enrollments.signals.enrollment_saved")
def enrollment_post_save(sender, instance: Enrollment, created, **kwargs):
    """Side-effect implicito al guardar un Enrollment.

    Trampa P01: este signal se ejecuta dentro de la misma transaccion
    que la creacion del Enrollment, sin proteccion ante rollback. Si la
    transaccion falla despues, la task queda en un estado inconsistente.
    """
    if created:
        logger.info("procesando inscripcion %s", instance.pk)
        procesar_inscripcion.delay(instance.pk)