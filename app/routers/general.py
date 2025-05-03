from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.usuario import Usuario
from app.models.mensaje import Mensaje
from app.models.entrada_diaria import EntradaDiaria
from app.models.frente import Frente

from app.schemas.mensaje import MensajeOut
from app.schemas.entrada_diaria import EntradaDiariaOut
from app.schemas.frente import FrenteOut

router = APIRouter()

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/datos_iniciales/{usuario_id}")
def datos_iniciales(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    mensajes = (
        db.query(Mensaje)
        .filter_by(usuario_id=usuario_id)
        .order_by(Mensaje.momento.desc())
        .limit(10)
        .all()
    )

    entradas = (
        db.query(EntradaDiaria)
        .filter_by(usuario_id=usuario_id)
        .order_by(EntradaDiaria.fecha.desc())
        .all()
    )

    frentes = (
        db.query(Frente)
        .filter_by(usuario_id=usuario_id)
        .order_by(Frente.creado_en.desc())
        .all()
    )

    return {
        "mensajes": [MensajeOut(
            id=m.id,
            texto=m.texto,
            origen=m.origen,
            momento=m.momento
        ) for m in mensajes],

        "diario": [EntradaDiariaOut(
            id=e.id,
            date=e.fecha,
            title=e.titulo,
            description=e.reflexiones,
            mood=[int(i) for i in e.emojis.split(",")] if e.emojis else []
        ) for e in entradas],

        "frentes": [FrenteOut(
            id=f.id,
            nombre=f.titulo,
            color="gray",  # o f.color si usas uno real
            creado_en=f.creado_en
        ) for f in frentes],

        "terapias": []  # Placeholder
    }
