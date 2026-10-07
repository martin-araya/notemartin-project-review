"""Custom context processor for the enrollments app (trampa E06).

Registrado en TEMPLATES['OPTIONS']['context_processors'] de base.py.
"""
from ..models import Enrollment


def enrollment_counts(request):
    """Anade counters globales de inscripciones a todas las templates."""
    try:
        total = Enrollment.objects.count()
    except Exception:
        total = 0
    return {
        "enrollments_total": total,
        "enrollments_active_total": 0,
    }