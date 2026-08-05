import json
from pathlib import Path

import mlflow
from mlflow import MlflowClient

from src.settings import REGISTERED_MODEL_NAME, TRACKING_URL

BEST_RUN_PATH = Path("outputs/best_run.json")

def main() -> None:

    mlflow.set_tracking_uri(TRACKING_URL)

    if not BEST_RUN_PATH.exists():
        raise FileNotFoundError("best_run.json dosyası bulunamadı.")

    with BEST_RUN_PATH.open("r", encoding = "utf-8") as file:
        best_run = json.load(file)

    model_uri = best_run["model_uri"]

    model_version = mlflow.register_model(model_uri=model_uri, name=REGISTERED_MODEL_NAME)

    client = MlflowClient()

    client.set_registered_model_tag(name=REGISTERED_MODEL_NAME, key = "task", value = "binary-classification")
    client.set_registered_model_tag(name=REGISTERED_MODEL_NAME, key = "dataset", value = "breast-cancer-wisconsin")
    client.set_model_version_tag(name=REGISTERED_MODEL_NAME, version=model_version.version, key = "selection_metric", value = "test_f1")
    client.set_model_version_tag(name=REGISTERED_MODEL_NAME, version=model_version.version, key = "validation_status", value="pending")
    client.update_model_version(name=REGISTERED_MODEL_NAME, version=model_version.version, description=(
        "MLflow deney karşılaştırması "
        f" test_f1: {best_run["test_f1"]}"
    ))

    print("Model regitry kaydı tamamlandı")
    print(f"Registered model: {REGISTERED_MODEL_NAME}")
    print(f"Model version: {model_version.version}")
    print(f"kaynak run: {best_run["run_id"]}")

if __name__ == "__main__":
    main()

