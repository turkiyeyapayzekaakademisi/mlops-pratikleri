from pathlib import Path

from joblib import dump
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Temel ayarlar
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "iris_model.joblib"
TEST_SIZE = 0.20
RANDOM_STATE = 42


def load_dataset():
    # Iris veri setini yükle
    dataset = load_iris(as_frame=True)

    # Girdileri ve hedef değerleri al
    features = dataset.data
    target = dataset.target
    target_names = dataset.target_names.tolist()

    return features, target, target_names


def split_dataset(features, target):
    # Train-test ayrımı yap
    return train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=target,
    )


def create_model():
    # Ölçekleme ve modeli tek pipeline içerisinde oluştur
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=500,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def evaluate_model(model, test_features, test_target):
    # Test verisi üzerinde tahmin yap
    predictions = model.predict(test_features)

    # Accuracy değerini hesapla
    return accuracy_score(test_target, predictions)


def save_model(model, feature_names, target_names, accuracy, model_path):
    # Model klasörünü oluştur
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Model paketini hazırla
    model_bundle = {
        "model": model,
        "feature_names": feature_names,
        "target_names": target_names,
        "model_version": "1.0.0",
        "accuracy": accuracy,
    }

    # Model paketini kaydet
    dump(model_bundle, model_path)


def train_and_save_model(model_path=MODEL_PATH):
    # Veri setini yükle
    features, target, target_names = load_dataset()

    # Veriyi böl
    train_features, test_features, train_target, test_target = split_dataset(
        features,
        target,
    )

    # Modeli oluştur ve eğit
    model = create_model()
    model.fit(train_features, train_target)

    # Model performansını hesapla
    accuracy = evaluate_model(
        model,
        test_features,
        test_target,
    )

    # Modeli kaydet
    save_model(
        model=model,
        feature_names=features.columns.tolist(),
        target_names=target_names,
        accuracy=accuracy,
        model_path=model_path,
    )

    return {
        "accuracy": accuracy,
        "model_path": model_path,
    }


def main():
    # Model eğitim sürecini çalıştır
    result = train_and_save_model()

    print("--- Iris Model ---")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"Model kaydedildi: {result['model_path']}")


if __name__ == "__main__":
    main()
