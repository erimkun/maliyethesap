**HESAPLAMA MOTORU**

*Teknik Detay & İmplementasyon Kılavuzu*

**En İnce Ayrıntısına Kadar — İmar Planı, LLM Entegrasyonu, QR/OCR, API Akışları**

**1. HESAPLAMA MOTORU MİMARİSİ**
================================

Motor üç katmandan oluşur ve her katman birbirinden bağımsız çalışabilir. Çıktılar hibrit olarak birleştirilir.

|  |
| --- |
| **Motor Katmanları**  Katman 1 — Kural Tabanlı (Rule Engine): Bakanlık cetveli + TAKS/KAKS formülleri. Her zaman çalışır. Katman 2 — Veri Tabanlı (Case Matching): Geçmiş vakalarla benzerlik skoru. Yeterli veri olduğunda aktif. Katman 3 — ML Modeli (Faz 4): XGBoost regressör. 500+ vaka birikince devreye girer. Çıktı = weighted average(K1, K2, K3) — ağırlıklar veri kalitesine göre dinamik. |

**2. VERİ GİRDİ KAYNAKLARI — HER BİRİ AYRI AYRI**
=================================================

**2.1 TKGM WMS — Parsel Geometrisi**
------------------------------------

Türkiye Kadastro Genel Müdürlüğü'nün açık WMS servisi parsel sınırlarını ve ada/parsel numaralarını sağlar.

|  |
| --- |
| # TKGM WMS Endpoint  BASE\_URL = 'https://atlas.tkgm.gov.tr/mapcache/wms'  # GetFeatureInfo — koordinattan parsel bilgisi  params = {  'SERVICE' : 'WMS',  'VERSION' : '1.1.1',  'REQUEST' : 'GetFeatureInfo',  'LAYERS' : 'parsel',  'QUERY\_LAYERS': 'parsel',  'INFO\_FORMAT' : 'application/json',  'SRS' : 'EPSG:4326', # WGS84 — kullanıcı koordinatı  'BBOX' : f'{lon-0.001},{lat-0.001},{lon+0.001},{lat+0.001}',  'WIDTH' : '101', # piksel  'HEIGHT' : '101',  'X' : '50', # merkez piksel  'Y' : '50',  'FEATURE\_COUNT': '1'  }  # Dönen JSON'dan çekilen alanlar:  # ada\_no, parsel\_no, il, ilce, mahalle, alan\_m2 |

|  |
| --- |
| **KRİTİK — Projeksiyon**  Kullanıcı koordinatı her zaman EPSG:4326 (GPS, WGS84) formatında gelir. TKGM WMS EPSG:4326 destekler — dönüşüm gerekmez. PostGIS'e yazarken geometry EPSG:4326 olarak saklanır. Harita görüntüleme için Mapbox EPSG:3857 (Web Mercator) kullanır — sadece görüntüleme katmanında dönüşüm var. |

**2.2 Belediye İmar Verisi — Admin Panelden Giriş**
---------------------------------------------------

Belediye GIS verisi farklı formatlarda gelebilir. Her format için ayrı import pipeline'ı gerekir.

|  |  |
| --- | --- |
| **Format** | **İşlem Yöntemi** |
| **GeoJSON** | ST\_GeomFromGeoJSON() ile doğrudan PostGIS'e import. En temiz format. |
| **Shapefile (.shp)** | ogr2ogr ile önce GeoJSON'a çevir, sonra import. Encoding sorunu olabilir (Windows-1254). |
| **Excel / CSV** | ada\_no + parsel\_no sütunları varsa pandas ile oku, geometrisiz sadece özellik verisi olarak sakla. |
| **AutoCAD DXF** | ogr2ogr -f GeoJSON ile çevrim. Koordinat sistemi genelde yerel — dikkat. |
| **PDF İmar Planı** | OCR + LLM pipeline gerekir. Bkz. Bölüm 4. |

|  |
| --- |
| # Shapefile → PostGIS import  ogr2ogr \  -f 'PostgreSQL' \  PG:'host=localhost dbname=kentsel user=app' \  imar\_verileri.shp \  -nln parcels\_uskudar \  -t\_srs EPSG:4326 \ # hedef projeksiyon  -s\_srs EPSG:23035 \ # kaynak (Türkiye ED50 UTM Zone 35)  -lco ENCODING=UTF-8 |

