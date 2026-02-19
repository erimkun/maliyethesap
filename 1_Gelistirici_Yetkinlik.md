**GELİŞTİRİCİ YETKİNLİK ÇERÇEVESİ**

*Kentsel Dönüşüm Karar Destek Platformu*

**Agent Rolleri, Skill Tanımları & İşe Alım Kriterleri**

**1. GENEL ÇERÇEVE**
====================

Bu belge, Kentsel Dönüşüm Karar Destek Platformu projesinde görev alacak yazılımcıların her bir rol için sahip olması gereken teknik ve davranışsal yetkinlikleri tanımlamaktadır. Her rol için 'zorunlu', 'güçlü tercih' ve 'artı değer' olarak üç seviye belirlenmiştir.

|  |
| --- |
| **Proje Teknik Yığını (Özet)**  Frontend: React.js + Mapbox GL JS Backend: Python FastAPI DB: PostgreSQL + PostGIS ML: Python scikit-learn / XGBoost Harita: TKGM WMS + OpenStreetMap Mobil (Faz 4): React Native Infra: Docker + GitHub Actions CI/CD |

**2. ROL 1 — FULL STACK GELİŞTİRİCİ**
=====================================

Platformun hem frontend hem backend katmanını geliştirir. Harita entegrasyonu, parsel sorgulama API'si ve belediye admin panelinden sorumludur. En kritik roldür.

**2.1 Frontend Yetkinlikleri**
------------------------------

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **React.js (Hooks + Context)** | **Zorunlu** | useState/useEffect/useContext kullanımını açıklayabilmeli. Gereksiz re-render'ları nasıl önlersin? |
| **Mapbox GL JS veya Leaflet** | **Zorunlu** | Harita üzerine polygon layer ekleyip tıklama eventi dinleyebilmeli. WMS tile katmanı nasıl eklenir? |
| **REST API entegrasyonu (fetch/axios)** | **Zorunlu** | Async/await ile hata yönetimi, loading state, retry mekanizması |
| **TypeScript** | **Güçlü Tercih** | Interface tanımlama, generic kullanımı. Runtime hatalarını type safety ile nasıl önlersin? |
| **Responsive CSS (Tailwind veya CSS Modules)** | **Güçlü Tercih** | Mobil uyumluluk. Flex ve Grid farkını ne zaman kullanırsın? |
| **Web Geolocation API** | **Güçlü Tercih** | navigator.geolocation.getCurrentPosition kullanımı, hata durumları |
| **DeviceOrientation API (pusula)** | **Artı Değer** | Telefon yön verisini okuma — mobil faz için kritik |

**2.2 Backend Yetkinlikleri**
-----------------------------

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **Python FastAPI** | **Zorunlu** | Endpoint tanımlama, Pydantic model validasyonu, async endpoint yazımı |
| **PostgreSQL + PostGIS** | **Zorunlu** | ST\_Contains, ST\_Intersects gibi uzamsal sorgular. Koordinattan parsel bulmak için hangi fonksiyonu kullanırsın? |
| **OGC WMS/WFS protokolü** | **Zorunlu** | GetFeatureInfo isteği nasıl yapılır? TKGM WMS'den parsel geometrisi çekme |
| **REST API tasarımı** | **Zorunlu** | Resource naming, HTTP method seçimi, status code kullanımı, versiyonlama |
| **JWT authentication** | **Güçlü Tercih** | Token yenileme, refresh token stratejisi |
| **Docker** | **Güçlü Tercih** | Multi-stage Dockerfile, docker-compose ile local geliştirme ortamı |
| **Redis (cache)** | **Artı Değer** | Parsel verisi cache'leme — aynı parselin tekrar tekrar TKGM'den çekilmesini önlemek |

**2.3 Coğrafi Veri Yetkinlikleri — KRİTİK**
-------------------------------------------

|  |
| --- |
| **Neden Bu Kadar Önemli?**  Projenin kalbi coğrafi veri işlemedir. Koordinat sistemleri, projeksiyon dönüşümleri ve uzamsal sorgular hatalı yapıldığında parseller yanlış eşleşir — bu uygulama için kabul edilemez bir hata. |

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **Koordinat sistemleri (WGS84 / EPSG:4326 vs EPSG:3857)** | **Zorunlu** | EPSG:4326 ile EPSG:3857 farkı nedir? TKGM hangi projeksiyon kullanır? |
| **GeoJSON formatı** | **Zorunlu** | Feature, FeatureCollection, Geometry tipleri. Polygon koordinat sırası önemli mi? |
| **Shapefile okuma/dönüştürme** | **Güçlü Tercih** | Belediye GIS verisi Shapefile olarak gelebilir — ogr2ogr veya Fiona ile import |
| **Bounding box sorgusu** | **Güçlü Tercih** | Harita görünümündeki parselleri verimli çekmek için spatial index kullanımı |

**3. ROL 2 — BACKEND & ML GELİŞTİRİCİ**
=======================================

Hesaplama motorunu, veri pipeline'ını ve makine öğrenmesi modelini geliştirir. Matematiksel doğruluk bu rolün birincil sorumluluğudur.

**3.1 Hesaplama Motoru Yetkinlikleri**
--------------------------------------

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **Python (ileri seviye)** | **Zorunlu** | Dataclass, typing, context manager, decorator kullanımı. Saf fonksiyon ne demek? |
| **Sayısal hesaplama (Decimal vs float)** | **Zorunlu** | Para/maliyet hesabında neden float kullanılmaz? Python Decimal modülünü açıkla. |
| **Birim test yazımı (pytest)** | **Zorunlu** | Hesaplama fonksiyonlarının her edge case'i test edilmeli. Test coverage nasıl ölçülür? |
| **Kural motoru tasarımı** | **Güçlü Tercih** | Belediyeye göre değişen tarife kuralları nasıl modellenir? Strateji pattern kullanımı. |
| **Bakanlık cetveli entegrasyonu** | **Güçlü Tercih** | PDF'den yapı sınıfı birim bedelleri çekilecek — pdfplumber veya tabula kullanımı |

