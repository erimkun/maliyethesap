import uuid
from sqlalchemy import Column, String, Numeric, Integer, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class BelediyeTarife(Base):
    __tablename__ = 'belediye_tarifeler'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    belediye_kodu = Column(String)
    yil = Column(Integer)
    ruhsat_harci_tl_m2 = Column(Numeric)
    altyapi_payi_tl_m2 = Column(Numeric)
    otopark_bedeli_tl = Column(Numeric)
    guncelleme_tarihi = Column(Date)

    __table_args__ = (
        UniqueConstraint('belediye_kodu', 'yil', name='uix_belediye_yil'),
    )
