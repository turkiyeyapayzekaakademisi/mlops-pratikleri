import json
from pathlib import Path

import mlflow

from src.settings import EXPERIMENT_NAME, SELECTION_METRIC, TRACKING_URL

BEST_RUN_PATH = Path("outputs/best_run.json")

RANKED_RUNS_PATH = Path("outputs/ranked_runs.json")

def clean_value(value):
    if value != value:
        return None

    return value

def main() -> None:

    mlflow.set_tracking_uri(TRACKING_URL)

    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    if experiment is None:
        raise RuntimeError(f"Experiment bulunamadı: {EXPERIMENT_NAME}")

    runs = mlflow.search_runs(
        experiment_ids=[
            experiment._experiment_id
        ],
        filter_string=(
            f"metrics.{SELECTION_METRIC} >= 0"  
        ),
        order_by = [
            f"metrics.{SELECTION_METRIC} DESC"
        ],
    )

    if runs.empty:
        raise RuntimeError("Karşılaştırılacak run bulunamadı")

    ranked_runs = []

    for rank, (_, row) in enumerate(runs.iterrows(), start=1):

        run_data = {
            "rank": rank,
            "run_id": row["run_id"],
            "run_name": clean_value(row.get("tags.mlflow.runName")),
            "model_name": clean_value(row.get("params.model_name")),
            "validation_f1": clean_value(row.get("metrics.validation_f1")),
            "test_f1": clean_value(row.get("metrics.test_f1")),
            "test_recall": clean_value(row.get("metrics.test_recall")),
            "test_roc_auc": clean_value(row.get("metrics.test_roc_auc")),
            "model_uri": f"runs:/{row["run_id"]}/model"
        }   

        ranked_runs.append(run_data)

    best_run = ranked_runs[0]

    BEST_RUN_PATH.parent.mkdir(parents=True, exist_ok=True)

    with BEST_RUN_PATH.open("w", encoding="utf-8") as file:
        json.dump(best_run, file, indent=4, ensure_ascii=False)     

    with RANKED_RUNS_PATH.open("w", encoding="utf-8") as file:
        json.dump(ranked_runs, file, indent=4, ensure_ascii=False)

    print("En başarılı run belirlendi")
    print(f"Run id: {best_run["run_id"]}")
    print(f"Model: {best_run["model_name"]}")
    print(f"Test f1: {best_run["test_f1"]}")

if __name__ == "__main__":
    main()