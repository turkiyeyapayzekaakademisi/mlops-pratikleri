# Dosya yollarını oluşturmak için Path sınıfını içe aktar
from pathlib import Path

# Eğitilen modeli dosyaya kaydetmek için dump fonksiyonunu içe aktar
from joblib import dump

# Iris veri setini yüklemek için load_iris fonksiyonunu içe aktar
from sklearn.datasets import load_iris

# Challenger model olarak Random Forest kullan
from sklearn.ensemble import RandomForestClassifier

# Model başarısını ölçmek için accuracy_score fonksiyonunu içe aktar
from sklearn.metrics import accuracy_score

# Veriyi train ve test olarak ayırmak için train_test_split fonksiyonunu içe aktar
from sklearn.model_selection import train_test_split


# Temel ayarlar
BASE_DIR = Path(__file__).resolve().parent.parent

# Challenger modelin kaydedileceği dosya yolunu belirle
MODEL_PATH = BASE_DIR / "artifacts" / "challenger_model.joblib"

# Verinin yüzde 20'sini test için ayır
TEST_SIZE = 0.20

# Sonuçların tekrar üretilebilir olmasını sağla
RANDOM_STATE = 42


def load_dataset():
    # Iris veri setini yükle
    dataset = load_iris(as_frame=True)

    # Girdileri ve hedef değerleri al
    features = dataset.data
    target = dataset.target
    target_names = dataset.target_names.tolist()

    # Veri seti bilgilerini döndür
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
    # Challenger olarak Random Forest modelini oluştur
    return RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=RANDOM_STATE,
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
        "model_version": "2.0.0",
        "accuracy": accuracy,
    }

    # Challenger model paketini kaydet
    dump(model_bundle, model_path)


def train_and_save_model(model_path=MODEL_PATH):
    # Veri setini yükle
    features, target, target_names = load_dataset()

    # Veriyi train ve test olarak böl
    train_features, test_features, train_target, test_target = split_dataset(
        features,
        target,
    )

    # Challenger modeli oluştur
    model = create_model()

    # Challenger modeli eğit
    model.fit(train_features, train_target)

    # Challenger model performansını hesapla
    accuracy = evaluate_model(
        model,
        test_features,
        test_target,
    )

    # Challenger modeli kaydet
    save_model(
        model=model,
        feature_names=features.columns.tolist(),
        target_names=target_names,
        accuracy=accuracy,
        model_path=model_path,
    )

    # Eğitim sonucunu döndür
    return {
        "accuracy": accuracy,
        "model_path": model_path,
    }


def main():
    # Challenger model eğitim sürecini çalıştır
    result = train_and_save_model()

    # Eğitim sonucunu terminalde göster
    print("--- Challenger Model ---")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"Model kaydedildi: {result['model_path']}")


if __name__ == "__main__":
    # Dosya doğrudan çalıştırıldığında eğitim sürecini başlat
    main()