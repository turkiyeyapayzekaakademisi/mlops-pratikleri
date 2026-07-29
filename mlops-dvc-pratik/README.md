DVC Kurulumu ve Projeye Eklenmesi
    1. Yeni proje klasörünün oluşturulması

    2. Git repo oluşturma
    git init
    git branch -M main

    3. Proje klasörlerini oluşturma

    4. Python sanal ortam oluşturma
    python -m venv venv
    .\venv\Scripts\activate

    5. .gitignore 

    6. requirements.txt oluşturulması
    pip install -r requirements.txt

    7. DVC kurulumunu kontrol et
    dvc --version

    8. DVC'yi projeye ekle
    dvc init

    9. Oluşan dosyaların kontrol edilmesi
    git status --short

    10. DVC proje kökü kontrol etme
    dvc root

    11. Başlangıç dosyalarının commit edilmesi
    git add .dvc .dvcignore .gitignore requirements.txt README.md
    git commit -m "DVC projesi oluşturuldu"

Veri Setinin DVC ile Takip Edilmesi: scikit learn kütüphanesinde bulunan Breast Cancer Veri Seti
    1. Veri oluşturma scriptinin hazırlanması
    src/create_dataset.py

    2. Script çalıştırma
    python src/create_dataset.py

    3. git durumunu kontrol et
    git status --short

    4. Veri dosyasını DVC ile takip et
    dvc add data/raw/breast_cancer.csv

    5. Oluşan dosyaları kontrol etme
    dir data\raw /A

    6. DVC durum kontrolü
    dvc status

DVC Dosyalarının Git ile Versiyonlanması
    1. git durumunu kontrol et
    git status --short

    2. DVC metadata dosyalarını git'e ekle
    git add data/raw/.gitignore data/raw/breast_cancer.csv.dvc src/create_dataset.py

    3. commit
    git commit -m "Ham veri setinin ilk sürümü DVC ile takip edildi."
    git log --oneline

    4. gerçek verinin git e eklenmediğini kontrol et
    git ls-files

Veri Setinin Güncellenmesi
    1. create_dataset.py dosyasının güncellenmesi

    2. Veri setinin yeniden oluşturulması
    python src/create_dataset.py

    3. Değişikliği DVC ile kontrol etmes
    dvc status

    4. Veri setinin yeni sürümünü kaydet
    dvc add data/raw/breast_cancer.csv

    5. .dvc dosyasındaki değişikliği görme
    git diff data/raw/breast_cancer.csv.dvc

    6. Değişiklikleri git'e kaydet
    git add src/create_dataset.py data/raw/breast_cancer.csv.dvc
    git commit -m "Veri setine record_id sütunu eklendi." 

Eski Veri Versyionuna Geri Dönme
    1. Veri sürümlerini gösteren commitleri listele
    git log --oneline -- data/raw/breast_cancer.csv.dvc

    2. .dvc dosyasını eski sürümüne getirme
    git checkout 6937a74 -- data/raw/breast_cancer.csv.dvc

    3. Eski veriyi çalışma alanına getir
    dvc checkout data/raw/breast_cancer.csv.dvc

    4. Eski veri sürümünü kontrol etme
    python -c "import pandas as pd; df=pd.read_csv('data/raw/breast_cancer.csv'); print(df.shape)"

    5. Güncel .dvc dosyasını geri getirme
    git restore --source=HEAD --staged --worktree data/raw/breast_cancer.csv.dvc

    6. güncel veri sürümünü geri getirme
    dvc checkout data/raw/breast_cancer.csv.dvc

Train, Validation ve Test Verilerinin Oluşturulması
    1. params.yaml dosyasının oluşturulması

    2. Parametreleri kontrol et
    type params.yaml

Veri Hazırlama Scriptinin Yazılması
    1. src/prepare_data.py yaz ve çalıştır.

DVC Remote Storage Yapılandırması
    1. Remote Storage Klasörünü Oluşturma
    New-Item -ItemType Directory -Force -Path ../dvc-storage

    2. DVC Remote Tanımlama
    dvc remote add -d localstorage ../dvc-storage

    3. remote bağlantısı kontrol
    dvc remote list

    4. DVC config dosyası ekle
    Get-Content .dvc/config

    5. Remote ayarını git ile kaydet
    git add .dvc/config
    git commit -m "Yerel DVC remote storage yapılandırıldı."

