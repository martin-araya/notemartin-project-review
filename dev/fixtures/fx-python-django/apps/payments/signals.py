"""Signals for the payments app.

Trampa P02: queryset sin indice para filtros custom (excepto el
de status que SI tiene indice). El Manager expone .completed() y
.for_enrollment() que filtran sin indice, causando full scan.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment


@receiver(post_save, sender=Payment, dispatch_uid="apps.payments.signals.payment_saved")
def payment_post_save(sender, instance: Payment, created, **kwargs):
    if created:
        # dead_signal: handler_pago_fallido existe pero NO esta conectado
        # (ver trampa S02 en handlers_dead.py).
        pass


def handler_pago_fallido(payment: Payment):
    """Handler dead: NO esta conectado como signal (trampa S02)."""
    payment.status = Payment.STATUS_FAILED
    payment.save(update_fields=["status"])