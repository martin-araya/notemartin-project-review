"""Custom template tags for the certificates app.

Trampa S03: `format_certificate_id` existe pero NO se usa en ninguna
template; la skill debe detectarlo via grep.
"""
from django import template

from ..models import Certificate

register = template.Library()


@register.simple_tag
def format_certificate_id(certificate: Certificate) -> str:
    """Formatea el serial de un Certificate (DEAD: no usado en templates)."""
    return f"CERT-{certificate.serial}"


@register.filter
def certificate_is_valid(certificate: Certificate) -> bool:
    return certificate.status == Certificate.STATUS_ISSUED