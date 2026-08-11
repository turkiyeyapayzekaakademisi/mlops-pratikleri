CI/CD Proje ve Klasör Altyapısının Oluşturulması
    1. yeni projenin oluşturulması
    2. git repo oluşturma
    3. python venv oluşturulması
    4. requirements.txt ve requirements-dev.txt dosyalarının oluşturulması ve kurulması
        python -c "import pandas, sklearn; print('ok')"
        pytest --version
    5. Uygulama klasörlerinin oluşturulması
    6. Github actions klasörünün oluşturulması
    7. temel proje dosyalarının oluşturulması

Kod Kalitesi Kontrolleri
    1. Ruff yapılandırma dosyasının oluşturulması
        pyproject.toml oluşturulması
    2. Ruff lint kontrolünün çalıştırılması
        ruff check .
    3. örnek hatalı bir python dosyası
        quality_example.py
    4. ruff ile otomatik olarak düzeltme
         ruff check training/quality_example.py --fix
    5. kodun ruff ile formatlanması 
        ruff format --check training/quality_example.py
        ruff format training/quality_example.py
    6. tüm projenin lint kontrolünün yapılması
        kontrol: ruff format --check
        düzelt: ruff format .
    7. pipeline akışı:
        git push -> ruff lint -> ruff format -> kod kalitesi başarılı -> ...

Otomatik Testlerin Pipeline İçerisinde Çalıştırılması
    1. artifacts klasörü güncelleme
    2. pytest ayarlarının eklenmesi
    3. ilk otomatik test dosyası oluştur
        test_project_setup.py
    4. ilk testin çalıştırılması
        python -m pytest
    5. Kod kalitesi ve testlerin birlikte çalıştırılması
        kod kalitesi: ruff check .
        format kontrolü: ruff format --check . 
        test: python -m pytest

Model Eğitim Kodlarının Test Edilmesi
    1. model eğitim dosyasının oluşturulması
        train_model.py
        python -m training.train_model
    2. Model eğitim test dosyasının oluşturulması
        test_train_model.py
        python -m pytest tests/test_train_model.py

FastAPI Testlerinin Çalıştırılması
    1. Fastapi uygulamasının oluşturulması
        main.py
        uvicorn app.main:app --reload
    2. Fastapi Test dosyasının oluşturulması
        test_api.py
    3. fastapi testlerinin çalıştırılması
        python -m pytest tests/test_api.py
    4. tüm testlerin birlikte çalıştırılması
        python -m pytest

Docker Image'ın Otomatik Oluşturulması
    1. Docker kurlumunun kontrol edilmesi
        docker version
    2..dockerignore dosyasının oluşturulması
    3. Dockerfile dosyasının hazırlanması
    4. Docker image oluşturulması
        docker build -t mlops-cicd-api:1.0 .
        docker images
    5. image ı container olarak çalıştır
        docker run -d `
            --name mlops-cicd-container `
            -p 8000:8000 `
            mlops-cicd-api:1.0
    6. Otomatik build
        ruff -> pytest -> docker

Image'ın Registry'ye Gönderilmesi
    1. Docker image'ın kontrol edilmesi
        docker images mlops-cicd-api
    2. Github Container Registry için token oluşturma
    3. Token'ın Powershell içerisine alınması
        $env:CR_PAT = Read-Host "Github personal access token"
    4. Github Container Registry giriş yapılması
        ghcr.io
        $env:CR_PAT | docker login ghcr.io -u turkiyeyapayzekaakademisi --password-stdin
    5. ghcr image adresinin belirlenmesi
        ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:1.0
        docker tag mlops-cicd-api:1.0 ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:1.0
    6. latest tag oluşturma
        docker tag mlops-cicd-api:1.0 ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:latest
    7. taglerin kontrol edilmesi
        docker images
    8. image'ların registry'ye gönderilmesi
        docker push ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:1.0
        docker push ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:latest
    9. lokal imageların silinmesi
        docker image rm ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:1.0
    10. registry de ki image'ın test edilmesi
        docker pull ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:latest
    11. registry den gelen image'ın çalıştırılması
        docker run -d `
            --name mlops-cicd-registry-container `
            -p 8000:8000 `
            ghcr.io/turkiyeyapayzekaakademisi/mlops-cicd-api:latest
    12. Kod -> ruff -> pytest -> docker (build + tag + push) -> github container registry

