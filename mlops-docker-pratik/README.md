Klasör Altyapısı ve ML Modeli Oluşturma
    1. projenin oluşturulması
    2. git repo oluşturma
    3. klasör altyapısı oluşturma
    4. sanal ortam oluşturma
    5. gerekli kütüphanelerin tanımlanması
    6. kütüphanelerin kurulması
    7. ML model eğitimi
        train_model.py
        python -m training.train_model

ML Modelinin API Servisi Haline Getirilmesi
    1. API klasörü oluştur
    2. FastAPI kütüphanelerinin eklenmesi
    3. API uygulamasının yazılması
    4. API servisi çalıştırma
        uvicorn app.main:app --reload

Docker Kurulumu ve Docker Desktop Hazırlanması 
    1. WSL 2 kontrolü (windows subsystem for linux), docker desktop kurulumu, docker doğrulamaları
    2. WSL 2 kontrolü
        wsl --version
        wsl -- install
        wsl --update
    3. WSL dağıtımlarının kontrol edilmesi
        wsl -l -v
    4. Sanallaştırma kontrol edilmesi
        görev yöneticisi - performans - cpu
    5. Docker desktop indirme
    6. Docker içinde wsl kontrolü settings - general - use wsl 2 based engine
    7. Docker CLI kontrolü
        docker --version
    8. Docker Engine kontrolü
        docker version
    9. Docker sistem bilgilerinin kontrol edilmesi
        docker info
    10. ilk container'in çalıştırılması
        docker run hello-world
        docker image -> container oluştur -> container çalıştır -> Hello from Docker!
    11. docker imajların kontrol edilmesi
        docker images
    12. containerların kontrol edilmesi
        docker ps
        docker ps -a
    13. Docker compose kontrolü
        docker compose version
    14. Bu derste ne yaptık?
        windows üzerinde wsl 2 altyapısını kontrol ettik ve docker desktop kurulumu yaptık
        docker CLI, Engine ve Compose düzgün çalıştığını doğruladık
        hello-world imajını kullanarak ilk docker container'ımızı çalıştırdık.

Dockerfile Oluşturulması: Makine Öğrenmesi API servisini Docker ile paketleyebilmek için gerekli Dockerfile hazırlama
    1. Dockerfile dosyasının oluşturulması

    2. Dockerfile içeriğinin hazırlanması

    3. .dockerignore dosyasının oluşturulması

Docker Image Oluşturulması: 
    1. bir önceki derste hazırladığımız Dockerfile dosyasını kullanarak makine öğrenmesi API servisimizin docker image'ını doluştur
    2. docker desktop kontrol edilmesi
    3. Docker image oluştur
        docker build -t diabetes-api:1.0 .
        dockerfile -> python ortamı -> python kütüphaneleri -> fastapi uygulması -> ml modeli -> docker image
    4. oluşturulan image ların kontrol edilmesi
        docker images
        docker image ls diabetes-api
    5. docker desktop üzerinden kontrol edilmesi

Docker Container'ın Çalıştırılması: docker image'ı kullanarak ilk container çalıştır.
    1. Docker image'ın kontrol edilmesi
        docker images
    2. Docker container çalıştırılması
        docker run -d --name diabetes-api-container -p 8000:8000 diabetes-api:1.0
        diabetes-api:1.0 -> docker container -> fastapi -> port 8000
    3. çalışan containerin kontrol edilmesi
        docker ps
    4. container durdurulması
        docker stop diabetes-api-container
        docker ps -a 
    5. container tekrar başlatma
        docker start diabetes-api-container

Container Üzerindeki Model Servisinin Test Edilmesi: Docker container içerisinde çalışan makine öğrenmesi servisimizin doğru şekilde çalıştığını test et
    1. Container çalışmasının kontrol edilmesi
        docker ps
    2. Endpointleri test edilmesi: ana root, /health, /predict
    3. Model servisinin çalışma akışı: kullanıcı -> localhost:8000 -> Docker port mapping -> docker container -> fastapi -> ml modeli -> tahmin(json)

Docker Container Loglarının İncelenmesi
    1. Container çalıştığının kontrol edilmesi
        docker ps
    2. Container loglarının görüntülenmesi
        docker logs diabetes-api-container
    3. logların canlı takip edilmesi
        docker logs -f diabetes-api-container
    4. Son logların görüntülenmesi
        docker logs --tail 5 diabetes-api-container

Docker Volume Oluşturulması: volume'un amacı, bir volume oluşturma ve volume kontrolü
    1. diabetes_model.joblib dosyasını docker volume içerisinde sakla
        docker volume -> diabetes_model.joblib sakla -> ML API Container
    2. Docker volume oluşturma
        docker volume create diabetes-model-volume
    3. volume listelenmesi
        docker volume ls
    4. docker volume inspect diabetes-model-volume

