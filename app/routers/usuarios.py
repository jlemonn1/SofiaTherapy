from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=UsuarioOut)
def login(data: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(email=data.email).first()
    if usuario:
        return usuario

    nuevo = Usuario(
        nombre=data.nombre,
        email=data.email,
        about="",
        ai_mode="default"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
