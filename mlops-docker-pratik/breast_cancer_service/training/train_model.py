from pathlib import Path
from joblib import dump
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# temel ayarlar
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "breast_cancer_model.joblib"
TEST_SIZE = 0.2
RANDOM_STATE = 42

def main():

    # veri setini yükle
    dataset = load_breast_cancer(as_frame=True)

    # girdiler ve hedefler
    features = dataset.data
    target = dataset.target

    # train test split
    train_features, test_features, train_target, test_target = train_test_split(features, target, test_size=TEST_SIZE, random_state=RANDOM_STATE)

    # model pipeline oluşturma
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression())
        ]
    )

    # modeli eğit
    model.fit(train_features, train_target)

    # test tahminlerini üret
    predictions = model.predict(test_features)

    # accuracy değeri hesapla
    accuracy = accuracy_score(test_target, predictions)

    # model paketi oluştur
    model_bundle = {
        "model": model,
        "feature_names": dataset.feature_names.tolist(),
        "target_names": dataset.target_names.tolist(),
        "model_version": "1.0.0",
        "accuracy": accuracy
    }

    # artifact klasörünü oluştur
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # modeli kaydet
    dump(model_bundle, MODEL_PATH)

    print(f"train: {len(train_features)}")
    print(f"test: {len(test_features)}")
    print(f"accuracy: {accuracy}")
    print("model kaydedildi")

if __name__ == "__main__":
    main()

