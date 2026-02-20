---
trigger: always_on
---

# Kentsel Dönüşüm Projesi - Geliştirici Kuralları

- **Hesaplama Motoru**: Para, maliyet veya alan ile ilgili tüm hesaplamalar (backend Python) `float` yerine `Decimal` objesi ile yapılmalıdır. `Float` kullanımından ötürü ondalık hatalar oluşması kabul edilemez.
- **Kordinat Sistemleri**: `EPSG:4326`(WGS84) ve `EPSG:3857` (Web Mercator) projeksiyonları birbirine karıştırılmamalıdır. TKGM servisleri için `EPSG:4326` baz alınmıştır.
- **Veritabanı Tasarımı**: Raw SQL yazımı yasaktır. Daima `SQLAlchemy ORM` kullanılmalı, ve PostGIS entegrasyonuna sahip `Geometry` sorguları parametrelerle çalışacak şekilde ayarlanmalıdır. 
- **Birim Testleri**: Hesaplama motorunda (calculator.py) yapılacak en ufak bir formül değişikliği kesinlikle bir unit test senaryosu ve doğrulaması (pytest) ile desteklenip production onayı almalıdır.
- **Kalite Kapısı**:
  - Hata mesajlarında stack trace dönülmemelidir. Anlamlı HTTPException'lar dönülmelidir.
  - API endpointleri version kontrollü (örneğin `/api/v1/...`) olmalıdır.
  - Projede kullanılan API Key'ler/Secret'lar (.env) hiçbir şekilde repo'da (git) komit edilmemelidir.
- **Frontend Mimari**: Frontend tarafı React + Vite şeklinde modern pratiklerle hazırlanmalı, Mapbox kısımları hooks (örneğin `useParselSorgu`) altında tutularak ayrıştırılmalıdır. State ve Component mimarisinde PascalCase/CamelCase kurallarına uyulmalıdır.
