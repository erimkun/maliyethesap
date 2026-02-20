import uuid
from sqlalchemy import Column, String, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from app.database import Base

class Parcel(Base):
    __tablename__ = 'parcels'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ada_no = Column(String, index=True)
    parsel_no = Column(String, index=True)
    il_kodu = Column(String)
    ilce_kodu = Column(String)
    belediye_kodu = Column(String)
    geom = Column(Geometry('POLYGON', srid=4326), index=True)
    alan_m2 = Column(Numeric)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