**2.3 Bakanlık Birim Maliyet Cetveli**
--------------------------------------

Çevre ve Şehircilik Bakanlığı her yıl Ocak ayında birim maliyet cetvelini PDF olarak yayınlar. Bu cetvel otomatik olarak sisteme çekilmeli — manuel güncelleme kabul edilemez.

|  |
| --- |
| **Pipeline**  1. Bakanlık web sitesinden PDF otomatik indirilir (cron job, Ocak ayı kontrol). 2. pdfplumber ile tablo çıkarılır. 3. LLM (Claude API) ile yapı sınıfı → m² bedeli eşleştirmesi doğrulanır. 4. Çıktı DB'ye yazılır: {yil, yapi\_sinifi, birim\_bedel\_tl, guncelleme\_tarihi} 5. Supervisor'a e-posta ile güncelleme bildirimi gider. |

|  |
| --- |
| # pdfplumber ile cetvel çekme  import pdfplumber  from anthropic import Anthropic  def extract\_unit\_costs(pdf\_path: str) -> list[dict]:  with pdfplumber.open(pdf\_path) as pdf:  tables = []  for page in pdf.pages:  tables.extend(page.extract\_tables())  # Ham tablo LLM'e gönderilerek yapılandırılır  client = Anthropic()  response = client.messages.create(  model='claude-opus-4-6',  system='Bakanlık maliyet cetvelinden yapı sınıfı ve TL/m² değerlerini JSON array olarak çıkar.',  messages=[{'role':'user','content': str(tables)}]  )  return json.loads(response.content[0].text) |

**3. HESAPLAMA FORMÜLLERI — TAM DETAY**
=======================================

**3.1 Neden float Değil Decimal?**
----------------------------------

Bu projenin en kritik teknik kuralıdır. Para ve maliyet hesabında Python float kullanmak ondalık hata biriktirir.

|  |
| --- |
| # ❌ YANLIŞ — Float kullanımı  maliyet = 500 \* 22500.75 # 11250375.0  print(500 \* 22500.75 == 11250375.0) # False olabilir!  # ✅ DOĞRU — Decimal kullanımı  from decimal import Decimal, ROUND\_HALF\_UP  alan = Decimal('500')  birim\_bedel = Decimal('22500.75')  maliyet = alan \* birim\_bedel # 11250375.00 — kesin  # Yuvarlama: her zaman ROUND\_HALF\_UP  maliyet\_yuvarli = maliyet.quantize(Decimal('0.01'), rounding=ROUND\_HALF\_UP) |

**3.2 Adım Adım Hesaplama Zinciri**
-----------------------------------

