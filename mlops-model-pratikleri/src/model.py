from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from src.preprocessing import build_preprocessor

from pathlib import Path
from joblib import dump

def build_model_pipeline(config: dict) -> Pipeline:

    preprocessing_config = config["preprocessing"]
    model_config = config["model"]

    preprocesser = build_preprocessor(imputer_strategy = preprocessing_config["imputer_strategy"])

    classifier = LogisticRegression(C = model_config["C"], max_iter = model_config["max_iter"], solver = model_config["solver"], random_state=model_config["random_state"], class_weight=model_config["class_weight"])

    return Pipeline(
        steps = [
            ("preprocesser", preprocesser),
            ("classifier", classifier)
        ]
    )

def save_model(model: Pipeline, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dump(model, output_path)