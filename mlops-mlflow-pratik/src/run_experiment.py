import argparse
from time import perf_counter
from typing import Any

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

from src.data import load_and_split_data
from src.evaluation import calculate_metrics, save_confusion_matrix, save_metrics_summary
from src.model_factory import build_model
from src.settings import EXPERIMENT_NAME, RANDOM_STATE, TEST_SIZE, TRACKING_URL, VALIDATION_SIZE

from pathlib import Path
from tempfile import TemporaryDirectory

from mlflow.models import infer_signature

def normalize_parameters(parameters: dict[str, Any]) -> dict[str, str | int | float | bool]:

    normalized = {}

    for key, value in parameters.items():
        if value is None:
            normalized[key] = "None"
        else:
            normalized[key] = value

    return normalized

def run_experiment(run_name: str, model_name: str, model_parameters: dict[str, Any]) -> str:

    mlflow.set_tracking_uri(TRACKING_URL)
    mlflow.set_experiment(EXPERIMENT_NAME)

    train_features, validation_features, test_features, train_target, validation_target, test_target = load_and_split_data()

    model = build_model(model_name=model_name, parameters=model_parameters)

    with mlflow.start_run(run_name = run_name) as run:
        logged_parameters = {
            "model_name": model_name,
            "random_state": RANDOM_STATE,
            "test_size": TEST_SIZE,
            "validation_size": VALIDATION_SIZE,
            "train_samples": len(train_features),
            "validation_samples": len(validation_features),
            "test_samples": len(test_features),
            **model_parameters,
        }

        mlflow.log_params(normalize_parameters(logged_parameters))

        mlflow.set_tags(
            {
                "project": ("mlops-mlflow-pratik"),
                "task": ("binary-classification"),
                "dataset": ("breast-cancer-wisconsin"),
                "model_family": model_name
            }
        )

        # training
        start_time = perf_counter()
        model.fit(train_features, train_target)
        training_time = perf_counter() - start_time

        # değerlendirme metriklerinin hesaplanması
        validation_metrics = calculate_metrics(model=model, features=validation_features, target=validation_target, prefix="validation")
        test_metrics = calculate_metrics(model=model, features=test_features, target=test_target,prefix="test")

        # eğitim süresini metriklere ekleme
        runtime_metrics = {
            "training_time_seconds": float(training_time)
        }

        # metrikleri mlflow a kaydetme
        all_metrics = {**validation_metrics, **test_metrics, ** runtime_metrics}
        mlflow.log_metrics(all_metrics)

        # model imzası oluşturma
        signature = infer_signature(train_features, model.predict(train_features))

        # modeli mlflow model artifcat olarak kaydet
        model_info = mlflow.sklearn.log_model(sk_model=model, name = "model", signature=signature, input_example=train_features.head(3), serialization_format="cloudpickle")

        # artifact klasörü oluştur
        with TemporaryDirectory() as temp_directory:
            artifact_directory = Path(temp_directory)

            validation_matrix_path = (
                artifact_directory
                / "validation_confusion_matrix.png"
            )

            test_matrix_path = (
                artifact_directory
                / "test_confusion_matrix.png"
            )

            metrics_summary_path = (
                artifact_directory
                / "metrics_summary.json"
            )

            # confusion matrix dosyalarını oluşturma
            save_confusion_matrix(model=model, features=validation_features, target=validation_target,output_path=validation_matrix_path, title = "validasyon confusion matrix")
            save_confusion_matrix(model=model, features=test_features, target= test_target, output_path=test_matrix_path, title = "test confusion matrix")

            # metric özetini oluşturma
            save_metrics_summary(parameters=logged_parameters, validation_metrics=validation_metrics, test_metrics=test_metrics, output_path=metrics_summary_path)

            # dosyaları mlflow'a gönder
            mlflow.log_artifacts(local_dir=str(artifact_directory), artifact_path="reports")

        # model uri bilgisini tag olarak kaydetme
        mlflow.set_tag("logged_model_uri", model_info.model_uri)

        # run id ve model uri bilgisini yazdırma
        print(f"Model uri: {model_info.model_uri}")


        print("Run oluşturuldu")
        print(f"Run id: {run.info.run_id}")
        print(f"Run name: {run_name}")
        print(f"Model: {model_name}")
        print(f"Eğitim süresi: {training_time} saniye")

        # metrikleri terminale yazdır
        print("validation metrikleri")
        for key, value in validation_metrics.items():
            print(f"{key}: {value:.3f}")

        print("Test metrikleri")
        for key, value in test_metrics.items():
            print(f"{key}: {value:.3f}")
                
        return run.info.run_id

def main() -> None:

    parser = argparse.ArgumentParser(description="Tek bir mlflow deneyi çalıştırır")

    parser.add_argument("--run-name", default="logistic-regression-c1")

    parser.add_argument("--model-name", default="logistic_regression", choices=["logistic_regression", "random_forest", "svm"])

    arguments = parser.parse_args()

    parameters = {
        "C": 1,
        "max_iter": 1000,
        "solver": "lbfgs" 
    }

    run_experiment(run_name=arguments.run_name, model_name=arguments.model_name, model_parameters=parameters)

if __name__ == "__main__":
    main()