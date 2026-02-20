import uuid
from sqlalchemy import Column, String, Numeric, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class BakanlikBirimMaliyet(Base):
    __tablename__ = 'bakanlik_birim_maliyetler'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    yil = Column(Integer)
    yapi_sinifi = Column(String)
    birim_bedel_tl_m2 = Column(Numeric) # Float yasak!
    aktif = Column(Boolean, default=True)
