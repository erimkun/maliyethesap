import uuid
from sqlalchemy import Column, String, Numeric, Integer, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class ImarVerisi(Base):
    __tablename__ = 'imar_verileri'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parsel_id = Column(UUID(as_uuid=True), ForeignKey('parcels.id'))
    taks = Column(Numeric)
    kaks = Column(Numeric)
    max_yukseklik_m = Column(Numeric, nullable=True)
    yapi_nizam = Column(String) # 'ayrik', 'bitisik', 'blok'
    bagimsiz_bolum_sayisi = Column(Integer)
    mevcut_yapi_alan_m2 = Column(Numeric)
    yapi_sinifi = Column(String) # 'lüks', 'normal', 'sosyal'
    imar_notlari = Column(Text, nullable=True)
    belediye_kodu = Column(String)
    guncelleme_tarihi = Column(Date)
    
    parsel = relationship("Parcel")
