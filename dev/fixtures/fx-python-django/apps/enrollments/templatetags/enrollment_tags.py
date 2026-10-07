"""Custom template tags for the enrollments app (trampa E06)."""
from django import template

from ..models import Enrollment

register = template.Library()


@register.simple_tag
def enrollment_status_label(status: str) -> str:
    """Devuelve una etiqueta legible para un status de Enrollment."""
    mapping = {
        Enrollment.STATUS_PENDING: "Pendiente",
        Enrollment.STATUS_ACTIVE: "Activo",
        Enrollment.STATUS_CANCELLED: "Cancelado",
        Enrollment.STATUS_COMPLETED: "Completado",
    }
    return mapping.get(status, status)


@register.filter
def enrollment_is_active(enrollment: Enrollment) -> bool:
    """Devuelve True si la inscripcion esta activa."""
    return enrollment.status == Enrollment.STATUS_ACTIVE