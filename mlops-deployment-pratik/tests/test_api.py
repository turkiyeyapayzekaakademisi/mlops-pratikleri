import pytest
from fastapi.testclient import TestClient

from app import main as app_main
from training.train_model import train_and_save_model


@pytest.fixture
def client(tmp_path, monkeypatch):

    # test için geçici model yolu oluştur
    test_model_path = tmp_path / "iris_model.joblib"

    # test modeli oluştur
    train_and_save_model(test_model_path)

    # API'nin geçici modeli kullanmasını sağla
    monkeypatch.setattr(app_main, "MODEL_PATH", test_model_path)

    # test istemcisini oluştur
    return TestClient(app_main.app)


def test_root_endpoint(client):

    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint(client):

    response = client.get("/health")

    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["accuracy"] >= 0.8


def test_predict_endpoint(client):

    request_data = {
        "sepal_length": 5,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    response = client.post("/predict", json=request_data)

    data = response.json()

    assert response.status_code == 200
    assert data["prediction"] in [0, 1, 2]


def test_predict_validation(client):

    request_data = {
        "sepal_length": 5,
        "sepal_width": 3.5,
        "petal_length": 1.4,
    }

    response = client.post("/predict", json=request_data)

    assert response.status_code == 422
