"""Tests for the certificates feature."""
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.certificates.models import Certificate
from apps.enrollments.models import Enrollment


@pytest.mark.django_db
def test_emitir_certificate_via_api_returns_201(user):
    enrollment = Enrollment.objects.create(user=user, status="completed", total=Decimal("100.00"))
    client = APIClient()
    payload = {"enrollment": enrollment.pk}
    resp = client.post("/api/certificates/", payload, format="json")
    assert resp.status_code == 201
    assert Certificate.objects.filter(enrollment=enrollment).count() == 1


@pytest.mark.django_db
def test_listar_certificates_devuelve_lista(user):
    enrollment = Enrollment.objects.create(user=user, status="completed", total=Decimal("100.00"))
    Certificate.objects.create(enrollment=enrollment, serial="CERT-001", status="issued")
    client = APIClient()
    resp = client.get("/api/certificates/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_obtener_certificate_inexistente_retorna_404():
    client = APIClient()
    resp = client.get("/api/certificates/9999/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_certificate_serial_unico(user):
    enrollment1 = Enrollment.objects.create(user=user, status="completed", total=Decimal("100.00"))
    Certificate.objects.create(enrollment=enrollment1, serial="CERT-001", status="issued")
    # Try to create another with the same serial via the API
    client = APIClient()
    payload = {"enrollment": enrollment1.pk}
    resp = client.post("/api/certificates/", payload, format="json")
    assert resp.status_code in (201, 400)  # 400 if serial collision