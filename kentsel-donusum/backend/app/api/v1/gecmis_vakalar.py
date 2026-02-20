from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.gecmis_vaka import GecmisVaka
from app.services.benzerlik_service import BenzerlikService

router = APIRouter(prefix='/api/v1/vakalar', tags=['vakalar'])

class VakaGiris(BaseModel):
    parsel_alan_m2: float
    mevcut_insa_alan_m2: float
    kaks: float
    taks: float
    bagimsiz_bolum_sayisi: int
    donusum_yili: int
    gerceklesen_maliyet_tl: Optional[float] = None
    gercek_kat_karsiligi_orani: Optional[float] = None
    notlar: Optional[str] = None

class BenzerlikIstek(BaseModel):
    parsel_alan_m2: float
    mevcut_insa_alan_m2: float
    kaks: float
    taks: float
    bagimsiz_bolum_sayisi: int

@router.post("/")
def iceri_aktar(vaka: VakaGiris, db: Session = Depends(get_db)):
    """Geçmiş dönüşüm vakasını (gerçekleşen maliyet ve oranlarla) ML veri setine ekler."""
    yeni_vaka = GecmisVaka(
        parsel_alan_m2=vaka.parsel_alan_m2,
        mevcut_insa_alan_m2=vaka.mevcut_insa_alan_m2,
        kaks=vaka.kaks,
        taks=vaka.taks,
        bagimsiz_bolum_sayisi=vaka.bagimsiz_bolum_sayisi,
        donusum_yili=vaka.donusum_yili,
        gerceklesen_maliyet_tl=vaka.gerceklesen_maliyet_tl,
        gercek_kat_karsiligi_orani=vaka.gercek_kat_karsiligi_orani,
        notlar=vaka.notlar,
        is_aktif=True
    )
    db.add(yeni_vaka)
    db.commit()
    return {"status": "success", "message": "Vaka sisteme işlendi"}

@router.post("/benzerler")
def benzer_bul(istek: BenzerlikIstek, db: Session = Depends(get_db)):
    """Verilen parsele en çok benzeyen geçmiş vakaları Makine Öğrenmesi (K-NN) ile döndürür."""
    service = BenzerlikService(db)
    sonuclar = service.benzer_sorgula(
        hedef_parsel_m2=istek.parsel_alan_m2,
        mevcut_yapi_m2=istek.mevcut_insa_alan_m2,
        kaks=istek.kaks,
        taks=istek.taks,
        bagimsiz_bolum=istek.bagimsiz_bolum_sayisi,
        top_n=3
    )
    return sonuclar
