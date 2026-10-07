from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Certificate


@receiver(post_save, sender=Certificate, dispatch_uid="apps.certificates.signals.certificate_saved")
def certificate_post_save(sender, instance: Certificate, created, **kwargs):
    """Side-effect al guardar un Certificate (placeholder)."""
    if created:
        pass