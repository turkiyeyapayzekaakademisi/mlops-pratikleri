Canlı Ortam Değişkenlerinin Tanımlanması
    1. Gerekli altyapı oluşturuldu
    2. APP_ENV değişkeninin uygulanması
        $env:APP_ENV = "production"
    3. Dockerfile'ın PORT ve LOG_LEVEL kullanacak şekilde güncellenmesi
    4. Güncel docker image oluşturma
        docker build -t mlops-deployment-api:1.0 .
        docker image ls mlops-deployment-api
    5. container canlı ortam değişkenleriyle çalıştırma
        docker run -d `
            --name mlops-deployment-container `
            -p 9000:9000 `
            -e APP_ENV=production `
            -e LOG_LEVEL=info `
            -e PORT=9000 `
            mlops-deployment-api:1.0

Docker Image'ın GHCR'den Render'a Aktarılması: image -> ghcr, render web service, ghcr -> render, canlı ortam tanımı, ilk deployment
    1. güncel docker image kontrol
        docker image ls mlops-deployment-api
    2. image ghcr için taglenmesi
        docker tag mlops-deployment-api:1.0 ghcr.io/turkiyeyapayzekaakademisi/mlops-deployment-api:1.0
        docker tag mlops-deployment-api:1.0 ghcr.io/turkiyeyapayzekaakademisi/mlops-deployment-api:latest
    3. ghcr'ye giriş yapılması
        token
        $env:GHCR_TOKEN = Read-Host "github write token"
        $env:GHCR_TOKEN | docker login ghcr.io -u turkiyeyapayzekaakademisi --password-stdin
    4. güncel image'ı ghcr ye gönder
        docker push ghcr.io/turkiyeyapayzekaakademisi/mlops-deployment-api:1.0
        docker push ghcr.io/turkiyeyapayzekaakademisi/mlops-deployment-api:latest

Github Actions ile Otomatik Deployment Yapılması
    1. Deployment projesi için github repo oluşturma
    2. Lokal projenin git repo haline getirilmesi
    3. Eski ci-cd workflow dosyasının silinmesi
    4. GHCR package'a yeni repo için yazma yetkisi verilmesi (write seçmeyi unutmayın)
    5. Render Deploy Hook adresinin alınması
        yeni image hazır deployment başlat
    6. Render deploy hook un github secret olarak eklenmesi
    7. deployment workflow dosyasının oluşturulması
    8. Projenin ilk commitinin oluşturulması    
        kod değişikliği
        git commit
        git push
        github actions
        ruff
        pytest
        docker build
        commit sha + latest
        ghcr push
        render deploy hook
        render ghcrden image ı çeker
        render yeni container oluşturur
        canlı api




