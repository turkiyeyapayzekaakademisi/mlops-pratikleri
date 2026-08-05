from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.settings import RANDOM_STATE

def build_model(model_name: str, parameters: dict[str, Any]) -> Pipeline:

    if model_name == "logistic_regression":
        classifier = LogisticRegression(C = parameters["C"], max_iter=parameters["max_iter"], solver=parameters["solver"], random_state=RANDOM_STATE)

        return Pipeline(
            steps = [
                (
                    "imputer",
                    SimpleImputer(strategy="median")
                ),
                (
                    "scaler",
                    StandardScaler()
                ),
                (
                    "classifier",
                    classifier
                )
            ]
        )

    if model_name == "random_forest":
            classifier = RandomForestClassifier(n_estimators = parameters["n_estimators"], max_depth=parameters["max_depth"], min_samples_split = parameters["min_samples_split"], random_state=RANDOM_STATE)
    
            return Pipeline(
                steps = [
                    (
                        "imputer",
                        SimpleImputer(strategy="median")
                    ),
                    (
                        "classifier",
                        classifier
                    )
                ]
            )

    if model_name == "svm":
                classifier = SVC(C = parameters["C"], kernel=parameters["kernel"], gamma = parameters["gamma"], probability = True, random_state=RANDOM_STATE)
        
                return Pipeline(
                    steps = [
                        (
                            "imputer",
                            SimpleImputer(strategy="median")
                        ),
                        (
                            "scaler",
                            StandardScaler()
                        ),
                        (
                            "classifier",
                            classifier
                        )
                    ]
                )

    raise ValueError(f"Desteklenmeyen model: {model_name}")