from celery import shared_task


@shared_task
def generar_pdf(certificate_id: int):
    """Genera el PDF de un certificado emitido (Celery task)."""
    return f"pdf:{certificate_id}"