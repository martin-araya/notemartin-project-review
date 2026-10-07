from celery import shared_task


@shared_task
def emitir_recibo(payment_id: int):
    """Emite un recibo tras un pago completado (Celery task)."""
    return f"recibo:{payment_id}"