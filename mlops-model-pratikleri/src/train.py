from pathlib import Path
import pandas as pd

from src.data_loader import load_split
from src.model import build_model_pipeline, save_model
from src.config_loader import load_config

from time import perf_counter

from src.evaluation import calculate_metrics, calculate_metric_gaps, save_metrics

def main() -> None:

    config = load_config()
    data_config = config["data"]
    target_column = data_config["target_column"] 

    train_features, train_target = load_split(Path(data_config["train_path"]), target_column)

    validation_features, validation_target = load_split(Path(data_config["validation_path"]), target_column)

    test_features, test_target = load_split(Path(data_config["test_path"]), target_column)

    model = build_model_pipeline(config)

    start_time = perf_counter()
    model.fit(train_features, train_target)
    training_time = perf_counter() - start_time

    classifier = model.named_steps["classifier"]
    print(f"Model sınıfları: {classifier.classes_}")
    print(f"Katysayı boyutu: {classifier.coef_.shape}")

    sample_prediction = model.predict(validation_features.iloc[[0]])
    print(f"Örnek tahmin: {sample_prediction[0]}")

    print(f"Eğitim süresi: {training_time:.4f} saniye")

    # validation
    validation_metrics = calculate_metrics(model, validation_features, validation_target)
    print("Validation Metrikleri")

    for metric_name, metric_value in validation_metrics.items():
        print(f"{metric_name}: {metric_value}")

    # test
    test_metrics = calculate_metrics(model, test_features, test_target)

    # metrik farklarını hesaplama
    metric_gaps = calculate_metric_gaps(validation_metrics, test_metrics)

    print_comparison(validation_metrics, test_metrics)
    print()
    print("Validation ve test farkları")

    for metric_name, metric_value in metric_gaps.items():
        print(f"{metric_name}: {metric_value}")

    # metrics save
    metrics_path = Path(config["outputs"]["metrics_path"])
    save_metrics(validation_metrics, test_metrics, metric_gaps, metrics_path)

    # model save
    model_path = Path(config["outputs"]["model_path"])

    save_model(model, model_path)

    print("Eğitim gerçekleşti.")

def print_comparison(validation_metrics: dict, test_metrics: dict) -> None:
    comparison = pd.DataFrame(
        {
            "validation": {
                key: value
                for key, value
                in validation_metrics.items()
                if key != "confusion_matrix"
            },
            "test": {
                key: value
                for key, value
                in test_metrics.items()
                if key != "confusion_matrix"
            },
        }
    ).T

    print(comparison)

if __name__ == "__main__":
    main()
