"""Tests for the webhooks feature (FEAT-003)."""
import pytest


@pytest.mark.asyncio
async def test_registrar_webhook_valido_returns_201(client):
    payload = {
        "url": "https://example.com/hook1",
        "event_type": "user.created",
        "secret": "this-is-a-very-strong-secret-123",
        "is_active": True,
    }
    resp = await client.post("/webhooks/", json=payload)
    assert resp.status_code == 201, resp.text
    assert resp.json()["event_type"] == "user.created"


@pytest.mark.asyncio
async def test_listar_webhooks_devuelve_lista(client):
    resp = await client.get("/webhooks/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_dispatch_webhook_event_returns_dispatched_count(client):
    payload = {
        "url": "https://example.com/hook2",
        "event_type": "user.created",
        "secret": "another-very-strong-secret-456",
        "is_active": True,
    }
    await client.post("/webhooks/", json=payload)
    resp = await client.post("/webhooks/dispatch?event_type=user.created", json={"data": "x"})
    assert resp.status_code == 200
    body = resp.json()
    assert "dispatched" in body


@pytest.mark.asyncio
async def test_webhook_secret_muy_corto_returns_422(client):
    payload = {
        "url": "https://example.com/hook3",
        "event_type": "user.created",
        "secret": "corto",  # min_length=16
        "is_active": True,
    }
    resp = await client.post("/webhooks/", json=payload)
    assert resp.status_code == 422