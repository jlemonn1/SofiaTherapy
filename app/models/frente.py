from sqlalchemy import BigInteger, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Frente(Base):
    __tablename__ = "frente"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(BigInteger, ForeignKey("usuario.id"), nullable=False)

    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, default="")
    creado_en = Column(DateTime, default=datetime.utcnow)
    contador_mensajes = Column(Integer, nullable=False, default=0)

    usuario = relationship("Usuario", back_populates="frentes", foreign_keys=[usuario_id])
    recuerdos = relationship("Recuerdo", back_populates="frente", cascade="all, delete-orphan")
