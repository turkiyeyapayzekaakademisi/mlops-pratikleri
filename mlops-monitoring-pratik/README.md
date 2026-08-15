Üretimde Model İzleme Projesinin Hazırlanması
    1. deployment projesinin kopyalanması
    2. sanal ortam ve bağımlılıkları kur
    3. model dasyasının hazırlanması
    4. testleri yapalım
    5. fastapi uygulama çalıştırma

Fastapi'ye prometheus metriklerinin eklenmesi: api istek sayısı ve hata sayısı, api/model tahmin süresi, modelin ürettiği sınıfları say
    1. prometheus client'ın kurulması
    2. prometheus metric dosyalarının oluşturulması
    3. fastapi çalıştır
    4. prometheus metrik testlerinin eklenmesi

Prometheus'un Docker Compose ile Kurulması
    1. monitoring klasörü oluşturulması
    2. canlı /metrics endpointinin kontrol edilmesi
    3. prometheus.yml dosyasının oluşturulması
    4. Docker compose dosyasının oluşturulması
    5. prometheus containerin başlatılması
        docker compose -f monitoring\compose.yaml up -d
    6. Prometheus arayüzünün açılması
        http://localhost:9090

Grafananın Docker Compose ile Kurulması ve Prometheus'a Bağlanması
    1. Granana servisinin docker compose dosyasına eklenmesi
    2. grafana container başlatılması
        docker compose up -d
    3. grafana arayüzünün açılması
        http://localhost:3000
    4. prometheus data source'unun eklenmesi

Canlı API Metriklerinin Grafana Dashboard Üzerinden İzlenmesi
    1. Dashboard oluştur
    2. Panel Ekle

Evidently AI ile Data Drift Senaryosunun Oluşturulması
    1. Evidently AI kurulması
        pip install evidently
    2. Drift çalışması için klasör oluşturma
    3. Data drift senaryosu script oluştur
        create_drift_data.py
        python monitoring\drift\create_drift_data.py

Data Drift Raporunun Oluşturulması ve İncelenmesi
    1. Evidently workspace oluştur
        run_drift_report.py
        python monitoring\drift\run_drift_report.py
    2. Evidently UI başlatılması
        evidently ui --workspace ./evidently_workspace --port 8001
