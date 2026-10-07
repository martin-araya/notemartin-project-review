"""Tests for the subscriptions feature (FEAT-002)."""
import pytest


@pytest.mark.asyncio
async def test_create_subscription_sin_auth_returns_401_o_403(client):
    """El router tiene dependencies=[Depends(get_active_subscription)].
    Sin auth valida -> 401 (token) o 403 (no active subscription)."""
    resp = await client.post("/subscriptions/", json={
        "user_id": 1,
        "plan": "basic",
        "started_at": "2026-10-07T00:00:00+00:00",
        "ends_at": "2026-12-07T00:00:00+00:00",
    })
    assert resp.status_code in (401, 403)


@pytest.mark.asyncio
async def test_subscription_ends_before_start_returns_ends_o_422_en_test():
    """Trampa E02: el @model_validator rechaza ends_at <= started_at -> 422.
    Llamamos al validador directamente sin pasar por la API.
    """
    from pydantic import ValidationError
    from app.schemas.subscription import SubscriptionCreate
    try:
        SubscriptionCreate(
            user_id=1,
            plan="basic",
            started_at="2026-12-01T00:00:00+00:00",
            ends_at="2026-11-01T00:00:00+00:00",
        )
        raise AssertionError("expected ValidationError")
    except ValidationError:
        pass


@pytest.mark.asyncio
async def test_get_subscription_sin_auth_returns_401_o_403(client):
    resp = await client.get("/subscriptions/9999")
    assert resp.status_code in (401, 403)


@pytest.mark.asyncio
async def test_list_subscriptions_sin_auth_returns_401_o_403(client):
    """Sin auth valida -> el flujo de dependencies corta con 401/403."""
    resp = await client.get("/subscriptions/")
    assert resp.status_code in (401, 403)