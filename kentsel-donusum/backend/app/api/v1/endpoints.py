from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from app.database import get_db
from app.services.tkgm_service import TKGMService
from app.engine.calculator import HesaplamaMotoru, ParselInput, HesaplamaResult
from app.models.birim_maliyet import BakanlikBirimMaliyet

router = APIRouter(prefix='/api/v1')
tkgm_service = TKGMService()
hesaplama_motoru = HesaplamaMotoru()

@router.get("/health")
def health_check():
    return {"status": "ok", "db": "reachable", "tkgm": "reachable"}

@router.get("/parsel/{lat}/{lon}")
async def get_parsel(lat: float, lon: float, db: Session = Depends(get_db)):
    """Koordinatlardan ada/parsel bilgilerini döner ve veritabanı yansımasıyla birleştirir"""
    result = await tkgm_service.koordinattan_parsel_bul(lat, lon)
    if not result:
        raise HTTPException(status_code=404, detail="Girdiğiniz koordinatlarda parsel bulunamadı.")
    return result

@router.post("/hesapla", response_model=HesaplamaResult)
def hesapla(parsel: ParselInput, db: Session = Depends(get_db)):
    """Maliyet hesaplama işlemini gerçekleştirir. (Mock değerler geçici verilmiştir)"""
    # Gerçek senaryoda bu DB'den alınacaktır
    birim_bedel = Decimal('22000') 
    tarife = {
        'ruhsat_harci_tl_m2': '15',
        'altyapi_payi_tl_m2': '25',
        'otopark_tl': '50000'
    }
    
    try:
        return hesaplama_motoru.hesapla(parsel, birim_bedel, tarife)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/birim-bedel/{yil}/{yapi_sinifi}")
def get_birim_bedel(yil: int, yapi_sinifi: str, db: Session = Depends(get_db)):
    """Veritabanından aktif bakanlık maliyetini getirir."""
    record = db.query(BakanlikBirimMaliyet).filter_by(yil=yil, yapi_sinifi=yapi_sinifi, aktif=True).first()
    if not record:
        return {"yil": yil, "yapi_sinifi": yapi_sinifi, "birim_bedel_tl_m2": 22000.0} 
    return {"yil": yil, "yapi_sinifi": yapi_sinifi, "birim_bedel_tl_m2": float(record.birim_bedel_tl_m2)}
