from pathlib import Path
from joblib import dump

from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import r2_score 
from sklearn.model_selection import train_test_split 

# temel ayarlar
BASE_DIR = Path(__file__).resolve.parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "diabetes_model.joblib"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# veri seti yükle
def load_dataset():

    dataset = load_diabetes(as_frame=True, scaled=False)

    # girdiler ve hedefler
    features = dataset.data.copy()
    target = dataset.target.copy()

    return features, target

# train test ayrımı
def split_dataset(features, target):

    return train_test_split(features, target, test_size= TEST_SIZE, random_state= RANDOM_STATE)

# model oluşturma
def create_model():
    model = RandomForestRegressor(n_estimators=300, max_depth=5, min_samples_split=4, random_state=RANDOM_STATE, n_jobs=-1)

    return model

# save model
def save_model(model, feature_names, r2):

    # artifact klasörü oluştur
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # model paketini hazırla
    model_bundle = {
        "model": model,
        "feature_names": feature_names,
        "model_version": "1.0.0",
        "r2_score": r2
    }

    # modeli kaydet
    dump(model_bundle, MODEL_PATH)

def main():

    # veri setini yükle
    features, target = load_dataset()
    print("Veri seti")
    print(f"Kayıt sayısı: {len(features)}")
    print(f"Özellik sayısı: {features.shape[1]}")
    print(f"Özellikler: {features.columns.tolist()}")

    # train test ayrımı
    train_features, test_features, train_target, test_target = split_dataset(features, target)
    print(f"train_features: {len(train_features)}")
    print(f"test_features: {len(test_features)}")

    # modeli oluştur
    model = create_model()

    # modeli eğit
    model.fit(train_features, train_target)

    # test verisi üzerinde tahmin yap
    predictions = model.predict(test_features)

    # r2 skor hesapla
    r2 = r2_score(test_target, predictions)
    print(f"r2: {r2}")

    # modeli kaydet
    save_model(model, features.columns.tolist(), r2)
    print("model kaydedildi")

if __name__ == "__main__":
    main()

