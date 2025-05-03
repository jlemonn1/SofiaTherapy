from sqlalchemy import BigInteger, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class EntradaDiaria(Base):
    __tablename__ = "entrada_diaria"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(BigInteger, ForeignKey("usuario.id"), nullable=False)

    fecha = Column(DateTime, default=datetime.utcnow)
    titulo = Column(String(255), nullable=False)
    reflexiones = Column(Text, nullable=False)
    emociones = Column(String(255))  # CSV o JSON textual generado por IA
    eventos = Column(String(500))   # Generado por IA
    emojis = Column(String(10))     # Guardar como "😊,😔"

    usuario = relationship("Usuario", back_populates="entradas_diarias")
