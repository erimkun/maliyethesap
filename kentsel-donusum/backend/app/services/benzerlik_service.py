import logging
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances
from app.models.gecmis_vaka import GecmisVaka

logger = logging.getLogger(__name__)

class BenzerlikService:
    def __init__(self, db: Session):
        self.db = db

    def benzer_sorgula(self, hedef_parsel_m2: float, mevcut_yapi_m2: float, kaks: float, taks: float, bagimsiz_bolum: int, top_n: int = 3):
        """
        Geçmiş vakaları çeker, normalize eder (MinMaxScaler) ve
        Öklid uzaklığına göre en yakın projeleri döndürür.
        """
        vakalar = self.db.query(GecmisVaka).filter(GecmisVaka.is_aktif == True).all()
        
        if not vakalar:
            return []
            
        # DataFrame Olusturma
        data = []
        for v in vakalar:
            data.append({
                "id": v.id,
                "parsel_alan_m2": float(v.parsel_alan_m2),
                "mevcut_insa_alan_m2": float(v.mevcut_insa_alan_m2),
                "kaks": float(v.kaks) if v.kaks else 0.0,
                "taks": float(v.taks) if v.taks else 0.0,
                "bagimsiz_bolum_sayisi": v.bagimsiz_bolum_sayisi,
                "gerceklesen_maliyet_tl": float(v.gerceklesen_maliyet_tl) if v.gerceklesen_maliyet_tl else 0.0,
                "gercek_kat_karsiligi_orani": float(v.gercek_kat_karsiligi_orani) if v.gercek_kat_karsiligi_orani else 0.0,
                "donusum_yili": v.donusum_yili
            })
            
        df = pd.DataFrame(data)
        
        # Hedef ozellikler
        hedef_vektor = pd.DataFrame([{
            "parsel_alan_m2": hedef_parsel_m2,
            "mevcut_insa_alan_m2": mevcut_yapi_m2,
            "kaks": kaks,
            "taks": taks,
            "bagimsiz_bolum_sayisi": bagimsiz_bolum
        }])
        
        # Sadece ML icin kullanilacak feature'lar
        features = ["parsel_alan_m2", "mevcut_insa_alan_m2", "kaks", "taks", "bagimsiz_bolum_sayisi"]
        
        # Scaler
        scaler = MinMaxScaler()
        X_all = pd.concat([df[features], hedef_vektor[features]], ignore_index=True)
        X_scaled = scaler.fit_transform(X_all)
        
        # Hedef vektor en altta
        hedef_scaled = X_scaled[-1:]
        vakalar_scaled = X_scaled[:-1]
        
        # Oklid mesafesi olcumu
        distances = euclidean_distances(hedef_scaled, vakalar_scaled)[0]
        
        df['distance'] = distances
        df_sorted = df.sort_values('distance')
        
        # En yakin top_n
        top_matches = df_sorted.head(top_n)
        
        sonuclar = []
        for _, row in top_matches.iterrows():
            sonuclar.append({
                "vaka_id": row['id'],
                "benzerlik_skoru": 1.0 / (1.0 + float(row['distance'])), # Uzaklık 0 ise skor 1
                "gercek_maliyet_tl": row['gerceklesen_maliyet_tl'],
                "yil": row['donusum_yili'],
                "kat_karsiligi_oran": row['gercek_kat_karsiligi_orani'],
                "parsel_alan_m2": row['parsel_alan_m2']
            })
            
        return sonuclar
