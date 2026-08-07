FastAPI Kurulumu ve Klasör Altyapısı Oluşturma
    1. Proje klasörü oluştur
    2. git init
    3. Proje klasörleri oluşturma
    4. Sanal ortam oluşturma
    5. requirements.txt oluşturma
    6. .gitignore yazılması

İlk FastAPI Uygulamasının Oluşturulması
    1. main.py oluşturulması
    2. FastAPI uygulamasının çalıştırılması
        fastapi dev app/main.py
        swagger: http://127.0.0.1:8000/docs
        fastapi: http://127.0.0.1:8000/redoc

ML Model Oluşturma
    1. train_model.py
        python -m training.train_model

Modelin API İçerisine Yüklenmesi
    1. model_service.py oluşturma
    2. main.py güncelleme
        fastapi dev app/main.py

Prediction Endpointinin Oluşturulması
    1. model_service.py içerisine tahmin fonksiyonu eklenmesi

    2. main.py içerisine geçici prediction endpointi ekleme

Request Veri Modelinin Hazırlanması
    1. schemas.py dosyasının oluşturulması

    2. oluşuturulan şemayı main.py tarafında içeriye aktar

Pydantic ile Veri Doğrulama
    1. schemas.py dosyasını güncelle

Response Modelinin Oluşturulması
    1. schemas.py dosyasına response modelini ekle

    2. main.py bölümüne response şemasının eklenmesi

Tekli Tahmin Endpoint Güncelleme
    1. schemas.py dosyasına health response modelinin eklenmesi

Toplu Tahmin Endpoint Oluşturma
    1. schemas.py dosyasına batch modellerinin eklenmesi

    2. model_service.py dosyasına toplu tahmin fonksiyonunu ekler

Hata Yönetimi ve HTTP Status Kodların Tanımlanması
    1. 200, 404, 422, 500, 503 
    
    2. errors.py dosyasının oluşturulması

    3. schemas.py dosyasına hata response modelinin eklenmesi

    4. model_service.py dosyasının hata yönetimi ile güncellenmesi

Pytest ile Otomatik API Testleri
    1. pytest.ini
    2. conftest.py dosyası oluşturma
    3. test_api.py oluşturma
    4. pytest çalıştıralım

Bölüm Sonu Kontrol Listesi

    mlops-fastapi-pratik projesi oluşturuldu.
    Python sanal ortamı hazırlandı.
    FastAPI ve gerekli kütüphaneler kuruldu.
    İlk FastAPI uygulaması oluşturuldu.
    Ana endpoint oluşturuldu.
    Health endpoint oluşturuldu.
    Swagger UI açıldı.
    Iris modeli sıfırdan eğitildi.
    Model Joblib dosyasına kaydedildi.
    Model metadata bilgileri kaydedildi.
    Model lifespan sırasında API’ye yüklendi.
    Modelin yalnızca bir kez yüklendiği doğrulandı.
    Prediction endpoint oluşturuldu.
    Request veri modeli oluşturuldu.
    Pydantic doğrulama kuralları eklendi.
    Fazladan alanlar yasaklandı.
    Tekli tahmin endpoint’i tamamlandı.
    Toplu tahmin endpoint’i oluşturuldu.
    Batch kayıt sayısı sınırlandırıldı.
    Validation hataları standartlaştırıldı.
    Hatalar yönetildi.
    HTTP status kodları tanımlandı.
    Tekli tahmin testi yazıldı.
    Batch tahmin testi yazıldı.
    Validation testleri yazıldı.
    Health endpoint testi yazıldı.
    Bilinmeyen endpoint için 404 testi yazıldı.
    Bütün Pytest testleri başarıyla tamamlandı.