Klasör Altyapısının Oluşturulması
    1. Proje klasörünün oluşturulmas
    2. git initialize
    3. klasörlerin oluşturulması
    4. venv oluşturulması
        python -m venv venv
        .\venv\Scripts\activate
    5. requirements.txt oluşturulması
        pip install -r requirements.txt
    6. .gitignore

Veri Setinin Python ile Yüklenmesi: 569 samples, 30 features, hedef değişken (0 ve 1)
    1. load_data.py oluştur ve çalıştır

Veri Ön İşleme Pipeline Oluşturma
    1. preprocessing.py

    2. Pipeline yapısının kontrol edilmesi
        python -c "from src.preprocessing import build_preprocessor; print(build_preprocessor())"

    3. pipeline adlarını kontrol et
        python -c "from src.preprocessing import build_preprocessor; print(build_preprocessor().named_steps.keys())"

    4. Ön işleme pipeline testi
        python -c "import pandas as pd; from src.preprocessing import build_preprocessor; df=pd.read_csv('data/processed/train.csv'); X = df.drop(columns=['target']); transformed=build_preprocessor().fit_transform(X); print(transformed.shape)"

Model Eğitim Scriptinin Yazılması
    1. data_loader.py
        python -c "from pathlib import Path; from src.data_loader import load_split; X, y = load_split(Path('data/processed/train.csv'), 'target'); print(X.shape); print(y.shape)"

    2. model.py dosyasını oluşturma
        python -c "from src.model import build_model_pipeline; print(build_model_pipeline())"

    3. train.py dosyasının oluşturulması

Model Parametrelerinin Config Dosyasından Alınması
    1. Config klasörü oluştur

    2. config_loader.py
        python -c "from src.config_loader import load_config; print(load_config())"

Modelin Eğitilmesi
    1. Modelin config değerleriyle eğitilmesi
        python -m src.train

    2. Eğitilen model bilgilerini görüntüle

    3. Tek kayıt üzerinden geçici bir tahmin kontrolü

    4. Eğitim süresinin ölçülmesi

Model Performansının Ölçülmesi
    1. evaluation.py dosyası oluşturma

    2. train.py a ekle
    
Validasyon ve Test Sonuçlarının Karşılaştırılması
    1. evaluation.py dosyasına fark hesaplama fonksiyonu ekle

Model Metriklerinin Kaydedilmesi
    1. evaluation.py bölümüme gerekli işlemlerin yapılması

Eğitilen Modelin Dosya Olarak Kaydedilmesi
    1. model.py güncelle

    2. train.py güncelle

    3. Kaydedilen pipeline adımlarını kontrol et
    python -c "from joblib import load; model=load('models/breast_cancer_pipeline.joblib'); print(model.named_steps.keys())"

Model Yükleme ve Tahmin Scriptinin Yazılması
    1. predict.py dosyasının oluşturulması

    2. tahmin scriptini çalıştır
    python -m src.predict --row 0

Bölüm Sonu Kontrol Listesi

    mlops-model-pratik projesi oluşturuldu.
    Klasör altyapısı hazırlandı.
    Sanal ortam oluşturuldu.
    Gerekli kütüphaneler kuruldu.

    Veri seti Python ile yüklendi.
    Train, validation ve test verileri oluşturuldu.
    Veri boyutları kontrol edildi.
    Ön işleme pipeline’ı oluşturuldu.
    SimpleImputer eklendi.
    StandardScaler eklendi.
    Veri yükleme modülü oluşturuldu.

    Model pipeline’ı oluşturuldu.
    Lojistik Regresyon modeli eklendi.
    Model eğitim scripti yazıldı.
    Config klasörü ve YAML dosyası oluşturuldu.
    Model parametreleri config dosyasına taşındı.
    Model train verisiyle eğitildi.
    Validation performansı ölçüldü.
    Test performansı ölçüldü.
    Validation ve test sonuçları karşılaştırıldı.
    Metrik farkları hesaplandı.
    Metrikler JSON dosyasına kaydedildi.

    Eğitilmiş pipeline Joblib dosyasına kaydedildi.
    Model dosyadan yeniden yüklendi.
    Test verisi üzerinde tahmin yapıldı.
    Projenin bütün dosyaları Git ile commit edildi.