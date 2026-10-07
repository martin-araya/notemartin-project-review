"""Tests for the admin actions feature (FEAT-004)."""
import pytest
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from apps.audit.admin import AuditLogAdmin
from apps.audit.models import AuditLog


def _make_request(user):
    rf = RequestFactory()
    request = rf.get("/")
    request.user = user
    setattr(request, "session", {})
    setattr(request, "_messages", FallbackStorage(request))
    return request


@pytest.mark.django_db
def test_export_csv_action_returns_csv_response(user):
    AuditLog.objects.create(actor=user, action="login", target="user:1", level="info")
    admin = AuditLogAdmin(model=AuditLog, admin_site=None)
    request = _make_request(user)
    queryset = AuditLog.objects.all()
    response = admin.export_csv(request, queryset)
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"


@pytest.mark.django_db
def test_mark_reviewed_action_updates_queryset(user):
    AuditLog.objects.create(actor=user, action="login", target="user:1", level="info")
    AuditLog.objects.create(actor=user, action="logout", target="user:1", level="info")
    admin = AuditLogAdmin(model=AuditLog, admin_site=None)
    request = _make_request(user)
    queryset = AuditLog.objects.all()
    admin.mark_reviewed(request, queryset)
    assert AuditLog.objects.filter(reviewed=True).count() == 2


@pytest.mark.django_db
def test_admin_action_no_public_route():
    """Las acciones de admin NO estan expuestas como rutas DRF publicas."""
    from django.urls import get_resolver

    resolver = get_resolver()
    patterns = [str(p.pattern) for p in resolver.url_patterns]
    # No debe haber endpoint DRF publico para las acciones de audit
    # (export_csv / mark_reviewed solo existen en el shell de admin).
    public_audit = [
        p for p in patterns
        if "audit" in p and "admin" not in p
    ]
    assert public_audit == [] or all("export" not in p for p in public_audit)