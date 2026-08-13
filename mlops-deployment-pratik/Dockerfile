# python tabanlı bir tane image kullan
FROM python:3.12-slim

# pythonın .pyc dosyaları üretmesini engelle
ENV PYTHONDONTWRITEBYTECODE=1

# python çıktılarını doğrudan terminale gönder
ENV PYTHONUNBUFFERED=1

# container çalışma klasörü belirle
WORKDIR / app

# uygulama bağımlılıklarını kopyala
COPY requirements.txt .

# python bağımlılıklarını kur
RUN pip install --no-cache-dir -r requirements.txt

# Model eğitim kodlarını kopyala
COPY training ./training

# Fastapi uygulamasını kopyala
COPY app ./app

# modeli docker build sırasında eğit
RUN python -m training.train_model

# fastapi portunu belirt
EXPOSE 8000

# container başladığında api servisini çalıştır
CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level ${LOG_LEVEL:-info}"]