|  |
| --- |
| from decimal import Decimal, ROUND\_HALF\_UP  from dataclasses import dataclass  @dataclass  class ParselInput:  parsel\_alan\_m2: Decimal  kaks: Decimal # Kat Alanı Katsayısı  taks: Decimal # Taban Alan Katsayısı  bagimsiz\_bolum\_sayisi: int  mevcut\_yapi\_alan\_m2: Decimal # Yıkılacak bina m²  yapi\_sinifi: str # 'lüks'/'normal'/'sosyal'  belediye\_kodu: str # 'uskudar', 'kadikoy'...  def hesapla(inp: ParselInput, birim\_bedel: Decimal, tarife: dict) -> dict:  # ADIM 1: İzin verilen yeni inşaat alanı  yeni\_insaat\_alani = inp.parsel\_alan\_m2 \* inp.kaks  # ADIM 2: Ham inşaat maliyeti (Bakanlık cetveli)  ham\_insaat = yeni\_insaat\_alani \* birim\_bedel  # ADIM 3: Ek maliyetler  proje\_musavirlik = ham\_insaat \* Decimal('0.20') # %20  yikim = inp.mevcut\_yapi\_alan\_m2 \* Decimal('1000') # 1000 TL/m²  sigorta = ham\_insaat \* Decimal('0.015') # %1.5  # ADIM 4: Belediye harçları (DB'den — belediyeye özgü)  ruhsat\_harci = yeni\_insaat\_alani \* Decimal(str(tarife['ruhsat\_harci\_tl\_m2']))  altyapi\_payi = yeni\_insaat\_alani \* Decimal(str(tarife['altyapi\_payi\_tl\_m2']))  otopark\_bedeli = Decimal(str(tarife.get('otopark\_tl', 0)))  # ADIM 5: Toplam  toplam = (ham\_insaat + proje\_musavirlik + yikim +  sigorta + ruhsat\_harci + altyapi\_payi + otopark\_bedeli)  # ADIM 6: Kişi başı pay (eşit bölüm — arsa payı bilinmiyorsa)  kisi\_payi = toplam / Decimal(str(inp.bagimsiz\_bolum\_sayisi))  # ADIM 7: Kat karşılığı senaryosu  muteahhit\_payi\_orani = Decimal('0.40') # %40 standart  vatandasa\_kalan\_toplam = yeni\_insaat\_alani \* (1 - muteahhit\_payi\_orani)  daire\_basi\_yeni\_alan = vatandasa\_kalan\_toplam / Decimal(str(inp.bagimsiz\_bolum\_sayisi))  R = ROUND\_HALF\_UP  return {  'yeni\_insaat\_alani\_m2' : yeni\_insaat\_alani.quantize(Decimal('0.01'), rounding=R),  'ham\_insaat\_tl' : ham\_insaat.quantize(Decimal('1'), rounding=R),  'toplam\_maliyet\_tl' : toplam.quantize(Decimal('1'), rounding=R),  'kisi\_payi\_tl' : kisi\_payi.quantize(Decimal('1'), rounding=R),  'kat\_karsiligi\_daire\_m2': daire\_basi\_yeni\_alan.quantize(Decimal('0.01'), rounding=R),  'guvenaraligi\_alt' : (toplam \* Decimal('0.85')).quantize(Decimal('1'), rounding=R),  'guvenaraligi\_ust' : (toplam \* Decimal('1.20')).quantize(Decimal('1'), rounding=R),  } |

**4. İMAR PLANI NOTLARININ OKUNMASI**
=====================================

İmar planı notları en karmaşık veri sorunudur. Belediyeden üç farklı formatta gelebilir. Her format için ayrı strateji uygulanır.

**4.1 Format 1: Dijital PDF (Makine Okunabilir)**
-------------------------------------------------

PDF içinde seçilebilir metin varsa pdfplumber ile doğrudan çıkarılır. LLM'e gönderilir, yapılandırılmış veri alınır.

|  |
| --- |
| import pdfplumber  from anthropic import Anthropic  def imar\_notlarini\_coz(pdf\_path: str, ada\_no: str, parsel\_no: str) -> dict:  # Metin çıkar  with pdfplumber.open(pdf\_path) as pdf:  text = ' '.join(page.extract\_text() or '' for page in pdf.pages)  # LLM'e gönder — yapılandırılmış çıktı al  client = Anthropic()  prompt = f'''  Ada: {ada\_no}, Parsel: {parsel\_no} için imar planı notlarından  şu bilgileri JSON olarak çıkar:  - taks (sayı veya null)  - kaks (sayı veya null)  - max\_yukseklik\_m (sayı veya null)  - yapi\_nizam (string: 'ayrik'/'bitisik'/'blok')  - cephe\_cekme\_m (sayı veya null)  - ozel\_kosullar (string listesi)  Belge: {text[:8000]}  '''  response = client.messages.create(  model='claude-opus-4-6',  messages=[{'role':'user','content': prompt}]  )  return json.loads(response.content[0].text) |

**4.2 Format 2: Taranmış PDF (Görsel — OCR Gerekli)**
-----------------------------------------------------

Belediye imar planını tarayarak PDF yapmışsa metin çıkarılamaz. Bu durumda OCR pipeline uygulanır.

|  |
| --- |
| # OCR Pipeline: Taranmış PDF → Metin  import pytesseract  from pdf2image import convert\_from\_path  from PIL import Image  def taranmis\_pdf\_ocr(pdf\_path: str) -> str:  # PDF → görüntü dönüşümü (300 DPI önerilir)  images = convert\_from\_path(pdf\_path, dpi=300)  full\_text = []  for img in images:  # Tesseract — Türkçe dil paketi ile  text = pytesseract.image\_to\_string(img, lang='tur',  config='--psm 6') # Tek blok metin modü  full\_text.append(text)  return ' '.join(full\_text)  # Sonra imar\_notlarini\_coz() ile aynı LLM pipeline |

