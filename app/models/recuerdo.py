# app/models/recuerdo.py
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.models.enums import TipoRecuerdo

class Recuerdo(Base):
    __tablename__ = "recuerdo"

    id        = Column(Integer, primary_key=True, index=True)
    frente_id = Column(Integer, ForeignKey("frente.id"), nullable=False)

    tipo      = Column(Enum(TipoRecuerdo), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha     = Column(DateTime, default=datetime.utcnow)

    frente = relationship("Frente", back_populates="recuerdos")
