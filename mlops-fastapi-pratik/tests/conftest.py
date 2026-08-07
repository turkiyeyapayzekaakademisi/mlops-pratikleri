import pytest
from fastapi.testclient import TestClient

from app.main import app
from training.train_model import MODEL_PATH, train_and_save_model

@pytest.fixture(scope="session")
def client():

    if not MODEL_PATH.exists():
        train_and_save_model()

    with TestClient(app) as test_client:
        yield test_client