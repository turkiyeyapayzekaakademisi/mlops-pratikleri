Yeniden Eğitim ve Model Güncelleme Projesinin Altyapı Hazırlığı
    1. sanal ortam ve kütüphaneler
    2. mevcut modelin champion model olarak ayarlanması
        python -m training.train_model
        iris_model.joblib -> champion
    3. dockerfile ve dockerignore güncelle
    4. yeni docker image oluşturulması
        docker build -t mlops-retraining-api:champion .
    5. champion model için container çalıştırma 
        docker run -d --name mlops-retraining-container -p 8000:8000 mlops-retraining-api:champion

Challenger Modelin Eğitilmesi
    1. train_challenger.py
        python -m training.train_challenger
    2. challenger model deneme
        python -c "from joblib import load; m=load('artifacts/challenger_model.joblib');print(m['model_version'])"

Github Actions ile Otomatik Model Güncelleme ve Deployment
    1. Promotion dosyasının oluşturulması
        promote_challenger.py
    2. Champion-Challenger kararının yazılması
        python -m training.train_model
        python -m training.train_challenger
        python -m training.promote_challenger