|  |
| --- |
| **Tesseract Türkçe Kurulumu**  sudo apt-get install tesseract-ocr tesseract-ocr-tur pip install pytesseract pdf2image Pillow DPI önerisi: 300 DPI altında Türkçe karakterler (ş, ğ, ı, ö, ü, ç) hatalı tanınır. Ön işleme: contrast artırma + gürültü azaltma OCR doğruluğunu %15–30 artırır. |

**4.3 Format 3: El Yazısı veya Düşük Kaliteli Tarama**
------------------------------------------------------

El yazısı notlar veya çok düşük kaliteli taramalarda Tesseract başarısız olur. Bu durumda Claude'un vision API'si kullanılır.

|  |
| --- |
| import base64  from anthropic import Anthropic  def el\_yazisi\_oku(image\_path: str) -> dict:  with open(image\_path, 'rb') as f:  img\_data = base64.standard\_b64encode(f.read()).decode('utf-8')  client = Anthropic()  response = client.messages.create(  model='claude-opus-4-6',  messages=[{'role':'user','content':[  {'type':'image','source':{'type':'base64',  'media\_type':'image/jpeg','data':img\_data}},  {'type':'text','text':'Bu imar planı notlarından TAKS, KAKS,  max yukseklik, yapi nizami bilgilerini JSON olarak cikar.}  ]}]  )  return json.loads(response.content[0].text) |

**5. GEÇMİŞ VERİ ENTEGRASYONu — BENZER PARSEL EŞLEŞME**
=======================================================

Geçmiş dönüşüm vakaları sisteme import edildikten sonra, sorgulanan parsele en benzer 5–10 vakayı bulan bir benzerlik algoritması çalışır.

|  |
| --- |
| # Benzerlik skoru hesaplama  import numpy as np  from sklearn.preprocessing import MinMaxScaler  def benzer\_parseller\_bul(sorgu: dict, vakalar: list[dict], k=5) -> list:  """  Özellikler: parsel\_alan\_m2, kaks, bina\_yasi, kat\_adedi, ilce\_kodu  Mesafe: normalize edilmiş Euclidean distance  """  features = ['parsel\_alan\_m2', 'kaks', 'bina\_yasi\_yil', 'kat\_adedi']  # Vaka matrisini hazırla  X = np.array([[v[f] for f in features] for v in vakalar])  sorgu\_vec = np.array([[sorgu[f] for f in features]])  # Normalize et (0-1 aralığına)  scaler = MinMaxScaler()  X\_norm = scaler.fit\_transform(X)  sorgu\_norm = scaler.transform(sorgu\_vec)  # Euclidean mesafe  mesafeler = np.sqrt(((X\_norm - sorgu\_norm)\*\*2).sum(axis=1))  en\_yakin\_idx = np.argsort(mesafeler)[:k]  return [{'vaka': vakalar[i], 'mesafe': mesafeler[i]} for i in en\_yakin\_idx] |

**5.1 Enflasyon Düzeltmesi**
----------------------------

Farklı yıllarda gerçekleşen vakalar doğrudan karşılaştırılamaz. Her geçmiş maliyet güncel yıla TÜFE ile normalize edilir.

|  |
| --- |
| # TÜFE bazlı enflasyon düzeltmesi  from decimal import Decimal  def enflasyon\_duzelt(maliyet\_tl: Decimal, vaka\_yili: int,  hedef\_yil: int, tufe\_db: dict) -> Decimal:  """  tufe\_db = {2020: 14.60, 2021: 19.60, 2022: 72.31,  2023: 64.77, 2024: 58.51, ...} # yıllık TÜFE  """  carpan = Decimal('1')  for yil in range(vaka\_yili + 1, hedef\_yil + 1):  carpan \*= (1 + Decimal(str(tufe\_db[yil])) / 100)  return maliyet\_tl \* carpan |

**6. API ENDPOINT TASARIMI**
============================

|  |  |
| --- | --- |
| **Endpoint** | **Açıklama** |
| **GET /api/v1/parsel/{lat}/{lon}** | Koordinattan parsel bilgisi çek — TKGM WMS proxy |
| **GET /api/v1/parsel/{ada}/{parsel}/imar** | Parselin imar verilerini getir — belediye DB |
| **POST /api/v1/hesapla** | Maliyet hesaplama — istek body'sinde parsel özellikleri |
| **GET /api/v1/benzer-vakalar** | Geçmiş vakalardan benzer parsel listesi |
| **GET /api/v1/bakanlık-birim-bedel/{yil}/{sinif}** | Aktif birim maliyet değeri |
| **POST /api/v1/admin/imar-import** | Belediye imar verisi import (admin only) |
| **PUT /api/v1/admin/tarife/{belediye}** | Belediye harç tarifesini güncelle (admin only) |

|  |
| --- |
| # POST /api/v1/hesapla — istek ve yanıt formatı  # REQUEST BODY:  {  'parsel\_alan\_m2' : 520.5,  'kaks' : 2.0,  'taks' : 0.4,  'bagimsiz\_bolum\_sayisi': 8,  'mevcut\_yapi\_alan\_m2' : 380.0,  'yapi\_sinifi' : 'normal',  'belediye\_kodu' : 'uskudar',  'arsa\_payi\_pay' : 80, # opsiyonel  'arsa\_payi\_payda' : 1000 # opsiyonel  }  # RESPONSE:  {  'toplam\_maliyet\_tl' : 12450000,  'guvenaraligi\_alt\_tl' : 10582500,  'guvenaraligi\_ust\_tl' : 14940000,  'kisi\_payi\_tl' : 1556250,  'kat\_karsiligi\_daire\_m2' : 39.04,  'yeni\_insaat\_alani\_m2' : 1041.0,  'motor\_versiyonu' : 'kural\_v1.2',  'veri\_tarihi' : '2025-01-15',  'uyari' : 'Bu bir tahmindir, yasal bağlayıcılığı yoktur.'  } |

**7. TEST STRATEJİSİ — HESAPLAMA MOTORU**
=========================================

Her hesaplama fonksiyonu için minimum 5 test senaryosu yazılacaktır.

|  |
| --- |
| # pytest — birim test örneği  from decimal import Decimal  import pytest  from engine.calculator import hesapla, ParselInput  MOCK\_BIRIM\_BEDEL = Decimal('22000') # 22.000 TL/m²  MOCK\_TARIFE = {  'ruhsat\_harci\_tl\_m2': '15',  'altyapi\_payi\_tl\_m2': '25',  'otopark\_tl': '50000'  }  class TestHesaplama:  def test\_temel\_senaryo(self):  inp = ParselInput(  parsel\_alan\_m2=Decimal('500'),  kaks=Decimal('2.0'),  taks=Decimal('0.4'),  bagimsiz\_bolum\_sayisi=8,  mevcut\_yapi\_alan\_m2=Decimal('380'),  yapi\_sinifi='normal',  belediye\_kodu='uskudar'  )  sonuc = hesapla(inp, MOCK\_BIRIM\_BEDEL, MOCK\_TARIFE)  # Ham inşaat: 1000 m² × 22000 = 22.000.000 TL  assert sonuc['ham\_insaat\_tl'] == Decimal('22000000')  assert sonuc['toplam\_maliyet\_tl'] > sonuc['ham\_insaat\_tl']  assert sonuc['guvenaraligi\_alt\_tl'] < sonuc['toplam\_maliyet\_tl']  assert sonuc['guvenaraligi\_ust\_tl'] > sonuc['toplam\_maliyet\_tl']  def test\_sifir\_bolum\_hatasi(self):  with pytest.raises(ValueError, match='bagimsiz\_bolum\_sayisi'):  ParselInput(..., bagimsiz\_bolum\_sayisi=0, ...)  def test\_guven\_araligi\_mantikli(self):  # Alt sınır her zaman üst sınırdan küçük  assert sonuc['guvenaraligi\_alt\_tl'] < sonuc['guvenaraligi\_ust\_tl'] |