ML Modelinin Docker Volume İçerisinde Saklanması
    1. Volume kontrol edilmesi
        docker volume ls
    2. model dosyasının volume içerisine alınması
        docker run --rm `
            --mount source=diabetes-model-volume,target=/app/artifacts `
            diabetes-api:1.0 `
            ls -l /app/artifacts
    3. volume içerisindeki modelin kontrol edilmesi
        docker run --rm `
            --mount source=diabetes-model-volume,target=/models `
            python:3.12-slim `
            ls -l /models

Volume Kullanarak Model Servisinin Çalıştırılması
    1. Volume ve model dosyasının kontrol edilmesi
        docker volume ls
        docker run --rm `
            --mount source=diabetes-model-volume,target=/models `
            python:3.12-slim `
            ls -l /models
    2. mevcut container durdurulması ve silinmesi
        docker stop diabetes-api-container
        docker rm diabetes-api-container
    3. volume kullanarak container çalıştır
        docker run -d `
            --name diabetes-api-container `
            -p 8000:8000 `
            --mount source=diabetes-model-volume,target=/app/artifacts `
            diabetes-api:1.0
    4. container kontrol edilmesi
        docker ps
    5. volume bağlantısının kontrol edilmesi
        docker inspect diabetes-api-container
    6. api servisi kontrolü
    7. model tahminin test edilmesi
    8. son yapı: diabetes-api:1.0 -> ml api container -> artifacts -> diabetes-model-volume -> diabetes_model.joblib

İkinci ML Modeli ve API Servisinin Oluşturulması
    1. İkinci servis klasörünün oluşturulması
    2. requirements.txt oluşturulması
    3. train_model.py dosyasını oluşturalım
    4. modelin eğitilmesi
        python -m breast_cancer_service.training.train_model
    5. fastapi service oluşturma
        uvicorn breast_cancer_service.app.main:app --reload --port 8001

ML Servisleri için Docker Image Oluşturma
    1. Breast cancer için docker file oluşturma
    2. Diabetes docker image oluşturma
        docker build -t diabetes-api:1.0 ./diabetes_service
    3. Breast Caner docker image oluşturma
        docker build -t breast-cancer-api:1.0 ./breast_cancer_service
    4. docker image kontrol etme
        docker images

Docker Compose Dosyası Oluşturma: iki tane ml servisini tek bir docker compose dosyası içinde tanımla
    1. compose.yaml dosyası oluşturma
    2. compose dosyasının kontrol edilmesi
        docker compose config

Docker Compose ile Birden Fazla ML Servisinin Birlikte Çalıştırılması
    1. container kontrol edilmesi
        docker ps -a 
        docker stop diabetes-api-container
        docker rm diabetes-api-container
    2. servislerin docker compose ile başlatılması
        docker compose up -d
    3. çalışan servislerin kontrol edilmesi
        docker compose ps
    4. docker compose
        diabetes API
            port 8000
        breast cancer API
            port 8001
    5. compose loglarının görülmesi
        docker compose logs
        docker compose logs -f
    6. servislerin durdurulması
        docker compose stop
    7. servislerin çalıştırılması
        docker compose start
    8. compose yapısının kapatılması
        docker compose down

Docker Compose İçerisinde Network ve Volume Kullanımı: docker compose yapımıza network ve volume ekleme
    1. Compose dosyasının güncellenmesi
    2. Compose yapısının çalıştırılması
        docker compose up -d
    3. Network'ün kontrol edilmesi
        docker network ls
        docker network inspect mlops-docker-pratik_ml-network
    4. Servis isimleriyle iletişimin kontrol edilmesi
        http://diabetes-api:8000
        docker exec breast-cancer-api-container python -c "import urllib.request; print(urllib.request.urlopen('http://diabetes-api:8000/health').read().decode())"
    5. volume bağlantısının kontrol edilmesi
        docker inspect diabetes-api-container
        model dosyasını doğrudan container içerisinden kontrol edelim
            docker exec diabetes-api-container ls -l /app/artifacts
    6. Docker compose -> ml-network - diabetes api (diabetes-model-volume (.joblib)) ve breast cancer api

Docker Image Tag ve Versiyonların Oluşturulması
    1. Mevcut Image ların Kontrol Edilmesi
        docker images
    2. Docker image tag yapısı: breast-cancer-api:1.0
    3. Yeni tag oluşturulması
        docker tag diabetes-api:1.0 diabetes-api:1.1
        docker tag breast-cancer-api:1.0 breast-cancer-api:1.1
    4. latest tag oluşturulması: güncel olarak kullanmak istediğimiz image'a latest diyelim
        docker tag diabetes-api:1.1 diabetes-api:latest
        docker tag breast-cancer-api:1.0 breast-cancer-api:latest
    5. image versiyonlarının kontrol edilmesi
        docker images diabetes-api
    6. Compose dosyasının yeni versiyonlarla güncellenmesi
        
Docker Image'larının Github Container Registry'ye Gönderilmesi  
    1. Bilgisayarımızda oluşturduğumuz image'ları GHCR'ye gönderelim. 
        GHCR nin ne olduğunu anlayalım: image -> tag -> ghcr.io kaydı -> push -> github container registry
        Githbu erişim tokenları
        docker üzerinden ghcr.io registry'sine giriş yap
        ML Servislerinin docker image'larını ghcr formatında tag le
        Image ların github üzerinde bulunduğunun kontrol edilmesi
    2. GHCR image isim yapısı
        ghcr.io/GITHUB_USERNAME/IMAGE_NAME:TAG
        ghcr.io/turkiyeyapayzekaakademisi/diabetes-api:1.1
    3. Github üzerinden personal access token oluşturulması
        profile -> settings -> developer setting -> personel access token -> token classic -> generate new token (classic)
    4. token yetkisinin belirlenmesi
    5. Github container registry'ye giriş yapılması
        $env:CR_PAT = Read-Host "Github Personal Access Token"
        docker ile github container registry giriş yap: $env:CR_PAT | docker login ghcr.io -u turkiyeyapayzekaakademisi --password-stdin
    6. image ların ghcr için taglenmesi
        docker tag diabetes-api:1.1 ghcr.io/turkiyeyapayzekaakademisi/diabetes-api:latest
        docker tag breast-cancer-api:1.1 ghcr.io/turkiyeyapayzekaakademisi/breast-cancer-api:latest
    7. image ları ghcr ye gönder
        docker push ghcr.io/turkiyeyapayzekaakademisi/diabetes-api:latest 
        docker push ghcr.io/turkiyeyapayzekaakademisi/breast-cancer-api:latest
    8. Github üzerinden kontrol edilmesi
        github -> packages 
    9. registry oturumunu kapat
        docker logout ghcr.io
        Remove-Item Env:CR_PAT

Github Container Registry'den Image İndirilmesi ve Çalıştırılması
    1. Registry -> docker pull -> Docker image -> docker run -> container -> ml api
    2. Mevcut containerların kapatılması
        docker compose down
        docker ps
    3. private package için GHCR giriş yapılması
        $env:CR_PAT = Read-Host "Github Personal Access Token"
        $env:CR_PAT | docker login ghcr.io -u turkiyeyapayzekaakademisi --password-stdin
    4. imageların indirilmesi
        docker pull ghcr.io/turkiyeyapayzekaakademisi/diabetes-api:latest
        docker pull ghcr.io/turkiyeyapayzekaakademisi/breast-cancer-api:latest
    5. container olarak çalıştır
        docker run -d `
            --name diabetes-ghcr-container `
            -p 8000:8000 `
            ghcr.io/turkiyeyapayzekaakademisi/diabetes-api:latest
        docker run -d `
            --name breast-cancer-ghcr-container `
            -p 8001:8000 `
            ghcr.io/turkiyeyapayzekaakademisi/breast-cancer-api:latest

Bu bölümde Ne Yaptık?
	Scikit-learn Diabetes veri setiyle bir regresyon modeli eğittik ve modeli joblib formatında kaydettik.
	Eğittiğimiz modeli FastAPI ile API servisi hâline getirdik ve tahmin endpoint’i oluşturduk.
	Docker Desktop, WSL 2 ve Docker CLI ortamını hazırlayıp Docker kurulumunu doğruladık.
	ML API servisini container içerisine alabilmek için Dockerfile oluşturduk.
	Dockerfile kullanarak ML servisimizin Docker image’ını oluşturduk.
	Docker image’dan container oluşturup FastAPI servisini dışarıya açtık.
	Container içerisinde çalışan model servisinin endpoint’lerini test ettik.
	Docker container loglarını görüntüleyip servis davranışlarını takip ettik.
	Model dosyasını container’dan bağımsız saklamak için Docker Volume oluşturduk.
	Eğitilmiş model dosyasını Docker Volume içerisine aktardık.
	ML API servisinin modeli Docker Volume üzerinden kullanmasını sağladık.
	Breast Cancer veri setiyle ikinci bir sınıflandırma modeli ve FastAPI servisi oluşturduk.
	Diabetes ve Breast Cancer servisleri için ayrı Docker image’ları oluşturduk.
	İki ML servisini tek bir compose.yaml dosyasında tanımladık.
	Docker Compose ile iki ML servisini aynı anda çalıştırdık.
	Servisleri ortak bir Docker network’e bağladık ve volume kullanımını Compose yapısına dahil ettik.
	Docker image’larına farklı tag ve versiyonlar verdik.
	Docker image’larını GitHub Container Registry’ye gönderdik.
	GitHub Container Registry üzerindeki image’ları indirip container olarak tekrar çalıştırdık.