Github Actions Dosyasının Hazırlanması
    1. github repo oluşturulması
        repo adı mlops-cicd-pratik
    2. lokal projenin github repoya bağlanması işlemleri
        github repoyu remote olarak ekle
            git remote add origin https://github.com/turkiyeyapayzekaakademisi/mlops-cicd-pratik.git
        github gönderme push
        git push -u origin main
    3. github actions dosyasının oluşturulması
        ci.yaml
    4. ci.yaml'ın içeriğini hazırlanması
    5. workflow dosyasının git e eklenmesi
    
Pipeline Secret Değişkenlerinin Tanımlanması
    1. Secret neden kullanılır? api key, access token, registry password bunların saklı olması lazım
    2. GITHUB_TOKEN kullanılması    
        ${{ secrets.GITHUB_TOKEN }}
    3. pipeline a package yazma yetkisi verilmesi
    4. registry bilgilerinin tanımlanası
    5. Docker image yapısının güncellenmesi
    6. GHCR authentication adımının eklenmesi
    7. latest tag inin oluşturulması
    8. image ı ghcr ye gönder

Başarılı ve Başarısız Pipeline Sonuçlarının İncelenmesi


Bölüm Sonu
    CI/CD projesini ve klasör altyapısını oluşturduk.
    Python sanal ortamını ve proje bağımlılıklarını hazırladık.
    Ruff ile kod kalitesi ve format kontrollerini ekledik.
    Pytest ile otomatik test altyapısını oluşturduk.
    Iris veri setiyle model eğitim kodunu hazırladık.
    Model eğitim sürecini testlerle doğruladık.
    Eğitilmiş modeli artifact olarak kaydettik.
    FastAPI ile model servisleştirme uygulamasını geliştirdik.
    FastAPI endpoint’leri için otomatik testler yazdık.
    Dockerfile ve .dockerignore dosyalarını hazırladık.
    Modelin Docker build sırasında otomatik eğitilmesini sağladık.
    Docker image oluşturup container olarak çalıştırdık.
    Docker image’ı GitHub Container Registry için tag’ledik.
    Image’ı GHCR’ye manuel olarak push ettik ve doğruladık.
    Projeyi GitHub repository’ye gönderdik.
    GitHub Actions için ci.yaml workflow dosyasını oluşturduk.
    Ruff kontrollerini GitHub Actions pipeline’ına ekledik.
    Pytest testlerini pipeline içerisinde otomatik çalıştırdık.
    Testler başarılı olduğunda Docker image’ın otomatik oluşturulmasını sağladık.
    Docker image’ı Git commit SHA değeriyle tag’ledik.
    GitHub Actions içerisinde GITHUB_TOKEN kullandık.
    Pipeline’a GHCR için packages: write yetkisi verdik.
    Pipeline içerisinden GHCR authentication gerçekleştirdik.
    Docker image’a latest tag’i ekledik.
    Image’ın commit SHA ve latest tag’leriyle GHCR’ye otomatik gönderilmesini sağladık.
    GitHub Push Protection’ın secret içeren commit’leri nasıl engellediğini gördük.
    Pipeline’da Ruff, dependency, Docker build ve registry permission hatalarını inceleyip düzelttik.
    Pipeline’ı bilerek başarısız hale getirerek hata loglarını inceledik.
    Başarısız testlerin sonraki build ve push adımlarını durdurduğunu doğruladık.
    Hataları düzelterek pipeline’ın tekrar başarılı çalışmasını sağladık.
    Koddan registry’ye kadar çalışan uçtan uca otomatik CI/CD sürecini tamamladık.

