Klasör Altyapısının ve Proje Ortamının Oluşturulması
    1. mlops-mlflow-pratik
    2. git init
    3. src ve outputs
    4. venv
    5. requirements.txt
        pip install -r requirements.txt
    6. .gitignore
    7. init dosyası oluşturma    
    8. settings.py

MLflow Kurulumu ve Tracking Server'ın Çalıştırılması
    deney ve model metadatasını backend storage (sqlite db) da ve model ve dosya çıktılarını ise artifact storage (klasör) da saklar.
    1. mlflow versiyon
        mlflow --version
    2. Tracking Server çalıştırma
        mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db --artifacts-destination ./mlartifacts
    3. mlflow ui: http://127.0.0.1:5000

Experiment (Deney) Oluşturulması
    1. create_experiment.py dosyası oluşturma

    2. create_experiment çalıştırma
        python -m src.create_experiment

Deney için Data, Model ve Değerlendirme Oluşturulması
    1. data.py dosyasının oluşturulması ve test edilmesi
        python -c "from src.data import load_and_split_data; X_train, X_val, X_test, y_train, y_val, y_test=load_and_split_data(); print(X_train.shape); print(X_val.shape); print(X_test.shape)"
    
    2. model_factory.py dosyasının oluşturulması

    3. Değerlendirme Kodunun Hazırlanması
        evaluation.py dosyasının oluşturulması 

Model Parametrelerinin Kaydedilmesi
    1. run_experiment.py dosyasının oluşturulması

    2. Scriptin sonuna CLI yapısını ekleme
        python -m src.run_experiment

Model Metriklerinin Kaydedilmesi
    1. run_experiment.py içerisine ekle
        python -m src.run_experiment --run-name logistic-regression-c1-metrics

Model Dosyalarının Artifact Olarak Kaydedilmesi
    1. run_experiment.py güncellemesi yap
        python -m src.run_experiment --run-name logistic-regression-complete

Farklı Model Deneylerinin Çalıştırılması
    1. Deney listesi:
        LR: C = 0.1
        LR: C = 1
        LR: C = 10
        RF: 100 
        RF: 300
        SVM: C = 1
        SVM: C = 10
    2. run_all_experiments.py 
        python -m src.run_all_experiments

Deney Sonuçlarının MLflow UI Üzerinden Karşılaştırılması
    1. MLflow UI: http://127.0.0.1:5000

En Başarılı Modelin Belirlenmesi
    1. test_f1 e göre model seçimi gerçekleştir

    2. select_best_run.py dosyası oluşturma
        python -m src.select_best_run

MLflow Model Registry Kullanımı
    1. register_best_model.py dosyası oluşturma
        python -m src.register_best_model

Model Versiyonlarının Oluşturulması
    1. register_model_version.py dosyası oluşturulması
        python -m src.register_model_versions
    
Modelin Üretim için Onaylanması
    1. approve_model.py dosyasını oluşturma
        python -m src.approve_model

Champion Model ile Tahmin Yapma
    1. predict_champion.py dosyasını oluşturma
        python -m src.predict_champion

Bölüm Sonu Kontrol Listesi
    mlops-mlflow-pratik projesi oluşturuldu.
    Git repository başlatıldı.
    Sanal ortam oluşturuldu.
    MLflow ve gerekli kütüphaneler kuruldu.
    Tracking Server SQLite backend ile çalıştırıldı.
    Yerel artifact deposu oluşturuldu.
    MLflow UI açıldı.
    Experiment oluşturuldu.
    Experiment tag’leri kaydedildi.
    Model parametreleri MLflow’a kaydedildi.
    Validation metrikleri kaydedildi.
    Test metrikleri kaydedildi.
    Eğitim süresi kaydedildi.
    Model MLflow artifact’ı olarak kaydedildi.
    Model signature oluşturuldu.
    Confusion matrix dosyaları artifact olarak kaydedildi.
    Metrik özeti JSON artifact’ı oluşturuldu.
    Farklı model ve parametre deneyleri çalıştırıldı.
    Run sonuçları MLflow UI’da karşılaştırıldı.
    Run’lar seçim metriğine göre sıralandı.
    En başarılı run belirlendi.
    En başarılı run bilgisi JSON dosyasına kaydedildi.
    Registered model oluşturuldu.
    Ek model versiyonları oluşturuldu.
    Model version tag’leri eklendi.
    Üretime onaylanan model belirlendi.
    Champion alias’ı atandı.
    Champion model Registry üzerinden yüklendi.
    Champion model ile tahmin yapıldı.
    Proje kodları Git ile commit edildi.