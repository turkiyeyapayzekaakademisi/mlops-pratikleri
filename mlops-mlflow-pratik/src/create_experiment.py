import mlflow
from mlflow import MlflowClient

from src.settings import EXPERIMENT_NAME, TRACKING_URL

def main() -> None:
    mlflow.set_tracking_uri(TRACKING_URL)

    client = MlflowClient()

    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)

    if experiment is None:
        experiment_id = client.create_experiment(
            name = EXPERIMENT_NAME,
            tags = {
                "project": "mlops-mlflow-pratik",
                "task": "binary-classification",
                "dataset": "breast-cancer-wisconsin"
            }
        )

        print("Experiment oluşturuldu")
        print(f"Experiment id: {experiment_id}")
        print(f"Experiment adı: {EXPERIMENT_NAME}")

        return

    print("Experiment zaten mevcut.")
    print(f"Experiment id: {experiment.experiment_id}")
    print(f"Experiment adı: {experiment.name}")

if __name__ == "__main__":
    main()