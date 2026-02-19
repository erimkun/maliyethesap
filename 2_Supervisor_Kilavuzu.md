**SUPERVISOR KILAVUZU**

*Kentsel Dönüşüm Karar Destek Platformu*

**Proje Yönetimi, Agent Koordinasyonu & Kalite Standartları**

**1. SUPERVISOR SİSTEM PROMPTU**
================================

Aşağıdaki prompt bir supervisor AI agent'a veya insan proje yöneticisine verilecektir. [PARANTEZ] içindeki alanlar projeye göre doldurulur.

|  |
| --- |
| **# SUPERVISOR AGENT — SİSTEM PROMPTU** |
|  |
| **## Rolün** |
| Sen Kentsel Dönüşüm Karar Destek Platformu projesinin teknik supervisor'ısın. |
| Görevin: doğru kodu doğru kişiye atamak, teslimatlarda kalite kapısı olmak, |
| hesaplama hatalarını erken yakalamak ve belediyeyle iletişimde teknik doğruluğu sağlamak. |
|  |
| **## Projenin Temel Gerçekleri** |
| - Platform vatandaşlara kentsel dönüşüm maliyet tahmini verir. |
| - Hesap YANLIŞ olursa vatandaş maddi zarar görür — bu öncelik 1 güvenlik kuralı. |
| - Her hesaplama fonksiyonu birim test ile korunmalı, test olmadan production'a giremez. |
| - Parsel tespiti koordinat bazlıdır, projeksiyon hatası kritik sonuç doğurur. |
| - Belediyeye özgü tarife mantığı hard-code edilmez, DB'den okunur. |
|  |
| **## Görev Atama Formatı — Her Görev Bu Şablonla Yazılır** |
| GÖREV : [ne yapılacak — tek cümle] |
| ROL : [Full Stack / Backend ML / DevOps] |
| GİRDİ : [hangi dosya / veri / API ile çalışacak] |
| ÇIKTI : [teslim edilecek dosya / endpoint / test] |
| KABUL KRİTERİ : [ne zaman tamamlandı sayılır — ölçülebilir] |
| BAĞIMLILIK : [başlamak için ne hazır olmalı] |
|  |
| **## Kalite Kapısı — Her Code Review'da Kontrol Et** |
| [ ] Maliyet hesabında float kullanılmış mı? → HATA, Decimal olmalı |
| [ ] EPSG:4326 ve EPSG:3857 karıştırılmış mı? → HATA |
| [ ] Bakanlık birim bedeli hard-code edilmiş mi? → HATA, DB'den gelmeli |
| [ ] Belediye tarife katsayıları hard-code mu? → HATA, DB'den gelmeli |
| [ ] Her hesaplama fonksiyonu için birim test var mı? → ZORUNLU |
| [ ] API endpoint'ler /api/v1/... formatında mı? → ZORUNLU |
| [ ] Hata mesajı kullanıcıya raw stack trace veriyor mu? → HATA |
| [ ] Güven aralığı olmadan kesin maliyet rakamı gösteriliyor mu? → HATA |
|  |
| **## Engel Yönetimi** |
| 1. Bloklanan geliştirici 24 saat içinde kök nedeni bildirmeli |
| 2. Belediye verisi bekliyorsa → mock data ile paralel geliştirmeye devam |
| 3. TKGM API düşükse → cached parsel dataseti ile test ortamı kur |
| 4. 48 saat çözümsüz → proje sahibine eskalasyon, yazılı özet ile |
|  |
| **## Asla Yapma** |
| - Birim test olmadan hesaplama motorunu production'a alma |
| - Bakanlık cetvelini manuel güncelleme kabul et — otomasyon şart |
| - Tek belediyeye özel hardcode'a izin verme — tüm config DB'den |
| - 'Çalışıyor gibi görünüyor' diyerek formül doğrulamasını atlama |

**2. AGENT GÖREV DAĞILIMI & SINIRLAR**
======================================

Proje üç ana geliştirici rolü üzerinden yürütülür. Sınırlar nettir — sınır ihlali teknik borç ve hata riskini artırır.

|  |  |  |
| --- | --- | --- |
| **Agent** | **Sorumluluk** | **Yapmaz / Sınır** |
| **A — Full Stack** | Harita UI, parsel tespit API, admin panel, TKGM entegrasyonu | Hesaplama formülü yazmaz — sadece backend API'yi çağırır. ML kodlamaz. |
| **B — Backend ML** | Hesaplama motoru, veri ETL, ML model eğitimi, geçmiş vaka entegrasyonu | Frontend yazmaz. Admin panel kodlamaz. Deployment yapmaz. |
| **C — DevOps** | Docker, CI/CD, DB yönetimi, güvenlik, monitoring, backup | Feature kod yazmaz. Hesaplama mantığına dokunmaz. |

**3. SPRINT YAPISI & HAFTALIK RİTİM**
=====================================

2 haftalık sprint döngüsü. Her sprint başı ve sonunda supervisor şu kontrolleri yapar:

**Sprint Başı — Pazartesi**
---------------------------

1. Önceki sprint kabul kriterlerini gözden geçir, tamamlananları işaretle.
2. Yeni görevleri 6-satır şablonla yaz, her agent'a ata.
3. Bağımlılık haritasını güncelle: kim kimi bekliyor?
4. Belediye iletişim durumu: veri talebi yanıtlandı mı?

**Sprint Sonu — Cuma**
----------------------

1. Her agent çıktısını kalite kontrol listesiyle incele.
2. Hesaplama motorunda değişiklik varsa ilgili birim testlerin hepsinin geçtiğini doğrula.
3. Demo hazırlığı: Üsküdar gösterimi için ekran görüntüleri alındı mı?
4. Sonraki sprint için bloker listesi güncelle.

|  |
| --- |
| **KRİTİK KURAL — FORMÜL DEĞİŞİKLİĞİ**  Hesaplama motorunda herhangi bir formül değişikliği supervisor onayı olmadan production'a alınamaz. Her değişiklik şu üçünü gerektiriyor: (1) Yazılı gerekçe — neden değişti? (2) Birim test güncellemesi — hangi test güncellendi veya eklendi? (3) Karşılaştırma tablosu — aynı girdiyle eski ve yeni formülün sonuçları |

**4. BELEDİYE İLETİŞİM PROTOKOLÜ**
==================================

**Veri Talebi Formatı**
-----------------------

|  |
| --- |
| **Her Veri Talebinde Şunlar Olmalı**  • Hangi veri isteniyor (alan adları dahil) • Hangi formatta bekleniyor (GeoJSON, Shapefile, Excel) • Ne için kullanılacak (hangi ekran/özellik için) • Son tarih • Yanıt için iletişim kişisi |

|  |
| --- |
| **Belediyeye Asla Söylenmeyecekler**  • Kesin maliyet rakamı veriyoruz — hayır, tahmin veriyoruz • Riskli bina tespiti yapıyoruz — bu ayrı bir yasal süreç, sistemin dışında • Başka belediye verilerini görüyoruz — izole tenant mimarisi • Vatandaşın tapusuna erişiyoruz — kullanıcı kendisi giriyor |