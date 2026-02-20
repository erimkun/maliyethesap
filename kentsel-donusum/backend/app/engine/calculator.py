from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import date

class ParselInput(BaseModel):
    """Parsel sorgu ve veri tabanı girdi bilgilerini tutar."""
    parsel_alan_m2: Decimal = Field(gt=0, description="Parsel alanı pozitif olmalı")
    kaks: Decimal = Field(ge=0, le=10, description="KAKS katsayısı 0 ile 10 arasında olmalı")
    taks: Decimal = Field(ge=0, le=1, description="TAKS katsayısı 0 ile 1 arasında olmalı")
    bagimsiz_bolum_sayisi: int = Field(ge=1, description="Bağımsız bölüm sayısı minimum 1 olmalı")
    mevcut_yapi_alan_m2: Decimal
    yapi_sinifi: Literal['lüks', 'normal', 'sosyal']
    belediye_kodu: str
    arsa_payi_pay: Optional[int] = None
    arsa_payi_payda: Optional[int] = None

class HesaplamaResult(BaseModel):
    """Hesaplama sonucu dönülecek model."""
    yeni_insaat_alani_m2: Decimal
    ham_insaat_tl: Decimal
    toplam_maliyet_tl: Decimal
    kisi_payi_tl: Decimal
    kat_karsiligi_daire_m2: Decimal
    guvenaraligi_alt_tl: Decimal
    guvenaraligi_ust_tl: Decimal
    arsa_payi_baz: str
    uyari: str
    motor_versiyonu: str
    hesaplama_tarihi: date

class HesaplamaMotoru:
    """Kentsel dönüşüm maliyetlerini float hatası olmadan (Decimal ile) hesaplayan motor."""
    
    def hesapla(self, parsel: ParselInput, birim_bedel: Decimal, tarife: dict) -> HesaplamaResult:
        R = ROUND_HALF_UP
        
        # ADIM 1: İzin verilen yeni inşaat alanı
        yeni_insaat_alani = parsel.parsel_alan_m2 * parsel.kaks
        
        # ADIM 2: Ham inşaat maliyeti
        ham_insaat = yeni_insaat_alani * birim_bedel
        
        # ADIM 3: Ek maliyetler
        proje_musavirlik = ham_insaat * Decimal('0.20')
        yikim = parsel.mevcut_yapi_alan_m2 * Decimal('1000')
        sigorta = ham_insaat * Decimal('0.015')
        
        # ADIM 4: Belediye harçları (sözlükten okunur, str/decimal güvenliğine dikkat)
        ruhsat_harci = yeni_insaat_alani * Decimal(str(tarife.get('ruhsat_harci_tl_m2', 0)))
        altyapi_payi = yeni_insaat_alani * Decimal(str(tarife.get('altyapi_payi_tl_m2', 0)))
        
        # Otopark bedeli farklı formatlarda gelebilir, kontrol edelim.
        otopark_val = tarife.get('otopark_bedeli_tl', tarife.get('otopark_tl', 0))
        otopark_bedeli = Decimal(str(otopark_val))
        
        belediye_harclari = ruhsat_harci + altyapi_payi + otopark_bedeli
        
        # ADIM 5: Toplam Maliyet
        toplam = ham_insaat + proje_musavirlik + yikim + sigorta + belediye_harclari
        
        # ADIM 6: Kişi Başı Pay
        if parsel.arsa_payi_pay and parsel.arsa_payi_payda:
            kisi_payi = toplam * Decimal(str(parsel.arsa_payi_pay)) / Decimal(str(parsel.arsa_payi_payda))
            arsa_payi_baz = 'arsa_payi'
        else:
            kisi_payi = toplam / Decimal(str(parsel.bagimsiz_bolum_sayisi))
            arsa_payi_baz = 'esit_bolum'
            
        # ADIM 7: Kat Karşılığı Senaryosu (Müteahhit %40 alıyor -> vatandaşa %60 kalır)
        kat_krs_toplam_alan = yeni_insaat_alani * Decimal('0.60')
        kat_krs_daire = kat_krs_toplam_alan / Decimal(str(parsel.bagimsiz_bolum_sayisi))
        
        # ADIM 8: Güven Aralığı
        alt = toplam * Decimal('0.85')
        ust = toplam * Decimal('1.20')
        
        return HesaplamaResult(
            yeni_insaat_alani_m2=yeni_insaat_alani.quantize(Decimal('0.01'), rounding=R),
            ham_insaat_tl=ham_insaat.quantize(Decimal('1'), rounding=R),
            toplam_maliyet_tl=toplam.quantize(Decimal('1'), rounding=R),
            kisi_payi_tl=kisi_payi.quantize(Decimal('1'), rounding=R),
            kat_karsiligi_daire_m2=kat_krs_daire.quantize(Decimal('0.01'), rounding=R),
            guvenaraligi_alt_tl=alt.quantize(Decimal('1'), rounding=R),
            guvenaraligi_ust_tl=ust.quantize(Decimal('1'), rounding=R),
            arsa_payi_baz=arsa_payi_baz,
            uyari="Bu bir tahmindir, yasal bağlayıcılığı yoktur.",
            motor_versiyonu="kural_v1.0",
            hesaplama_tarihi=date.today()
        )
