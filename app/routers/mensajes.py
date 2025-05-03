from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.usuario import Usuario
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate, MensajeOut

router = APIRouter()

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/mensajes/{usuario_id}", response_model=list[MensajeOut])
def ultimos_mensajes(usuario_id: int, db: Session = Depends(get_db)):
    mensajes = (
        db.query(Mensaje)
        .filter_by(usuario_id=usuario_id)
        .order_by(Mensaje.momento.desc())
        .limit(10)
        .all()
    )
    return [
        MensajeOut(
            id=m.id,
            texto=m.texto,
            origen=m.origen,
            momento=m.momento
        )
        for m in mensajes
    ]

@router.get("/mensajes/todos/{usuario_id}", response_model=list[MensajeOut])
def todos_los_mensajes(usuario_id: int, db: Session = Depends(get_db)):
    mensajes = (
        db.query(Mensaje)
        .filter_by(usuario_id=usuario_id)
        .order_by(Mensaje.momento.asc())
        .all()
    )
    return [
        MensajeOut(
            id=m.id,
            texto=m.texto,
            origen=m.origen,
            momento=m.momento
        )
        for m in mensajes
    ]
