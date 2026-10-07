"""Custom template tags for the payments app."""
from django import template

from ..models import Payment

register = template.Library()


@register.simple_tag
def payment_status_badge(status: str) -> str:
    mapping = {
        Payment.STATUS_PENDING: "badge-warning",
        Payment.STATUS_COMPLETED: "badge-success",
        Payment.STATUS_FAILED: "badge-error",
        Payment.STATUS_REFUNDED: "badge-info",
    }
    return mapping.get(status, "badge-default")