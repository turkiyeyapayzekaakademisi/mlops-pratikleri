from pathlib import Path

from joblib import dump

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_PATH = Path("artifacts/iris_classifier.joblib")

FEATURES_NAMES = [
    "sepal_length_cm",
    "sepal_width_cm",
    "petal_length_cm",
    "petal_width_cm"
]

RANDOM_STATE = 42
TEST_SIZE = 0.2

def train_and_save_model() -> dict[str, object]:

    dataset = load_iris(as_frame=True)

    features = dataset.data.copy()
    features.columns = FEATURES_NAMES

    target = dataset.target.copy()

    train_features, test_features, train_target, test_target = train_test_split(features, target, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=target)

    model = Pipeline(
        steps=[
            (
                "scaler", StandardScaler()
            ),
            (
                "classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
            )
        ]
    )

    model.fit(train_features, train_target)

    predictions = model.predict(test_features)

    test_accuracy = accuracy_score(test_target, predictions)

    model_bundle = {
        "model": model,
        "feature_names": FEATURES_NAMES,
        "class_names": dataset.target_names.tolist(),
        "model_version": "1.0.0",
        "test_accuracy": test_accuracy
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    dump(model_bundle, MODEL_PATH)

    return {
        "model_path": str(MODEL_PATH),
        "model_version": "1.0.0",
        "test_accuracy": test_accuracy,
        "train_samples": len(train_features),
        "test_samples": len(test_features)
    }

def main() -> None:

    result = train_and_save_model()

    print("Model eğitimi tamamlandı")

    print(result)

if __name__ == "__main__":
    main()