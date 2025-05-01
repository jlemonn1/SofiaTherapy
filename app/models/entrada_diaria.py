# app/models/entrada_diaria.py
from sqlalchemy import BigInteger, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class EntradaDiaria(Base):
    __tablename__ = "entrada_diaria"

    id         = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(BigInteger, ForeignKey("usuario.id"), nullable=False) 

    fecha        = Column(DateTime, default=datetime.utcnow)
    emociones    = Column(String(255))   # csv o JSON textual
    eventos      = Column(String(500))
    reflexiones  = Column(Text)

    usuario = relationship("Usuario", back_populates="entradas_diarias")
