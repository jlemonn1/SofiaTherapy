# app/models/usuario.py
from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True, index=True) 
    #id            = Column(Integer, primary_key=True, index=True)
    id_telegram   = Column(String(50), unique=True, index=True, nullable=False)
    nombre        = Column(String(100))

    estado_conversacional = Column(
        String(50), nullable=False, default="CONVERSACION_GENERAL"
    )

    frente_actual_id = Column(Integer, ForeignKey("frente.id", ondelete="SET NULL"))
    frente_actual = relationship(
        "Frente",
        back_populates="usuarios_activos",
        foreign_keys=[frente_actual_id],
        uselist=False,
    )

    # relaciones “uno-a-muchos”
    frentes          = relationship(
        "Frente",
        back_populates="usuario",
        cascade="all, delete-orphan",
        foreign_keys="Frente.usuario_id",
    )
    entradas_diarias = relationship(
        "EntradaDiaria",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
    mensajes         = relationship(
        "Mensaje",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
