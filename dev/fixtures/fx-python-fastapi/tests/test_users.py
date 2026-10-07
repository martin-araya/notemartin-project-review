"""Tests for the users feature (FEAT-001)."""
import pytest


@pytest.mark.asyncio
async def test_crear_usuario_valido_returns_201(auth_client):
    payload = {
        "email": "ana@example.com",
        "password": "secure123",
        "is_active": True,
    }
    resp = await auth_client.post("/users/", json=payload)
    assert resp.status_code == 201, resp.text
    assert resp.json()["email"] == "ana@example.com"


@pytest.mark.asyncio
async def test_obtener_usuario_inexistente_returns_404(auth_client):
    resp = await auth_client.get("/users/9999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_listar_usuarios_con_auth_returns_200(auth_client):
    resp = await auth_client.get("/users/")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_crear_usuario_email_invalido_returns_422(auth_client):
    """Email malformado (no es un email valido segun email-validator).

    Con Authorization Bearer valida, el validator corre y devuelve 422.
    """
    payload = {"email": "no-es-email", "password": "secure123", "is_active": True}
    resp = await auth_client.post("/users/", json=payload)
    assert resp.status_code == 422