**3.2 ML Yetkinlikleri (Faz 3+)**
---------------------------------

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **scikit-learn** | **Zorunlu (Faz 3)** | Pipeline oluşturma, cross-validation, feature importance çıkarma |
| **XGBoost / LightGBM** | **Güçlü Tercih** | Gradient boosting hiperparametre tuning. Overfitting nasıl tespit edilir? |
| **Feature engineering** | **Zorunlu (Faz 3)** | Kategorik değişken encoding, enflasyon düzeltmesi, outlier tespiti |
| **MLflow veya benzeri** | **Artı Değer** | Model versiyonlama, experiment tracking |
| **Pandas + NumPy** | **Zorunlu** | Veri temizleme, merge, groupby, pivot. 10.000 satır veriyi nasıl işlersin? |

**3.3 Veri Mühendisliği Yetkinlikleri**
---------------------------------------

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **ETL pipeline tasarımı** | **Zorunlu** | Geçmiş vaka verilerini standart şemaya dönüştürme pipeline'ı |
| **Veri kalite kontrolü** | **Zorunlu** | Eksik alan tespiti, aykırı değer (outlier) işleme, duplicate yönetimi |
| **PostGIS uzamsal join** | **Güçlü Tercih** | Koordinata göre parsel bulma, mahalle bazlı gruplama |
| **Enflasyon düzeltmesi** | **Güçlü Tercih** | Farklı yıllardaki maliyet verilerini güncel TL'ye normalize etme — TÜFE bazlı |

**4. ROL 3 — DEVOPS / ALTYAPI MÜHENDİSİ**
=========================================

Deployment pipeline'ını, güvenliği ve ölçeklenebilirliği yönetir. Özellikle birden fazla belediyeye ölçeklenme aşamasında kritik hale gelir.

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **Docker + docker-compose** | **Zorunlu** | Multi-container uygulama yönetimi. Volume, network, env değişkeni kullanımı |
| **GitHub Actions CI/CD** | **Zorunlu** | Test → build → deploy pipeline'ı. Branch koruması nasıl yapılır? |
| **PostgreSQL yönetimi** | **Zorunlu** | Backup stratejisi, connection pooling (PgBouncer), index optimizasyonu |
| **Nginx reverse proxy** | **Zorunlu** | SSL termination, rate limiting, upstream yapılandırması |
| **Kubernetes (veya Render/Railway)** | **Güçlü Tercih** | Multi-tenant deployment — her belediye izole ortamda mı yoksa shared DB'de mi? |
| **Monitoring (Prometheus + Grafana)** | **Güçlü Tercih** | API yanıt süresi, DB sorgu süresi, hesaplama motoru latency izleme |
| **Güvenlik (OWASP Top 10)** | **Zorunlu** | SQL injection önleme, rate limiting, input sanitization |

**5. DAVRANIŞ & ÇALIŞMA STİLİ YETKİNLİKLERİ**
=============================================

Teknik yetkinlik kadar önemli olan davranışsal yetkinliklerdir. Özellikle belediyelerle çalışılan bir projede şu özellikler aranmalıdır:

|  |  |  |
| --- | --- | --- |
| **Yetkinlik** | **Seviye** | **Beklenti & Kontrol Sorusu** |
| **Belirsizlikte çalışabilme** | **Zorunlu** | Belediye verisi her zaman eksik veya kirli gelir. 'Veri gelene kadar devam edemem' diyemez. |
| **Hesap verebilirlik** | **Zorunlu** | Maliyet hesabı yanlışsa vatandaş zarar görür. Her değişiklik gerekçelendirilmeli. |
| **Dokümantasyon disiplini** | **Zorunlu** | Formüller değiştiğinde sadece kodu değil, nedenini de yazmalı. |
| **Kamu sektörü anlayışı** | **Güçlü Tercih** | Belediye onay süreçleri yavaştır. Beklemeyi planlayabilmeli, bloklamamalı. |
| **Şeffaf tahmin verme** | **Zorunlu** | Emin olmadığında söylemeli. Yanlış bir güven aralığı, doğru bir 'bilmiyorum'dan kötüdür. |

**6. İŞE ALIM SORULARI — KONTROL LİSTESİ**
==========================================

**6.1 Full Stack Geliştirici İçin**
-----------------------------------

* Bir harita üzerine WMS katmanı ekleyin ve kullanıcının tıkladığı noktadaki parseli getirin — nasıl yaparsınız?
* PostGIS ile 'şu koordinatı içeren parseli bul' sorgusu yazın.
* Bir API endpoint'i hem eski hem yeni istemcilere aynı anda hizmet verecek şekilde nasıl versiyonlarsınız?
* Aynı parselin her sorguda TKGM'den çekilmesini önlemek için ne yaparsınız?

**6.2 Backend & ML Geliştirici İçin**
-------------------------------------

* İnşaat maliyet hesabında neden float yerine Decimal kullanıyoruz? Bir örnek üzerinden gösterin.
* 500 geçmiş dönüşüm vakası var, bir kısmında bina yaşı eksik. Bu eksik veriyi ML modelinde nasıl ele alırsınız?
* Bakanlık birim maliyet cetveli her yıl değişiyor. Bu değişikliği sistemde nasıl yönetirsiniz?
* Modeliniz %15 hatalı tahmin verdi ve gerçek maliyetin altında kalıyor. Sebebi ne olabilir?