Verilerin Uzak Depolama Alanına Gönderilmesi
    1. DVC durumunu kontrol et
    dvc status

    2. Ham veriyi remote storage a gönder
    dvc push

    3. Remote storage içeriğini kontrol et
    Get-ChildItem ../dvc-storage -Recurse

    4. remote durumunu kontrol et
    dvc status -c

Verilerin Uzak Depolama Alanından Alınması
    1. Ham verilerin silinmesi
    Remove-Item data/raw/breast_cancer.csv

    2. Yerel dvc cache sil
    Remove-Item -Recurse -Force .dvc/cache

    3. Dosyaların silinniğini kontrol et
    Test-Path data/raw/breast_cancer.csv

    4. Veriyi remote storage dan al
    dvc pull data/raw/breast_cancer.csv.dvc

DVC Pipeline Oluşturulması
    1. Mevcut processed dosyalarını sil

    2. Stage oluşturma
    dvc stage add -n prepare -d src/prepare_data.py -d data/raw/breast_cancer.csv -p split.test_size -p split.validation_size -p split.random_state -o data/processed/train.csv -o data/processed/validation.csv -o data/processed/test.csv python src/prepare_data.py

    3.pipeline çalıştırma
    dvc repro

    4. oluşan dvc dosyalarını kontrol et
    git status --short

    5. pipeline grafiğini görüntüle
    dvc dag

    6. pipeline durumunu kontrol et
    dvc status

Tekrar Üretilebilir Veri Pipeline'ı Hazırlanması
    1. Pipeline'i değişiklik yapmadan tekrar çalıştır
    dvc repro

    2.Parametreyi değiştirme: params.yaml içerisinde değişiklik yapalım

    3. Pipeline durumunu kontrol et
    dvc status

    4. pipeline yeniden çalıştırma
    dvc repro

    5. pipeline dosyalarını git e kaydet
    git add data/processed/.gitignore dvc.yaml dvc.lock params.yaml src/prepare_data.py
    git commit -m "Tekrar üretilebilir veri hazırlama pipeline oluşturuldu."

    6. pipeline çıktılarını remote storage a gönder
    dvc push

    7. git durumunu kontrol et
    git status

    8. tekrar üretilebilirliği yeni klasörde test etme
    cd ..
    git clone ./mlops-dvc-pratik mlops-dvc-pratik-kopya
    cd mlops-dvc-pratik-kopya

    Diğer Projede
    9. Sanal ortamı yeni projede yeniden oluşturma
    10. Verileri remote storage dan alma: dvc pull
    11. pipeline çalıştırma: dvc repro

Bölüm Sonu Kontrol Listesi

    mlops-dvc-pratik projesi sıfırdan oluşturuldu.
    Git repository başlatıldı.
    Python sanal ortamı oluşturuldu.
    DVC kuruldu.
    DVC projeye eklendi.

    Breast Cancer veri seti oluşturuldu.
    Veri seti DVC ile takip edildi.
    Gerçek CSV dosyasının Git’e eklenmediği doğrulandı.
    .dvc dosyası Git ile versiyonlandı.

    Veri setinin ikinci sürümü oluşturuldu.
    Eski veri sürümüne geri dönüldü.
    Güncel veri sürümü tekrar getirildi.

    Train, validation ve test ayrımı yapıldı.
    Veri hazırlama scripti yazıldı.

    Yerel DVC remote storage oluşturuldu.
    Veriler dvc push ile remote storage’a gönderildi.
    Veriler dvc pull ile geri alındı.

    dvc.yaml pipeline dosyası oluşturuldu.
    dvc.lock dosyası oluşturuldu.
    Pipeline dvc repro ile çalıştırıldı.

    Parametre değişikliğinde pipeline’ın yeniden çalıştığı görüldü.
    Proje farklı bir klasöre klonlandı.
    Veriler ve pipeline yeni klasörde yeniden oluşturuldu.