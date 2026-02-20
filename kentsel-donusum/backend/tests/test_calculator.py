import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.engine.calculator import HesaplamaMotoru, ParselInput

@pytest.fixture
def motor():
    return HesaplamaMotoru()

@pytest.fixture
def mock_tarife():
    return {
        'ruhsat_harci_tl_m2': '15',
        'altyapi_payi_tl_m2': '25',
        'otopark_tl': '50000'
    }

def test_temel_senaryo(motor, mock_tarife):
    inp = ParselInput(
        parsel_alan_m2=Decimal('500'),
        kaks=Decimal('2.0'),
        taks=Decimal('0.4'),
        bagimsiz_bolum_sayisi=8,
        mevcut_yapi_alan_m2=Decimal('380'),
        yapi_sinifi='normal',
        belediye_kodu='uskudar'
    )
    sonuc = motor.hesapla(inp, Decimal('22000'), mock_tarife)
    
    # 500 * 2.0 = 1000 m2
    # Ham insaat = 1000 * 22000 = 22,000,000
    assert sonuc.ham_insaat_tl == Decimal('22000000')
    assert sonuc.toplam_maliyet_tl > sonuc.ham_insaat_tl

def test_arsa_payi_senaryosu(motor, mock_tarife):
    inp = ParselInput(
        parsel_alan_m2=Decimal('500'),
        kaks=Decimal('2.0'),
        taks=Decimal('0.4'),
        bagimsiz_bolum_sayisi=8,
        mevcut_yapi_alan_m2=Decimal('380'),
        yapi_sinifi='normal',
        belediye_kodu='uskudar',
        arsa_payi_pay=80,
        arsa_payi_payda=1000
    )
    sonuc = motor.hesapla(inp, Decimal('22000'), mock_tarife)
    pay = sonuc.toplam_maliyet_tl * Decimal('80') / Decimal('1000')
    assert sonuc.kisi_payi_tl == pay.quantize(Decimal('1'))
    assert sonuc.arsa_payi_baz == 'arsa_payi'

def test_kat_karsiligi_senaryosu(motor, mock_tarife):
    inp = ParselInput(
        parsel_alan_m2=Decimal('500'),
        kaks=Decimal('2.0'),
        taks=Decimal('0.4'),
        bagimsiz_bolum_sayisi=10,
        mevcut_yapi_alan_m2=Decimal('380'),
        yapi_sinifi='normal',
        belediye_kodu='uskudar'
    )
    sonuc = motor.hesapla(inp, Decimal('22000'), mock_tarife)
    # 500 * 2 = 1000m2. 1000*0.6 = 600m2. 600/10 = 60m2
    assert sonuc.kat_karsiligi_daire_m2 == Decimal('60.00')

def test_hata_senaryolari():
    with pytest.raises(ValidationError):
        ParselInput(
            parsel_alan_m2=Decimal('500'),
            kaks=Decimal('2.0'),
            taks=Decimal('0.4'),
            bagimsiz_bolum_sayisi=0, # error: min 1
            mevcut_yapi_alan_m2=Decimal('380'),
            yapi_sinifi='normal',
            belediye_kodu='uskudar'
        )
    with pytest.raises(ValidationError):
        ParselInput(
            parsel_alan_m2=Decimal('-100'), # error: min 0
            kaks=Decimal('2.0'),
            taks=Decimal('0.4'),
            bagimsiz_bolum_sayisi=8,
            mevcut_yapi_alan_m2=Decimal('380'),
            yapi_sinifi='normal',
            belediye_kodu='uskudar'
        )
    with pytest.raises(ValidationError):
        ParselInput(
            parsel_alan_m2=Decimal('500'), 
            kaks=Decimal('15.0'), # error: max 10
            taks=Decimal('0.4'),
            bagimsiz_bolum_sayisi=8,
            mevcut_yapi_alan_m2=Decimal('380'),
            yapi_sinifi='normal',
            belediye_kodu='uskudar'
        )

def test_guven_araligi_kontrolu(motor, mock_tarife):
    inp = ParselInput(
        parsel_alan_m2=Decimal('500'), kaks=Decimal('2.0'), taks=Decimal('0.4'),
        bagimsiz_bolum_sayisi=8, mevcut_yapi_alan_m2=Decimal('380'),
        yapi_sinifi='normal', belediye_kodu='uskudar'
    )
    sonuc = motor.hesapla(inp, Decimal('22000'), mock_tarife)
    assert sonuc.guvenaraligi_alt_tl < sonuc.toplam_maliyet_tl
    assert sonuc.toplam_maliyet_tl < sonuc.guvenaraligi_ust_tl

def test_float_yok_kontrolu(motor, mock_tarife):
    inp = ParselInput(
        parsel_alan_m2=Decimal('500'), kaks=Decimal('2.0'), taks=Decimal('0.4'),
        bagimsiz_bolum_sayisi=8, mevcut_yapi_alan_m2=Decimal('380'),
        yapi_sinifi='normal', belediye_kodu='uskudar'
    )
    sonuc = motor.hesapla(inp, Decimal('22000'), mock_tarife)
    
    # Check that they are Decimal types, not float
    assert type(sonuc.ham_insaat_tl) == Decimal
    assert type(sonuc.toplam_maliyet_tl) == Decimal
    assert type(sonuc.kisi_payi_tl) == Decimal
    assert type(sonuc.kat_karsiligi_daire_m2) == Decimal
    assert type(sonuc.guvenaraligi_alt_tl) == Decimal
    assert type(sonuc.guvenaraligi_ust_tl) == Decimal
