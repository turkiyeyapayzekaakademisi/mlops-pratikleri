import pytest
from fastapi.testclient import TestClient

SETOSA_PAYLOAD = {
    "sepal_length_cm": 5.1,
    "sepal_width_cm": 3.5,
    "petal_length_cm": 1.4,
    "petal_width_cm": 0.5
}

VERSICOLOR_PAYLOAD = {
    "sepal_length_cm": 6,
    "sepal_width_cm": 2.9,
    "petal_length_cm": 4.5,
    "petal_width_cm": 1.5
}

VIRGINICA_PAYLOAD = {
    "sepal_length_cm": 6.5,
    "sepal_width_cm": 3,
    "petal_length_cm": 5.8,
    "petal_width_cm": 2.2
}

def test_root_endpoint(client: TestClient) -> None:

    response = client.get("/")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "running"

def test_health_endpoint(client: TestClient) -> None:

    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["model_ready"] is True
    assert body["model_version"] == "1.0.0"

def test_single_prediction(client:TestClient) -> None:

    response = client.post("/predict", json=SETOSA_PAYLOAD)
    assert response.status_code == 200

    body = response.json()
    assert body["model_version"] == "1.0.0"
    assert body["predicted_class"] == 0
    assert body["predicted_label"] == "setosa"

    assert set(
        body["probabilities"].keys()
    ) == {
        "setosa",
        "versicolor",
        "virginica"
    }

    probability_total = sum(body["probabilities"].values())
    assert probability_total == pytest.approx(1.0, abs = 0.001)

def test_negative_value_returns_422(client: TestClient) -> None:

    invalid_payload = {
        **SETOSA_PAYLOAD,
        "sepal_length_cm": -1
    }  

    response = client.post("/predict", json = invalid_payload)
    assert response.status_code == 422

    body = response.json()
    assert body["error"] == "VALIDATION_ERROR"

def test_missing_field_returns_422(client:TestClient) -> None:

    invalid_payload = {
        "sepal_length_cm": 5.1,
        "sepal_width_cm": 3.5,
        "petal_length_cm": 1.4,
    }

    response = client.post("/predict", json = invalid_payload)
    assert response.status_code == 422

def test_extra_field_returns_422(client:TestClient) -> None:

    invalid_payload = {
        **SETOSA_PAYLOAD,
        "kcy": 5
    }  

    response = client.post("/predict", json = invalid_payload)
    assert response.status_code == 422

def test_batch_prediction(client: TestClient) -> None:

    response = client.post("/predict/batch", json = {
        "items": [
            SETOSA_PAYLOAD, VERSICOLOR_PAYLOAD, VIRGINICA_PAYLOAD
        ]
    })

    assert response.status_code == 200

    body = response.json()
    assert body["total"] == 3
    assert len(body["predictions"]) == 3

    assert [item["input_index"] for item in body["predictions"] == [0, 1, 2]]

def test_empty_batch_returns_422(client: TestClient) -> None:

    response = client.post("/predict/batch", json = {"items": []})
    assert response.status_code == 422

def test_unknown_endpoint_returns_404(client: TestClient) -> None:

    response = client.get("/unknown-endpoint")
    assert response.status_code == 404

    