from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.entrada_diaria import EntradaDiaria
from app.models.usuario import Usuario
from app.schemas.entrada_diaria import EntradaDiariaCreate, EntradaDiariaOut

router = APIRouter()

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/diario", response_model=EntradaDiariaOut)
def crear_entrada(entry: EntradaDiariaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(id=entry.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    entrada = EntradaDiaria(
        usuario_id=entry.usuario_id,
        fecha=entry.fecha,
        titulo=entry.titulo,
        reflexiones = entry.descripcion,
        emojis=",".join(str(e) for e in entry.emojis),
        emociones="",  # Se rellenarán más tarde por la IA
        eventos="",    # Se rellenarán más tarde por la IA
    )
    db.add(entrada)
    db.commit()
    db.refresh(entrada)

    return EntradaDiariaOut(
        id=entrada.id,
        date=entrada.fecha,
        title=entrada.titulo,
        description=entrada.reflexiones,
        mood=entry.emojis
    )

@router.get("/diario/{usuario_id}", response_model=list[EntradaDiariaOut])
def obtener_entradas(usuario_id: int, db: Session = Depends(get_db)):
    entradas = (
        db.query(EntradaDiaria)
        .filter_by(usuario_id=usuario_id)
        .order_by(EntradaDiaria.fecha.desc())
        .all()
    )

    return [
        EntradaDiariaOut(
            id=e.id,
            date=e.fecha,
            title=e.titulo,
            description=e.reflexiones,
            mood=[int(i) for i in e.emojis.split(",")] if e.emojis else []
        )
        for e in entradas
    ]
