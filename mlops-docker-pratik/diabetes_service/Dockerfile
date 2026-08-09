# python 3.12 tabanlı hafif linux image'ını kullan
# FROM: hangi temel image üzerinde başlayacağımızı belirtir
FROM python:3.12-slim

# pythonın .pyc dosyalarını oluşturmasını engelle
# ENV container içerisinde kullanılacak ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1

# python çıktılarını doğrudan terminale gönder
ENV PYTHONUNBUFFERED=1

# container içerisinde ki çalışma klasörünü belirle
# WORKDIR: container içerisinde ki çalışma klasörü
WORKDIR /app

# requirement.txt dosyasının container içerisine kopyalanması
# COPY: dosyaları bilgisayarımızdan image içerisine kopyalamak için
COPY requirements.txt .

# python kütüphanelerini yükle
# RUN: image oluştururken bir komut çalıştırır 
RUN pip install --no-cache-dir -r requirements.txt

# fastapi uygulamasının container içerisine kopyalanması
COPY app ./app

# eğitilmiş ML modelini container içerisine kopyala
COPY artifacts ./artifacts

# fastapi service kullanılacak port u belirle 
#EXPOSE: uygulamanın hangi port üzerinden servis vereceğini belirtir  
EXPOSE 8000

# container başladığında fastapi servisini çalıştırır
# CMD: container başladığında çalıştırılacak varsayılan komutu belirler
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]