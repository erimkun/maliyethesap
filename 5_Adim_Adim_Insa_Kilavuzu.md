🏗

**ADIM ADIM İNŞA KILAVUZU**

**Kentsel Dönüşüm Karar Destek Platformu**

*Yapay Zeka Araçlarıyla — Cursor & Claude ile Sıfırdan İnşaat*

**Her adımda tam prompt verilmiştir — kopyala, yapıştır, çalıştır**

|  |
| --- |
| **Bu Kılavuz Kimler İçin?**  • Kod yazmayı az bilen veya hiç bilmeyenler için  • Cursor (AI kod editörü) + Claude kullanacaklar için  • Üsküdar Belediyesi pilot projesini başlatacaklar için  Her adımda ne yapacağın, hangi aracı açacağın, ne yazacağın ve ne görmen gerektiği yazılıdır. |

**HAZIRLIK — Başlamadan Önce Kurulumlar**
=========================================

Bu bölümü bir kez yapacaksın. Bilgisayarına kuracakların: Cursor, Node.js, Python, Git. Hepsini adım adım gösterim.

**Adım H1 — Cursor'ı Kur (AI Kod Editörü)**
-------------------------------------------

1. cursor.com adresine git.
2. 'Download for Windows/Mac' butonuna tıkla — indir ve kur.
3. Cursor'ı aç. İlk açılışta 'Sign up with GitHub' seç. GitHub hesabın yoksa github.com'dan ücretsiz aç.
4. Cursor açıldıktan sonra sağ üstteki ⚙ ikonuna tıkla → 'Models' → 'claude-opus-4-6' seç. Bu en güçlü model.

|  |
| --- |
| **Cursor Nedir?**  Cursor, yapay zekanın içine gömülü olduğu bir kod yazma programıdır. Normal bir kod editörü gibi görünür ama Ctrl+K tuşuna basınca Claude'a 'şunu yaz' diyebilirsin ve kod kendisi yazılır. Siz sadece ne istediğinizi söylüyorsunuz. |

**Adım H2 — Node.js Kur**
-------------------------

1. nodejs.org adresine git.
2. 'LTS' yazan büyük yeşil butona tıkla — indir ve kur (tüm 'Next' butonlarına bas).
3. Kurulum bitti mi kontrol et: Cursor'da Terminal açmak için üstten View → Terminal. Oraya şunu yaz:

|  |
| --- |
| **Terminale Yaz**  node --version Eğer 'v20.x.x' gibi bir şey görüyorsan kurulum tamam. |

**Adım H3 — Python Kur**
------------------------

1. python.org/downloads adresine git.
2. 'Download Python 3.11.x' butonuna tıkla. ÖNEMLI: Kurulum ekranında 'Add Python to PATH' kutucuğunu işaretle.
3. Terminale şunu yaz: python --version → '3.11.x' görmelisin.

**Adım H4 — Proje Klasörü Oluştur**
-----------------------------------

1. Bilgisayarında bir yere 'kentsel-donusum' adlı klasör oluştur (örn: Belgelerim/kentsel-donusum).
2. Cursor'da: File → Open Folder → bu klasörü seç.
3. Artık bu klasör senin 'proje ana merkezi'. Tüm dosyalar buraya gelecek.

**── FAZ 1 ──**

**VERİTABANI & BACKEND**

*Tahmini süre: 3–5 gün (Claude ile birlikte)*

|  |  |
| --- | --- |
| **1** | **Proje İskeletini Oluştur**  *Cursor'da — tahmini 30 dakika* |

Cursor'ı aç. Sağ tarafta 'Chat' panelini aç (Ctrl+Shift+L). Aşağıdaki promptu yapıştır:

