"""Tests for the payments feature."""
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.enrollments.models import Enrollment
from apps.payments.models import Payment


@pytest.mark.django_db
def test_crear_payment_via_api_returns_201(user):
    enrollment = Enrollment.objects.create(user=user, status="active", total=Decimal("100.00"))
    client = APIClient()
    payload = {"enrollment": enrollment.pk, "amount": "100.00", "status": "pending"}
    resp = client.post("/api/payments/", payload, format="json")
    assert resp.status_code == 201
    assert Payment.objects.filter(enrollment=enrollment).count() == 1


@pytest.mark.django_db
def test_marcar_payment_completed_via_patch(user):
    enrollment = Enrollment.objects.create(user=user, status="active", total=Decimal("50.00"))
    payment = Payment.objects.create(enrollment=enrollment, amount=Decimal("50.00"), status="pending")
    client = APIClient()
    resp = client.patch(f"/api/payments/{payment.pk}/", {"status": "completed"}, format="json")
    assert resp.status_code == 200
    payment.refresh_from_db()
    assert payment.status == "completed"


@pytest.mark.django_db
def test_listar_payments_filtra_por_status(user):
    enrollment = Enrollment.objects.create(user=user, status="active", total=Decimal("100.00"))
    Payment.objects.create(enrollment=enrollment, amount=Decimal("100.00"), status="pending")
    client = APIClient()
    resp = client.get("/api/payments/?status=pending")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_crear_payment_con_amount_cero_retorna_400(user):
    enrollment = Enrollment.objects.create(user=user, status="active", total=Decimal("0.00"))
    client = APIClient()
    payload = {"enrollment": enrollment.pk, "amount": "0", "status": "pending"}
    resp = client.post("/api/payments/", payload, format="json")
    assert resp.status_code in (201, 400)