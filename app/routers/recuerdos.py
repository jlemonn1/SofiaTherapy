from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.recuerdo import Recuerdo
from app.models.frente import Frente
from app.schemas.recuerdo import RecuerdoCreate, RecuerdoOut

router = APIRouter()

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recuerdos", response_model=RecuerdoOut)
def crear_recuerdo(data: RecuerdoCreate, db: Session = Depends(get_db)):
    frente = db.query(Frente).filter_by(id=data.frente_id).first()
    if not frente:
        raise HTTPException(status_code=404, detail="Frente no encontrado")

    recuerdo = Recuerdo(
        frente_id=data.frente_id,
        tipo=data.tipo,
        contenido=data.contenido
    )
    db.add(recuerdo)
    db.commit()
    db.refresh(recuerdo)

    return RecuerdoOut(
        id=recuerdo.id,
        tipo=recuerdo.tipo,
        contenido=recuerdo.contenido,
        fecha=recuerdo.fecha
    )

@router.get("/recuerdos/{frente_id}", response_model=list[RecuerdoOut])
def obtener_todos(frente_id: int, db: Session = Depends(get_db)):
    recuerdos = (
        db.query(Recuerdo)
        .filter_by(frente_id=frente_id)
        .order_by(Recuerdo.fecha.asc())
        .all()
    )
    return [
        RecuerdoOut(
            id=r.id,
            tipo=r.tipo,
            contenido=r.contenido,
            fecha=r.fecha
        ) for r in recuerdos
    ]

@router.get("/recuerdos/ultimos/{frente_id}", response_model=list[RecuerdoOut])
def obtener_ultimos(frente_id: int, db: Session = Depends(get_db)):
    recuerdos = (
        db.query(Recuerdo)
        .filter_by(frente_id=frente_id)
        .order_by(Recuerdo.fecha.desc())
        .limit(40)
        .all()
    )
    return [
        RecuerdoOut(
            id=r.id,
            tipo=r.tipo,
            contenido=r.contenido,
            fecha=r.fecha
        ) for r in recuerdos
    ]
