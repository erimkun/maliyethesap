from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.database import get_db
from app.models.imar import ImarVerisi
from app.models.tarife import BelediyeTarife
from app.models.parcels import Parcel

router = APIRouter(prefix='/api/v1/admin', tags=['admin'])

# Pydantic Girdi Modelleri
class ImarGiris(BaseModel):
    ada_no: str
    parsel_no: str
    taks: float
    kaks: float
    bagimsiz_bolum_sayisi: int
    yapi_nizam: str
    yapi_sinifi: str
    imar_notlari: Optional[str] = None
    belediye_kodu: str = "uskudar"

class TarifeGiris(BaseModel):
    yil: int
    ruhsat_harci_tl_m2: float
    altyapi_payi_tl_m2: float
    otopark_bedeli_tl: float
    belediye_kodu: str = "uskudar"

@router.post("/imar")
def kaydet_imar_verisi(veri: ImarGiris, db: Session = Depends(get_db)):
    """Belediyenin belirli bir parsele ait imar bilgisini kaydeder."""
    
    # Gerçek uygulamada önce parsel tablosunda var mı diye bakılır
    # Yoksa dummy olarak ekliyor gibi farz ediyoruz
    parsel = db.query(Parcel).filter_by(ada_no=veri.ada_no, parsel_no=veri.parsel_no).first()
    
    yeni_imar = ImarVerisi(
        parsel_id=parsel.id if parsel else None,
        taks=veri.taks,
        kaks=veri.kaks,
        bagimsiz_bolum_sayisi=veri.bagimsiz_bolum_sayisi,
        yapi_nizam=veri.yapi_nizam,
        yapi_sinifi=veri.yapi_sinifi,
        imar_notlari=veri.imar_notlari,
        belediye_kodu=veri.belediye_kodu,
        guncelleme_tarihi=date.today(),
        mevcut_yapi_alan_m2=0 # dummy
    )
    db.add(yeni_imar)
    db.commit()
    return {"status": "success", "message": "İmar bilgisi başarıyla eklendi."}

@router.put("/tarife")
def guncelle_tarife(tarife: TarifeGiris, db: Session = Depends(get_db)):
    """Belediye tarifelerini yıl bazlı günceller (Upsert)."""
    
    mevcut = db.query(BelediyeTarife).filter_by(
        belediye_kodu=tarife.belediye_kodu, 
        yil=tarife.yil
    ).first()
    
    if mevcut:
        mevcut.ruhsat_harci_tl_m2 = tarife.ruhsat_harci_tl_m2
        mevcut.altyapi_payi_tl_m2 = tarife.altyapi_payi_tl_m2
        mevcut.otopark_bedeli_tl = tarife.otopark_bedeli_tl
        mevcut.guncelleme_tarihi = date.today()
    else:
        yeni_tarife = BelediyeTarife(
            belediye_kodu=tarife.belediye_kodu,
            yil=tarife.yil,
            ruhsat_harci_tl_m2=tarife.ruhsat_harci_tl_m2,
            altyapi_payi_tl_m2=tarife.altyapi_payi_tl_m2,
            otopark_bedeli_tl=tarife.otopark_bedeli_tl,
            guncelleme_tarihi=date.today()
        )
        db.add(yeni_tarife)
        
    db.commit()
    return {"status": "success", "message": "Tarife güncellendi."}

@router.get("/istatistik")
def get_istatistik(db: Session = Depends(get_db)):
    """Sorgulama istatistiklerini getirir (Mock veriler)."""
    # Gerçek uygulamada logs tablosundan select çekilir.
    return {
        "son_7_gun_sorgu_sayisi": 154,
        "en_cok_sorgulanan_mahalleler": [
            {"mahalle": "Mimar Sinan", "adet": 42},
            {"mahalle": "Bulgurlu", "adet": 38},
            {"mahalle": "Ahmediye", "adet": 25},
            {"mahalle": "Acıbadem", "adet": 19},
            {"mahalle": "Muratreis", "adet": 12},
        ]
    }
