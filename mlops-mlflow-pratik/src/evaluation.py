import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline

def calculate_metrics(model: Pipeline, features: pd.DataFrame, target: pd.Series, prefix: str) -> dict[str, float]:

    predictions = model.predict(features)

    probabilities = model.predict_proba(features)[:, 1]

    return {
        f"{prefix}_accuracy": float(accuracy_score(target, predictions)),
        f"{prefix}_precision": float(precision_score(target, predictions)),
        f"{prefix}_recall": float(recall_score(target, predictions)),
        f"{prefix}_f1": float(f1_score(target, predictions)),
        f"{prefix}_roc_auc": float(roc_auc_score(target, predictions)),
    }

def save_confusion_matrix(model: Pipeline, features = pd.DataFrame, target = pd.Series, output_path = Path, title = str) -> None:
    predictions = model.predict(features)

    matrix = confusion_matrix(target, predictions)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize= (6,6))

    display = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=["benign", "malignant"])

    display.plot(ax=axis, values_format="d")

    axis.set_title(title)

    figure.tight_layout()

    figure.savefig(output_path)

    plt.close()

def save_metrics_summary(parameters: dict, validation_metrics: dict, test_metrics: dict, output_path: Path) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = {
        "parameters": parameters,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)