from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.frente import Frente
from app.models.usuario import Usuario
from app.schemas.frente import FrenteCreate, FrenteOut

router = APIRouter()

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/frentes", response_model=FrenteOut)
def crear_frente(data: FrenteCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(id=data.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    frente = Frente(
        usuario_id=data.usuario_id,
        titulo=data.titulo,
        descripcion=data.descripcion
    )
    db.add(frente)
    db.commit()
    db.refresh(frente)

    return FrenteOut(
        id=frente.id,
        nombre=frente.titulo,
        color="gray",  # puedes cambiar esto si tienes un campo real
        creado_en=frente.creado_en
    )

@router.get("/frentes/{usuario_id}", response_model=list[FrenteOut])
def obtener_frentes(usuario_id: int, db: Session = Depends(get_db)):
    frentes = (
        db.query(Frente)
        .filter_by(usuario_id=usuario_id)
        .order_by(Frente.creado_en.desc())
        .all()
    )

    return [
        FrenteOut(
            id=f.id,
            nombre=f.titulo,
            color="gray",  # igual que arriba
            creado_en=f.creado_en
        ) for f in frentes
    ]
