from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    about = Column(String(500), nullable=True)
    ai_mode = Column(String(50), default="0.5")
    estado_conversacional = Column(String(50), nullable=False, default="CONVERSACION_GENERAL")

    frente_actual_id = Column(Integer, ForeignKey("frente.id", ondelete="SET NULL"))

    frentes = relationship("Frente", back_populates="usuario", foreign_keys="Frente.usuario_id")
    entradas_diarias = relationship("EntradaDiaria", back_populates="usuario")
    mensajes = relationship("Mensaje", back_populates="usuario")
    frente_actual = relationship("Frente", foreign_keys=[frente_actual_id])
