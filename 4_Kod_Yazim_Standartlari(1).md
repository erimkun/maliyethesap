**KOD YAZIM STANDARTLARI**

*Kentsel Dönüşüm Karar Destek Platformu*

**Backend Python, Frontend React, Veritabanı & Güvenlik Standartları**

**1. PYTHON BACKEND STANDARTLARI**
==================================

**1.1 Genel Kurallar**
----------------------

|  |  |
| --- | --- |
| **Kural** | **Detay** |
| **Linter** | ruff (flake8 yerine — 10x daha hızlı). CI'da zorunlu. |
| **Formatter** | black — her commit'te otomatik. |
| **Type hints** | Tüm fonksiyonlarda zorunlu. mypy ile kontrol. |
| **Docstring** | Google tarzı. Public API'lerde zorunlu. |
| **Import sırası** | stdlib → 3rd party → local. isort ile otomatik. |
| **Satır uzunluğu** | 88 karakter (black default). |

|  |
| --- |
| # ✅ DOĞRU — Tam tip işaretli, dokümanlı fonksiyon  from decimal import Decimal  from typing import Optional  def kaks\_hesapla(  parsel\_alan: Decimal,  kaks\_katsayisi: Decimal,  max\_kat: Optional[int] = None,  ) -> Decimal:  """İzin verilen toplam inşaat alanını hesaplar.  Args:  parsel\_alan: Parsel yüzölçümü (m²).  kaks\_katsayisi: Kat alanı katsayısı.  max\_kat: Maksimum kat adedi kısıtı (opsiyonel).  Returns:  İzin verilen toplam inşaat alanı (m²).  """  if parsel\_alan <= 0:  raise ValueError(f'Parsel alanı pozitif olmalı: {parsel\_alan}')  return parsel\_alan \* kaks\_katsayisi |

**1.2 Hata Yönetimi Standartları**
----------------------------------

|  |
| --- |
| **Altın Kural**  Kullanıcıya asla raw stack trace gösterilmez. Tüm hatalar loglanır, kullanıcıya sadece anlamlı mesaj döner. |

|  |
| --- |
| # FastAPI global exception handler  from fastapi import Request  from fastapi.responses import JSONResponse  import logging  logger = logging.getLogger(\_\_name\_\_)  @app.exception\_handler(Exception)  async def genel\_hata\_handler(request: Request, exc: Exception):  logger.error(f'Beklenmedik hata: {exc}', exc\_info=True)  return JSONResponse(status\_code=500, content={  'hata': 'Sistem hatası oluştu. Lütfen tekrar deneyin.',  'istek\_id': request.headers.get('X-Request-ID', 'N/A')  })  # Özel exception sınıfları  class HesaplamaHatasi(Exception): pass  class ParselBulunamadi(Exception): pass  class BelediyeVeriYok(Exception): pass |

**1.3 Veritabanı Kuralları**
----------------------------

* Raw SQL yasak — SQLAlchemy ORM veya parametreli sorgu kullanılır.
* Her migration Alembic ile yapılır ve geri alınabilir (downgrade yazılır).
* N+1 sorgu problemi: ilişkili veri çekerken her zaman joinedload veya selectinload kullan.
* Spatial sorgu için her zaman PostGIS index'i (GIST) oluştur.

|  |
| --- |
| # ✅ PostGIS spatial index — zorunlu  CREATE INDEX idx\_parcels\_geom  ON parcels USING GIST(geom);  # ✅ Koordinattan parsel bulma — parametre ile  SELECT ada\_no, parsel\_no, alan\_m2  FROM parcels  WHERE ST\_Contains(geom, ST\_SetSRID(ST\_MakePoint($1, $2), 4326))  LIMIT 1;  # $1=lon, $2=lat — injection'a karşı parametreli |

**2. REACT FRONTEND STANDARTLARI**
==================================

**2.1 Bileşen Kuralları**
-------------------------

|  |  |
| --- | --- |
| **Kural** | **Detay** |
| **Dosya isimlendirme** | PascalCase: ParselDetay.jsx, MaliyetHesap.jsx |
| **Hook isimlendirme** | usePrefix: useParselData, useMaliyetHesap |
| **State yönetimi** | useState/useReducer local. Paylaşılan state: Context API. |
| **API çağrıları** | Custom hook içinde. Bileşen içinde fetch yasak. |
| **Loading/Error state** | Her API çağrısı loading + error durumunu yönetmeli. |
| **PropTypes / TypeScript** | TypeScript tercih edilir. PropTypes kabul edilir. |

|  |
| --- |
| // ✅ DOĞRU — Custom hook ile API ayrımı  // hooks/useParselData.js  import { useState, useCallback } from 'react';  export function useParselData() {  const [parsel, setParsel] = useState(null);  const [loading, setLoading] = useState(false);  const [error, setError] = useState(null);  const fetchParsel = useCallback(async (lat, lon) => {  setLoading(true);  setError(null);  try {  const res = await fetch(`/api/v1/parsel/${lat}/${lon}`);  if (!res.ok) throw new Error(await res.text());  setParsel(await res.json());  } catch (err) {  setError(err.message);  } finally {  setLoading(false);  }  }, []);  return { parsel, loading, error, fetchParsel };  } |

**3. GÜVENLİK STANDARTLARI**
============================

|  |  |
| --- | --- |
| **Risk** | **Önlem** |
| **SQL Injection** | Tüm DB sorguları parametreli. ORM veya $1/$2 syntax. |
| **XSS** | React varsayılan olarak escape eder. dangerouslySetInnerHTML yasak. |
| **Rate Limiting** | Hesaplama endpoint: 10 istek/dk per IP. TKGM proxy: 30/dk. |
| **Authentication** | JWT + refresh token. Admin panele 2FA zorunlu. |
| **CORS** | Sadece whitelist'teki domainler. '\*' asla production'da. |
| **Env değişkenleri** | Hiçbir secret .env dışında. .env hiçbir zaman git'e girmez. |
| **Input validation** | Pydantic ile backend, Zod ile frontend validation zorunlu. |
| **Log'da kişisel veri** | Koordinat loglanabilir, vatandaş adı/TC asla loglanmaz. |