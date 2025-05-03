from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Mensaje(Base):
    __tablename__ = "mensaje"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey("usuario.id"), nullable=False)
    frente_id = Column(Integer, ForeignKey("frente.id"), nullable=True)

    texto = Column(Text, nullable=False)
    origen = Column(String(10), nullable=False)  # 'usuario' | 'sofia'
    momento = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="mensajes", foreign_keys=[usuario_id])
