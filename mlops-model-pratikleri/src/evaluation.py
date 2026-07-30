import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline

import json
from pathlib import Path

METRIC_NAMES = [
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc"
]

def calculate_metrics(model: Pipeline, features: pd.DataFrame, target: pd.Series) -> dict:

    predictions = model.predict(features)
    probabilities = model.predict_proba(features)[:,1]

    return {
        "accuracy": round(float(accuracy_score(target, predictions)), 4),
        "precision": round(float(precision_score(target, predictions)), 4),
        "recall": round(float(recall_score(target, predictions)), 4),
        "f1": round(float(f1_score(target, predictions)),4),
        "roc_auc": round(float(roc_auc_score(target, probabilities)), 4),
        "confusion_matrix": confusion_matrix(target, predictions).tolist()
    }

def calculate_metric_gaps(validation_metrics: dict, test_metrics: dict) -> dict:

    return {
        metric_name: round(abs(validation_metrics[metric_name] - test_metrics[metric_name]), 4) for metric_name in METRIC_NAMES 
    }

def save_metrics(validation_metrics: dict, test_metrics: dict, metric_gaps: dict, output_path: Path) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)

    results = {
        "validation": validation_metrics,
        "test": test_metrics,
        "gaps": metric_gaps
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent = 4, ensure_ascii=False)