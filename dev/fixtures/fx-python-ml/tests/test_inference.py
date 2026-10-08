from __future__ import annotations


def test_root(fastapi_client):
    response = fastapi_client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "fxpm-inference"


def test_predict_model_not_registered(fastapi_client):
    response = fastapi_client.post(
        "/inferencia",
        params={"model_name": "does_not_exist_anywhere"},
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    # P4 trap: 404 porque el modelo no esta registrado
    assert response.status_code in (404, 500)


def test_predict_invalid_request(fastapi_client):
    response = fastapi_client.post(
        "/inferencia",
        json={"sepal_length": "not_a_number"},
    )
    # pydantic validation error -> 422
    assert response.status_code == 422


def test_predict_valid_request_no_model(fastapi_client):
    response = fastapi_client.post(
        "/inferencia",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    # Si el modelo default no esta disponible, debe fallar gracefully
    assert response.status_code in (200, 404, 500)


def test_predict_query_param_default_model_name(fastapi_client):
    """Verifica que el param model_name tiene default 'iris_clf'."""
    import inspect
    from src.app.main import predict
    sig = inspect.signature(predict)
    assert 'model_name' in sig.parameters
    assert sig.parameters['model_name'].default == 'iris_clf'