|  |
| --- |
| **▶ PROMPT — ADIM 1 — Proje İskeleti**  Sen bir senior Python FastAPI geliştiricisisin.  Aşağıdaki klasör yapısını oluştur:  kentsel-donusum/  backend/  app/  api/v1/ (endpoint'ler buraya)  engine/ (hesaplama motoru buraya)  models/ (veritabanı modelleri)  services/ (TKGM, belediye servisleri)  tests/  requirements.txt  main.py  frontend/  src/  components/  hooks/  pages/  package.json  docker-compose.yml  .env.example  .gitignore  Her klasöre uygun içerikte boş dosyalar oluştur.  requirements.txt içine: fastapi, uvicorn, sqlalchemy,  psycopg2-binary, geoalchemy2, pydantic, httpx, pdfplumber,  pytesseract, anthropic, python-dotenv, alembic, pytest  ekle. package.json içine React + Mapbox GL JS bağımlılıklarını ekle. |

|  |
| --- |
| **Ne Görmelisin?**  Cursor klasör panelinde (solda) backend/ ve frontend/ klasörleri oluşmalı. requirements.txt ve package.json dosyaları içi dolu olmalı. |

|  |  |
| --- | --- |
| **2** | **Veritabanı Modellerini Yaz**  *Cursor'da — tahmini 1 saat* |

Cursor'da backend/app/models/ klasörüne tıkla. Chat panelinde şunu yaz:

|  |
| --- |
| **▶ PROMPT — ADIM 2 — Veritabanı Modelleri**  Sen bir PostgreSQL + PostGIS uzmanısın.  SQLAlchemy ORM kullanarak şu tabloları oluştur:  1. parcels tablosu:  - id (UUID, primary key)  - ada\_no (string)  - parsel\_no (string)  - il\_kodu (string)  - ilce\_kodu (string)  - belediye\_kodu (string)  - geom (Geometry, EPSG:4326) — PostGIS  - alan\_m2 (Numeric — FLOAT DEĞİL)  - created\_at, updated\_at  2. imar\_verileri tablosu:  - id (UUID)  - parsel\_id (FK → parcels)  - taks (Numeric)  - kaks (Numeric)  - max\_yukseklik\_m (Numeric, nullable)  - yapi\_nizam (string: 'ayrik'/'bitisik'/'blok')  - bagimsiz\_bolum\_sayisi (Integer)  - mevcut\_yapi\_alan\_m2 (Numeric)  - yapi\_sinifi (string: 'lüks'/'normal'/'sosyal')  - imar\_notlari (Text, nullable)  - belediye\_kodu (string)  - guncelleme\_tarihi (Date)  3. belediye\_tarifeler tablosu:  - id (UUID)  - belediye\_kodu (string, unique per yil)  - yil (Integer)  - ruhsat\_harci\_tl\_m2 (Numeric)  - altyapi\_payi\_tl\_m2 (Numeric)  - otopark\_bedeli\_tl (Numeric)  - guncelleme\_tarihi (Date)  4. bakanlık\_birim\_maliyetler tablosu:  - id (UUID)  - yil (Integer)  - yapi\_sinifi (string)  - birim\_bedel\_tl\_m2 (Numeric — FLOAT DEĞİL)  - aktif (Boolean)  5. gecmis\_vakalar tablosu:  - id (UUID)  - parsel\_id (FK → parcels, nullable)  - parsel\_alan\_m2 (Numeric)  - kaks (Numeric)  - bina\_yasi\_yil (Integer)  - kat\_adedi (Integer)  - bagimsiz\_bolum\_sayisi (Integer)  - ilce\_kodu (string)  - gerceklesen\_maliyet\_tl (Numeric)  - vaka\_yili (Integer)  - muteahhit\_modeli (string: 'kat\_karsiligi'/'nakit')  NOT: Para ve alan için HER YERDE Numeric kullan,  Float ve Double kesinlikle yasak.  Alembic migration dosyasını da oluştur. |

|  |
| --- |
| **Ne Görmelisin?**  backend/app/models/parcels.py, imar.py, tarife.py, birim\_maliyet.py, gecmis\_vaka.py dosyaları oluşmalı. Alembic klasörü ve migration dosyası hazır olmalı. |

|  |  |
| --- | --- |
| **3** | **Hesaplama Motorunu Yaz**  *Cursor'da — tahmini 2 saat. EN KRİTİK ADIM.* |

Cursor'da backend/app/engine/ klasörüne tıkla. Bu dosyayı oluşturacaksın: calculator.py

|  |
| --- |
| **▶ PROMPT — ADIM 3 — Hesaplama Motoru (calculator.py)**  Sen bir Python uzmanısın. Maliyet hesaplama motoru yazacaksın.  ZORUNLU KURALLAR:  1. Para hesabında HER YERDE Decimal kullan, float yasak  2. Tüm fonksiyonlar type hint'li olmalı  3. Her fonksiyon Google tarzı docstring içermeli  4. Tüm input validation Pydantic ile yapılmalı  Şu sınıf ve fonksiyonları yaz:  class ParselInput(BaseModel):  parsel\_alan\_m2: Decimal (pozitif olmalı)  kaks: Decimal (0-10 arası)  taks: Decimal (0-1 arası)  bagimsiz\_bolum\_sayisi: int (minimum 1)  mevcut\_yapi\_alan\_m2: Decimal  yapi\_sinifi: Literal['lüks', 'normal', 'sosyal']  belediye\_kodu: str  arsa\_payi\_pay: Optional[int] = None  arsa\_payi\_payda: Optional[int] = None  class HesaplamaMotoru:  def hesapla(parsel: ParselInput, birim\_bedel: Decimal,  tarife: dict) -> HesaplamaResult:  # ADIM 1: yeni\_insaat\_alani = parsel\_alan\_m2 \* kaks  # ADIM 2: ham\_insaat = yeni\_insaat\_alani \* birim\_bedel  # ADIM 3: proje\_musavirlik = ham\_insaat \* 0.20  # yikim = mevcut\_yapi\_alan\_m2 \* 1000  # sigorta = ham\_insaat \* 0.015  # ADIM 4: belediye\_harclari = tarifeden hesapla  # ADIM 5: toplam = hepsini topla  # ADIM 6a: arsa\_payi biliniyorsa:  # kisi\_payi = toplam \* (pay/payda)  # ADIM 6b: bilinmiyorsa:  # kisi\_payi = toplam / bagimsiz\_bolum\_sayisi  # ADIM 7: kat\_karsiligi\_daire\_m2:  # = yeni\_insaat\_alani \* 0.60 / bagimsiz\_bolum\_sayisi  # ADIM 8: guven araligi:  # alt = toplam \* 0.85, ust = toplam \* 1.20  # TÜM ara hesaplar ROUND\_HALF\_UP ile yuvarla  class HesaplamaResult(BaseModel):  yeni\_insaat\_alani\_m2: Decimal  ham\_insaat\_tl: Decimal  toplam\_maliyet\_tl: Decimal  kisi\_payi\_tl: Decimal  kat\_karsiligi\_daire\_m2: Decimal  guvenaraligi\_alt\_tl: Decimal  guvenaraligi\_ust\_tl: Decimal  arsa\_payi\_baz: str ('esit\_bolum' veya 'arsa\_payi')  uyari: str (her zaman 'Bu tahmindir...' mesajı)  motor\_versiyonu: str  hesaplama\_tarihi: date |

|  |
| --- |
| **Kritik Kontrol**  Dosya oluştuğunda Cursor'a şunu sor: 'Bu dosyada float kullanılmış yer var mı? Varsa Decimal'a çevir.' Bu kontrolü MUTLAKA yap. |

|  |  |
| --- | --- |
| **4** | **Hesaplama Motorunu Test Et**  *Cursor'da — tahmini 1 saat* |

backend/tests/ klasörüne tıkla. test\_calculator.py dosyası oluşturacaksın:

|  |
| --- |
| **▶ PROMPT — ADIM 4 — Birim Testler**  calculator.py dosyasını okudu. Şimdi bu dosya için  pytest birim testleri yaz. Şu senaryoları test et:  1. TEMEL SENARYO:  500 m² parsel, KAKS 2.0, 8 bağımsız bölüm,  22000 TL/m² birim bedel.  Beklenti: ham\_insaat\_tl = 22.000.000 TL (tam)  2. ARSA PAYI SENARYOSU:  Arsa payı 80/1000 olan mal sahibi,  toplam 10.000.000 TL maliyette ne öder?  Beklenti: 800.000 TL  3. KAT KARŞILIĞI SENARYOSU:  1000 m² yeni inşaat, 10 daire.  Müteahhit %40 alıyor.  Beklenti: daire başı 60 m²  4. HATA SENARYOLARI:  - bagimsiz\_bolum\_sayisi=0 → ValueError fırlatmalı  - parsel\_alan\_m2=-100 → ValidationError fırlatmalı  - kaks=15 (10'dan büyük) → ValidationError fırlatmalı  5. GÜVEN ARALIĞI KONTROLÜ:  alt < toplam < ust her zaman doğru olmalı  6. FLOAT YOK KONTROLÜ:  Tüm Result alanları Decimal tipinde olmalı,  float içermemeli.  Her test açıklayıcı isimli olsun. Mock tarife verisi  fixture olarak tanımla. |

Testleri çalıştır — terminale şunu yaz:

|  |
| --- |
| **Terminale Yaz**  cd backend pip install -r requirements.txt pytest tests/test\_calculator.py -v Hepsi yeşil (PASSED) görünmeli. Kırmızı (FAILED) varsa Cursor'a: 'Bu hata neden çıktı, nasıl düzeltirim?' diye sor. |

|  |  |
| --- | --- |
| **5** | **TKGM WMS Entegrasyonu**  *Cursor'da — tahmini 1.5 saat* |

backend/app/services/ klasörüne tıkla. tkgm\_service.py dosyası oluşturacaksın:

|  |
| --- |
| **▶ PROMPT — ADIM 5 — TKGM WMS Servisi**  Sen bir GIS (coğrafi bilgi sistemi) uzmanısın.  Python httpx kütüphanesi ile TKGM WMS servisine bağlanan  bir servis sınıfı yaz.  TKGM WMS Base URL:  https://atlas.tkgm.gov.tr/mapcache/wms  class TKGMService:  async def koordinattan\_parsel\_bul(  self, lat: float, lon: float  ) -> dict | None:  # WMS GetFeatureInfo isteği gönder  # Parametreler:  # SERVICE=WMS, VERSION=1.1.1  # REQUEST=GetFeatureInfo  # LAYERS=parsel, QUERY\_LAYERS=parsel  # INFO\_FORMAT=application/json  # SRS=EPSG:4326  # BBOX = lon-0.001, lat-0.001, lon+0.001, lat+0.001  # WIDTH=101, HEIGHT=101, X=50, Y=50  # FEATURE\_COUNT=1  # Dönen JSON'dan çıkar: ada\_no, parsel\_no, il, ilce, alan\_m2  # Eğer parsel bulunamazsa None döndür  # Timeout: 10 saniye  # Retry: 3 kez dene  async def parsel\_geometri\_cek(  self, ada\_no: str, parsel\_no: str, ilce: str  ) -> dict | None:  # GetMap ile parsel geometrisini GeoJSON olarak çek  Tüm HTTP hataları logla, kullanıcıya anlamlı mesaj döndür.  httpx.AsyncClient kullan. |

|  |
| --- |
| **Test Etmek İçin**  Terminale şunu yaz (Üsküdar koordinatı): python -c "import asyncio; from app.services.tkgm\_service import TKGMService; s=TKGMService(); print(asyncio.run(s.koordinattan\_parsel\_bul(41.0100, 29.0300)))" Bir ada/parsel numarası dönüyorsa entegrasyon çalışıyor. |

|  |  |
| --- | --- |
| **6** | **API Endpoint'leri Yaz**  *Cursor'da — tahmini 2 saat* |

backend/app/api/v1/ klasörüne tıkla. FastAPI endpoint'lerini oluşturacaksın:

|  |
| --- |
| **▶ PROMPT — ADIM 6 — FastAPI Endpoint'ler**  FastAPI kullanarak şu endpoint'leri yaz:  router = APIRouter(prefix='/api/v1')  1. GET /parsel/{lat}/{lon}  → TKGMService.koordinattan\_parsel\_bul() çağır  → Sonucu DB'de parcels tablosuna upsert et  → Parsel + imar verisini birleştirip döndür  Response: {ada\_no, parsel\_no, ilce, alan\_m2,  taks, kaks, bagimsiz\_bolum\_sayisi,  yapi\_sinifi, imar\_notlari}  2. POST /hesapla  Request Body: ParselInput (Pydantic model)  → DB'den birim\_bedel ve tarife çek (belediye\_kodu'na göre)  → HesaplamaMotoru.hesapla() çağır  → Sonucu döndür  Response: HesaplamaResult  3. GET /birim-bedel/{yil}/{yapi\_sinifi}  → bakanlık\_birim\_maliyetler tablosundan çek  4. GET /health  → {'status': 'ok', 'db': 'connected', 'tkgm': 'reachable'}  Her endpoint için:  - HTTPException ile hata yönetimi  - Pydantic response model tanımı  - Docstring açıklaması  - Rate limit dekoratörü (hesapla için: 10/dakika) |

|  |
| --- |
| **Uygulamayı Başlat**  cd backend uvicorn main:app --reload Tarayıcıda http://localhost:8000/docs adresini aç. Swagger UI görünmeli — tüm endpoint'leri buradan test edebilirsin. |

**── FAZ 2 ──**

**FRONTEND — HARITA & KULLANICI ARAYÜZÜ**

*Tahmini süre: 3–4 gün (Claude ile birlikte)*

|  |  |
| --- | --- |
| **7** | **React Projesini Kur ve Haritayı Ekle**  *Cursor'da — tahmini 1 saat* |

Cursor'da frontend/ klasörüne tıkla. Chat panelinde:

|  |
| --- |
| **▶ PROMPT — ADIM 7 — React + Mapbox Kurulum**  frontend/ klasöründe React uygulaması kurulu.  Şimdi şunları yap:  1. Mapbox GL JS paketini ekle (package.json'a):  mapbox-gl ve react-map-gl  2. src/pages/AnaSayfa.jsx oluştur:  - Tam ekran Mapbox haritası (İstanbul merkezi: 41.01, 29.03)  - Zoom: 13  - Harita stili: mapbox://styles/mapbox/light-v11  - Haritaya tıklandığında o koordinatı state'e kaydet  - Tıklanan noktaya kırmızı marker koy  - Sol tarafta bilgi paneli (300px genişlik)  3. src/hooks/useParselSorgu.js oluştur:  - fetchParsel(lat, lon) fonksiyonu  - GET /api/v1/parsel/{lat}/{lon} çağırır  - loading, error, parselData state'leri döndürür  4. Haritaya tıklanınca useParselSorgu'yu çağır,  sonuç gelince sol panelde göster:  Ada/Parsel: ... | Alan: ... m² | KAKS: ...  Mapbox token için .env dosyasında:  REACT\_APP\_MAPBOX\_TOKEN=pk.XXXXX  (Token almak için: account.mapbox.com → Tokens) |

|  |
| --- |
| **Mapbox Token Nasıl Alınır?**  1. account.mapbox.com adresine git 2. Ücretsiz hesap aç 3. 'Tokens' bölümünden 'Default public token'ı kopyala 4. frontend/.env dosyasına yapıştır: REACT\_APP\_MAPBOX\_TOKEN=pk.eyJ1IjoiXXXX... |

|  |  |
| --- | --- |
| **8** | **Maliyet Hesap Panelini Tasarla**  *Cursor'da — tahmini 2 saat* |

|  |
| --- |
| **▶ PROMPT — ADIM 8 — Maliyet Hesap Paneli**  src/components/MaliyetPaneli.jsx bileşeni oluştur.  Bu panel haritanın sağ tarafında veya altında görünecek.  Panel şunları içermeli:  BÖLÜM 1 — Parsel Bilgileri (otomatik dolu):  Ada/Parsel No, İlçe, Alan (m²), KAKS, TAKS  BÖLÜM 2 — Kullanıcı Girdileri (manuel):  [ ] Arsa payım var (checkbox)  Arsa payı pay / payda (göster/gizle)  Yapı sınıfı seçimi (lüks/normal/sosyal dropdown)  BÖLÜM 3 — Hesapla Butonu  'Dönüşüm Maliyetini Hesapla' — büyük mavi buton  POST /api/v1/hesapla çağırır  BÖLÜM 4 — Sonuç Kartları (hesap sonrası görünür):  Kart 1: Tahmini Toplam Maliyet  X.XXX.XXX TL – Y.YYY.YYY TL  (güven aralığı, turuncu renk)  Kart 2: Senin Payın  Z.ZZZ.ZZZ TL  (kişi başı pay, kırmızı renk)  Kart 3: Kat Karşılığı Senaryosu  Yeni dairenizden X m² size kalır  (yeşil renk)  Alt kısım: Küçük gri uyarı metni:  'Bu hesap tahmindir, yasal bağlayıcılığı yoktur.'  Mobil uyumlu (responsive) tasarım zorunlu.  Tailwind CSS veya CSS Modules kullan. |

|  |
| --- |
| **Tasarım İçin İpucu**  Cursor'a şunu da ekleyebilirsin: 'Tasarımı modern ve sade tut. Vatandaş dostu olsun, teknik terimler açıklamalı gösterilsin.' Bu prompt ile daha iyi UI çıkar. |

|  |  |
| --- | --- |
| **9** | **Frontend'i Çalıştır ve Test Et**  *— tahmini 30 dakika* |

|  |
| --- |
| **Terminale Yaz**  cd frontend npm install npm start Tarayıcıda http://localhost:3000 açılmalı. Harita görünmeli. Bir parsele tıklayınca sol panelde bilgiler gelmeli. |

Çalışıyorsa aynı anda backend de açık olmalı (ayrı terminal):

|  |
| --- |
| **İkinci Terminale Yaz**  cd backend uvicorn main:app --reload İki terminal yan yana açık olacak. Biri backend (8000 portu), biri frontend (3000 portu). |

**── FAZ 3 ──**

**İMAR PLANI NOTLARI & LLM ENTEGRASYONu**

*Tahmini süre: 2–3 gün*

|  |  |
| --- | --- |
| **10** | **Claude API Bağlantısını Kur**  *Cursor'da — tahmini 30 dakika* |

Önce Anthropic API anahtarını al:

1. console.anthropic.com adresine git.
2. Ücretsiz hesap aç. 'API Keys' bölümüne git.
3. 'Create Key' → kopyala → .env dosyasına ekle: ANTHROPIC\_API\_KEY=sk-ant-XXXXX

|  |
| --- |
| **▶ PROMPT — ADIM 10 — Claude API Servisi**  backend/app/services/llm\_service.py dosyasını oluştur.  Anthropic Python SDK kullanarak:  class LLMService:  async def imar\_notu\_parse(self, raw\_text: str,  ada\_no: str, parsel\_no: str) -> dict:  # Claude'a gönder, yapılandırılmış JSON al  # System prompt:  # 'Sen bir imar planı uzmanısın. Verilen metinden  # belirtilen ada/parsel için TAKS, KAKS, max yükseklik,  # yapı nizamı ve özel koşulları JSON olarak çıkar.  # Bulunmayanlar için null döndür.  # Sadece JSON döndür, başka metin ekleme.'  # model: claude-opus-4-6  # Dönen JSON'u parse et ve döndür  async def bakanlık\_cetveli\_parse(self,  tablo\_metni: str) -> list[dict]:  # Bakanlık PDF tablosundan yapı sınıfı → m² bedeli çek  # System prompt:  # 'Bakanlık inşaat maliyet cetvelinden yapı sınıfı ve  # TL/m² değerlerini JSON array olarak çıkar.  # Format: [{yapi\_sinifi: str, birim\_bedel: number}]  # Sadece JSON döndür.'  Hata durumlarını logla. API limiti aşılırsa retry ekle. |

|  |  |
| --- | --- |
| **11** | **PDF İmar Notlarını Oku**  *Cursor'da — tahmini 1.5 saat* |

|  |
| --- |
| **▶ PROMPT — ADIM 11 — PDF İmar Notu Okuma Servisi**  backend/app/services/imar\_ocr\_service.py oluştur.  Üç farklı durumu ele al:  class ImarOCRService:  async def pdf\_isle(self, pdf\_path: str,  ada\_no: str, parsel\_no: str) -> dict:  # DURUM 1: Seçilebilir metin içeren PDF  # pdfplumber ile metni çıkar  # eğer metin uzunluğu > 100 karakter ise:  # LLMService.imar\_notu\_parse() çağır  # DURUM 2: Taranmış PDF (metin çıkarılamıyor)  # pdf2image ile sayfalara çevir (300 DPI)  # pytesseract ile OCR (lang='tur')  # elde edilen metni LLMService.imar\_notu\_parse() çağır  # DURUM 3: OCR başarısız (el yazısı / çok düşük kalite)  # İlk sayfayı JPEG'e çevir  # Claude Vision API ile görüntüyü gönder  # (base64 encode, image/jpeg media\_type)  # Hangi yöntemin kullanıldığını sonuçta belirt:  # {'metod': 'pdf\_text'/'ocr'/'vision', ...sonuçlar}  def \_pdf\_metin\_cek(self, pdf\_path: str) -> str:  # pdfplumber ile metin çıkarma  def \_ocr\_uygula(self, pdf\_path: str) -> str:  # pdf2image + pytesseract pipeline  # Ön işleme: kontrast artır, gürültü azalt  async def \_vision\_ile\_oku(self, image\_path: str) -> dict:  # Claude Vision API |

|  |
| --- |
| **Test Dosyası**  Üsküdar'dan bir imar planı PDF'i al (veya belediyeden iste). backend/tests/ klasörüne koy. Cursor'a: 'test\_ocr.py yaz, gerçek PDF dosyasıyla imar\_ocr\_service'i test et' de. |

**── FAZ 4 ──**

**BELEDİYE YÖNETİM PANELİ**

*Tahmini süre: 2–3 gün*

|  |  |
| --- | --- |
| **12** | **Admin Panel — Veri Giriş Ekranları**  *Cursor'da — tahmini 2 saat* |

|  |
| --- |
| **▶ PROMPT — ADIM 12 — Belediye Admin Paneli**  src/pages/AdminPanel.jsx sayfası oluştur.  Bu sayfa sadece 'belediye' rolündeki kullanıcılara açık.  Sayfa 3 sekme içerecek:  SEKME 1 — İmar Verisi Girişi:  Form alanları:  - Ada no, Parsel no (text input)  - TAKS, KAKS (number input, validasyon: 0-10)  - Bağımsız bölüm sayısı (integer)  - Yapı nizamı (dropdown: ayrık/bitişik/blok)  - Yapı sınıfı (dropdown: lüks/normal/sosyal)  - İmar notları (textarea)  - İmar planı PDF yükleme (file upload)  'Kaydet' butonu → POST /api/v1/admin/imar  SEKME 2 — Tarife Güncelleme:  - Yıl seçimi (dropdown)  - Ruhsat harcı (TL/m²)  - Altyapı katılım payı (TL/m²)  - Otopark bedeli (TL sabit)  'Güncelle' butonu → PUT /api/v1/admin/tarife  SEKME 3 — Sorgulama İstatistikleri:  - Son 7 gün kaç sorgu yapıldı (basit sayı)  - En çok sorgulanan 5 mahalle listesi  GET /api/v1/admin/istatistik  Tasarım: Sade, belediye çalışanı için kolay. Hata  mesajları Türkçe. Başarılı kayıtta yeşil bildirim. |

**── FAZ 5 ──**

**YAYINA ALMA (DEPLOYMENT)**

*Tahmini süre: 1–2 gün*

|  |  |
| --- | --- |
| **13** | **Docker ile Paketleme**  *Cursor'da — tahmini 1 saat* |

|  |
| --- |
| **▶ PROMPT — ADIM 13 — Docker Kurulumu**  docker-compose.yml dosyasını tamamla. İçinde olması gerekenler:  services:  db:  image: postgis/postgis:15-3.3  environment:  POSTGRES\_DB: kentsel\_donusum  POSTGRES\_USER: app  POSTGRES\_PASSWORD: ${DB\_PASSWORD}  volumes: [postgres\_data:/var/lib/postgresql/data]  ports: ['5432:5432']  backend:  build: ./backend  environment:  DATABASE\_URL: postgresql://app:${DB\_PASSWORD}@db/kentsel  ANTHROPIC\_API\_KEY: ${ANTHROPIC\_API\_KEY}  depends\_on: [db]  ports: ['8000:8000']  frontend:  build: ./frontend  ports: ['3000:3000']  environment:  REACT\_APP\_API\_URL: http://backend:8000  volumes:  postgres\_data:  Ayrıca backend/Dockerfile ve frontend/Dockerfile oluştur.  Her ikisi de production-ready multi-stage build olsun. |

|  |
| --- |
| **Terminale Yaz**  docker-compose up --build Her şey ayakta kalkarsa: http://localhost:3000 aç. Uygulama tam çalışıyor olmalı. |

|  |  |
| --- | --- |
| **14** | **Render.com'a Deploy**  *— tahmini 1 saat. Üsküdar demosu için.* |

1. render.com → ücretsiz hesap aç.
2. GitHub'a kodunu yükle (Cursor'da Source Control panelinden).
3. Render'da 'New Web Service' → GitHub reposunu bağla.
4. Backend için: Environment = Docker, Root Directory = backend.
5. Frontend için: Environment = Static Site, Build Command = npm run build.
6. PostgreSQL için: Render'da 'New PostgreSQL' → PostGIS extension'ı ekle.
7. Environment variable'ları Render paneline ekle (.env değerlerini).

|  |
| --- |
| **Demo Linki**  Render deploy ettikten sonra sana bir URL verir: https://kentsel-donusum-backend.onrender.com https://kentsel-donusum.onrender.com Bu linkleri Üsküdar toplantısına götür. |

**── FAZ 6 ──**

**GEÇMİŞ VERİ ENTEGRASYONu & YAPAY ZEKA**

*Tahmini süre: 1 hafta — elindeki vakalar hazır olduktan sonra*

|  |  |
| --- | --- |
| **15** | **Geçmiş Vakaları Sisteme Import Et**  *Cursor'da* |

Elindeki geçmiş dönüşüm maliyet verilerini önce Claude ile analiz et. Claude.ai'da yeni bir konuşma aç ve şu promptu yaz:

|  |
| --- |
| **▶ PROMPT — CLAUDE.AI'DA ÇALIŞTIR — Veri Analizi**  Sana bir Excel/CSV dosyası yapıştıracağım.  Bu dosya geçmiş kentsel dönüşüm maliyet vakalarımı içeriyor.  Lütfen şunları yap:  1. Hangi sütunlar var? Listele.  2. Hangi sütunlar eksik veya boş? Kaç kayıt var?  3. Bu alanları standart şemama eşleştir:  parsel\_alan\_m2, kaks, bina\_yasi\_yil, kat\_adedi,  bagimsiz\_bolum\_sayisi, ilce\_kodu, gerceklesen\_maliyet\_tl,  vaka\_yili, muteahhit\_modeli  4. Hangi alanlar eksik, nasıl doldurabiliriz?  5. Bana SQL INSERT komutlarını yaz.  [Buraya Excel verisini yapıştır veya dosya yükle] |

Claude'un analizi bittikten sonra Cursor'da:

|  |
| --- |
| **▶ PROMPT — ADIM 15 — Import Script**  backend/scripts/import\_gecmis\_vakalar.py yaz.  Bu script:  1. CSV/Excel dosyasını oku (pandas)  2. Her satır için vaka\_yili'ni alıp  TÜFE ile 2025'e normalize et:  tüfe\_carpanlari = {2020:1.45, 2021:1.65, 2022:2.23,  2023:3.35, 2024:4.82}  normalize\_maliyet = maliyet \* carpan  3. gecmis\_vakalar tablosuna toplu insert et  4. Başarısız kayıtları logla, atla  5. Sonunda: 'X kayıt eklendi, Y hata' özeti bas |

|  |  |
| --- | --- |
| **16** | **Benzer Parsel Eşleştirme**  *Cursor'da* |

|  |
| --- |
| **▶ PROMPT — ADIM 16 — Benzerlik Servisi**  backend/app/services/benzerlik\_service.py oluştur.  class BenzerlikServisi:  def benzer\_vakalar\_bul(  self, sorgu: dict, k: int = 5  ) -> list[dict]:  # DB'den tüm vakaları çek  # Özellik vektörü: [parsel\_alan\_m2, kaks,  # bina\_yasi\_yil, kat\_adedi]  # MinMaxScaler ile normalize et  # Euclidean mesafe hesapla  # En yakın k vakayı döndür:  # [{vaka\_id, parsel\_alan, kaks, gerceklesen\_maliyet,  # normalize\_maliyet, vaka\_yili, benzerlik\_skoru}]  def hibrit\_tahmin(  self, kural\_tahmini: Decimal,  benzer\_vakalar: list[dict]  ) -> dict:  # Kural motoru tahmini: %60 ağırlık  # Benzer vakalar ortalaması: %40 ağırlık  # Eğer benzer vaka 5'ten azsa ağırlık: %80 / %20  # Sonuç: hibrit tahmin + güncellenmiş güven aralığı  /api/v1/benzer-vakalar endpoint'ini güncelle:  → sorgu parseli için benzerlik servisi çalıştır  → sonuçları API'den döndür  → hesapla endpoint'ine hibrit tahmin ekle |

**GENEL KONTROL LİSTESİ — DEMO ÖNCESİ**
=======================================

Üsküdar Belediyesi toplantısına girmeden önce aşağıdakiler tamamlanmış olmalı:

**Backend ✓**
-------------

|  |  |
| --- | --- |
| **☐** | Veritabanı modelleri oluşturuldu ve migration çalıştırıldı |
| **☐** | TKGM WMS entegrasyonu çalışıyor (test koordinatıyla denenmiş) |
| **☐** | Hesaplama motoru tüm birim testleri geçiyor (pytest yeşil) |
| **☐** | API endpoint'ler Swagger'da görünüyor ve test edildi |
| **☐** | float kullanımı yok — Decimal kontrolü yapıldı |
| **☐** | Belediye tarife tablosu Üsküdar verileriyle dolu |
| **☐** | Bakanlık 2025 birim maliyet cetveli DB'ye girildi |

**Frontend ✓**
--------------

|  |  |
| --- | --- |
| **☐** | Harita açılıyor ve İstanbul'u gösteriyor |
| **☐** | Parsele tıklayınca ada/parsel bilgisi geliyor |
| **☐** | Maliyet hesap paneli çalışıyor |
| **☐** | Güven aralığı gösteriliyor |
| **☐** | Uyarı metni ('Bu tahmindir...') görünüyor |
| **☐** | Mobil görünüm düzgün (telefonda test edildi) |

**Genel ✓**
-----------

|  |  |
| --- | --- |
| **☐** | Uygulama internette erişilebilir (Render URL'si çalışıyor) |
| **☐** | Üsküdar'dan en az 3 gerçek parsel denenmiş |
| **☐** | Hata durumları düzgün mesaj veriyor (stack trace yok) |
| **☐** | Demo için örnek parsel listesi hazır |

**SIKÇA KARŞILAŞILAN SORUNLAR**
===============================

|  |  |
| --- | --- |
| **Sorun** | **Çözüm** |
| **TKGM'den veri gelmiyor** | VPN kullanıyorsan kapat. Sunucu arasıra düşüyor, 5 dakika bekle ve tekrar dene. BBOX parametrelerinin doğru hesaplandığını kontrol et. |
| **'ModuleNotFoundError' hatası** | pip install -r requirements.txt komutunu tekrar çalıştır. Sanal ortam (venv) kullanıyorsan aktif ettiğinden emin ol: source venv/bin/activate |
| **Harita görünmüyor** | Mapbox token'ı .env'e doğru girdiğini kontrol et. Token 'pk.' ile başlamalı. Konsol hatası F12 ile bak. |
| **Decimal hataları** | Sayıları string olarak ver: Decimal('22000') — parantez içinde tırnak. Decimal(22000.5) yanlış, Decimal('22000.5') doğru. |
| **CORS hatası** | Backend main.py'de CORS middleware aktif mi? Frontend URL'si whitelist'te mi? |
| **PostGIS yüklenmedi** | PostgreSQL veritabanında: CREATE EXTENSION postgis; komutunu çalıştır. |

**YARDIM ALMA — CURSOR'A NASIL SORMALIYIM?**
============================================

Cursor'da sorun yaşadığında şu kalıpları kullan:

|  |
| --- |
| **Hata Durumunda**  'Şu hatayı alıyorum: [hatayı buraya yapıştır]. Neden oluyor ve nasıl düzeltirim?' |

|  |
| --- |
| **Anlamadığında**  'Bu kodu basit Türkçe ile adım adım açıkla. Her satırın ne işe yaradığını söyle.' |

|  |
| --- |
| **Geliştirmek İstediğinde**  'Bu bileşene [özelliği] eklemek istiyorum. Mevcut kodu bozmadan nasıl yaparım?' |

|  |
| --- |
| **Test Etmek İstediğinde**  'Bu fonksiyon için pytest testi yaz. Şu senaryoları kapsamalı: [senaryo listesi]' |