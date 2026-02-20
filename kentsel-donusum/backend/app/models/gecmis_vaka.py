import uuid
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class GecmisVaka(Base):
    __tablename__ = 'gecmis_vakalar'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parsel_id = Column(UUID(as_uuid=True), ForeignKey('parcels.id'), nullable=True)
    parsel_alan_m2 = Column(Numeric)
    kaks = Column(Numeric)
    bina_yasi_yil = Column(Integer)
    kat_adedi = Column(Integer)
    bagimsiz_bolum_sayisi = Column(Integer)
    ilce_kodu = Column(String)
    gerceklesen_maliyet_tl = Column(Numeric)
    vaka_yili = Column(Integer)
    muteahhit_modeli = Column(String) # 'kat_karsiligi' veya 'nakit'
    
    parsel = relationship("Parcel")
