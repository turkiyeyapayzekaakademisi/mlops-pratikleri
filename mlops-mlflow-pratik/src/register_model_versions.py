import json
from pathlib import Path

import mlflow

from mlflow import MlflowClient

from src.settings import REGISTERED_MODEL_NAME, TRACKING_URL

RANKED_RUN_PATH = Path("outputs/ranked_runs.json")

MAX_VERSION_COUNT = 3

def main() -> None:
    mlflow.set_tracking_uri(TRACKING_URL)

    if not RANKED_RUN_PATH.exists():
        raise FileNotFoundError("ranhed_runs.json bulunamadı")

    with RANKED_RUN_PATH.open("r", encoding="utf-8") as file:
        ranked_runs = json.load(file)

    client = MlflowClient()

    existing_version = (
        client.search_model_versions(filter_string=(f"name='{REGISTERED_MODEL_NAME}'"))
    )

    registered_run_ids = {
        version.run_id for version in existing_version if version.run_id
    }

    created_versions = []

    for run_data in ranked_runs[:MAX_VERSION_COUNT]:

        run_id = run_data["run_id"]

        if run_id in registered_run_ids:
            print(f"run zaten kayıtlı: {run_id}")
            continue

        model_version = mlflow.register_model(model_uri=run_data["model_uri"], name = REGISTERED_MODEL_NAME)

        client.set_model_version_tag(name=REGISTERED_MODEL_NAME, version=model_version.version, key = "ranking", value=str(run_data["rank"]))
        client.set_model_version_tag(name=REGISTERED_MODEL_NAME, version=model_version.version, key = "model_family", value=run_data["model_name"])
        client.set_model_version_tag(name = REGISTERED_MODEL_NAME, version=model_version.version, key = "validation_status", value = "pending")
        client.update_model_version(name=REGISTERED_MODEL_NAME, version=model_version.version, description=(
            f"deney sıralaması"
            f"{run_data["rank"]}. model"
        ))

        created_versions.append(model_version.version)

        registered_run_ids.add(run_id)      

        print("versiyon oluşturuldu")

    if not created_versions:
        print("yeni model versiyonu oluşturulmadı")

if __name__ == "__main__":
    main()  