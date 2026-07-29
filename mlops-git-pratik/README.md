Git Kurulumu ve Yapılandırması
    1. Git indirme
    - https://git-scm.com/install/windows

    2. Git bash açma

    3. Git kurulumunu kontrol etme
    git --version

    4. Git kullanıcı adını tanımla
    git config --global user.name "admin"
    git config --global --get user.name

    5. Git e-posta adresi tanımla
    git config --global user.email "admin@example.com"
    git config --global --get user.email

    6. Varsayılan branch adını belirle
    git config --global init.defaultBranch main

    7. Windows satır sonu ayarını yapma
    git config --global core.autocrlf true

    8. Yapılandırmayı kontrol etme
    git config --global --list

Git Repo Oluşturma
    1. klasör yapısı oluşturma ve terminal açma

    2. py dosyalarının çalıştırılmas
    python hello_world.py

    3. git repo oluşturma
    git init

    4. git repo durum kontrolü
    git status

    5. .git (repo geçmişinin ve git bilgilerinin saklandığı gizli klasör) kontrol etme
    git rev-parse --git-dir

Dosya Ekleme ve Commit Oluşturma
    1. Dosyaların durumunu kontrol etme
    git status

    2. Sadece hello_world.py dosyasını ekleme
    git add hello_world.py

    3. Diğer dosyaları ekle
    git add README.md src/train.py
    git add .

    4. İlk commit oluşturma
    git commit -m "Proje başlangıç dosyaları oluşturuldu"

Git Durumunu ve Geçmişini İncele
    1. Detaylı commit geçmişi: 
    git log
        commit kimliği
        yazar bilgisi
        commit tarihi
        commit mesajı

    2. Kısa commit geçmişini görüntüleme
    git log --oneline

    3. .py dosyasını güncelle ve durumunu kontrol et

    4. Değişikliği görüntüle
    git diff

    5. yeni commit oluştur

    6. Son commit detayları göster
    git show HEAD

Branch Oluşturma ve Branchler Arasında Geçiş
    1. Mevcut branch i kontrol et
    git branch

    2. Yeni branch oluşturma
    git switch -c feature-model-message

    3. Branch leri kontrol et
    git branch

    4. train.py dosyası değiştirme

    5. feature-model-message branch üzerinde commit oluşturma
    git add .
    git commit -m "New feature eğitim verileri hazırlanıyor."

    6. Main branch e geri dönme
    git switch main

Branch Birleştirme ve Merge İşlemleri
    1. Aktif branch kontrol etme
    git branch

    2. feature-model-message branch i main ile birleştirme 
    git merge feature-model-message
    git checkout feature-model-message -- src/train.py

    3. commit geçmişi kontrol etme
    git log --oneline --graph --decorate --all

    4. Birleştirilen branch silme
    git branch -D feature-model-message

Merge Conflict Çözme
    1. Yeni branch oluştur
    git switch -c feature-model-message

    2. train.py dosyasında değişiklik yapma, commit etme

    3. main branch dönme
    git switch main

    4. main branch commit etme
    git add .\src\train.py
    git commit -m "logistic regression modeli eklendi."

    5. branch birleştirme
    git merge feature-model-message

    6. Conflict i çözdük, git e bildir
    git add .\src\train.py

    7. merge commit oluştur
    git commit -m "Model mesajındaki random forest ve log reg conflict çözüldü."

    8. Branch geçmişlerini görüntüle
    git log --oneline --graph --decorate --all

    9. feature-model-message branch sil
    git branch -d feature-model-message

.gitignore Dosyasının Hazırlanması
    1. .env, data, models

    2. Durumun kontrol edilmesi
    git status --short

    3. .gitignore dosyasının oluşturulması ve içeriğinin tanımlanması

    4. Durumun kontrol edilmesi

    5. Yok sayılan yani ignore edilen dosyaların görüntülenmesi
    git status --ignored --short

    6. Bir dosyanın hangi kurala göre yok sayıldığı
    git check-ignore -v .env

    7. .gitignore dosyasının commit edilmesi
    git add .gitignore
    git commit -m "gitignore ve readme güncelleme ekledik"

    8. git e eklenen bir dosyanın çıkartılması
    git rm --cached .kcy

README
    1. README.md oluştur

    2. README içerisinde olması gereken örnek yaklaşımlar.
    - projenin adı, amacı, teknolojiler, klasör yapısı, komutlar, git komutları, repo komutları, commit, branch ve merge komutları

    3. commit 

GitHub Repository Oluşturma
    1. Github hesabı açmak
    2. Yeni repo oluşturma
    3. Repo bilgileri girme (isim:mlops-git-pratik, açıklama ve görünürlük)
    4. Başlangıç dosyalarının eklenmeMEsi
    5. Repo oluşturma
    6. HTTPS adresi: yerel repo ile github arasında bağlantı kurmak için kullanılan adres 
    https://github.com/turkiyeyapayzekaakademisi/mlops-git-pratik.git

Yerel Projeyi Github'a Gönderme
    1. Yerel repo durumu kontrol et
    git status

    2. git add, commit

    3. github'a ekleme
        git init 
        git add .
        git commit -m "first commit"
        git branch -M main
        git remote add origin https://github.com/turkiyeyapayzekaakademisi/mlops-git-pratik.git
        git push -u origin main

Github Üzerinden Proje Güncelleme
    1. Github üzerinden readme dosyası güncelle. (güncellendi)
    2. uzak repo değişikliklerini kontrol et
    git fetch origin

    3. github da yapılan yeni commitleri görüntüle
    git log main..origin/main --oneline

    4. Değişikliği yerel projeye al
    git pull origin main

Bölüm Sonu Kontrol Listesi

    Git resmi kurulum dosyasıyla kuruldu.
    Git Bash üzerinden Git sürümü kontrol edildi.
    Git kullanıcı adı ve e-posta adresi tanımlandı.
    Varsayılan branch adı main olarak ayarlandı.
    Proje VS Code üzerinden açıldı.
    hello_world.py oluşturuldu ve çalıştırıldı.
    src/train.py oluşturuldu ve çalıştırıldı.
    Git repository oluşturuldu.
    Dosyalar staging area’ya eklendi.
    İlk commit oluşturuldu.
    Commit geçmişi incelendi.
    Dosya değişiklikleri git diff ile görüntülendi.
    Yeni branch oluşturuldu.
    Branchler arasında geçiş yapıldı.
    Feature branch main ile birleştirildi.
    Merge conflict oluşturuldu.
    .gitignore dosyası oluşturuldu.
    Gizli bilgiler, veri ve model dosyaları Git dışında bırakıldı.
    README dokümantasyonu düzenlendi.
    GitHub repository oluşturuldu.
    Yerel repository GitHub’a gönderildi.
    GitHub değişikliği git fetch ve git pull ile alındı.
    Yerel değişiklik git push ile GitHub’a gönderildi.
    Repository git clone ile yeni bir klasöre indirildi.