from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.mensaje import Mensaje
from app.models.usuario import Usuario
from datetime import datetime
import random

router = APIRouter()

# Frases y fragmentos base para construir respuestas tipo Sofía
inicios = [
    "Sabes, estuve pensando en eso...",
    "Me ha venido algo curioso a la mente.",
    "No es casualidad que menciones eso.",
    "A veces, la vida tiene formas raras de mostrarnos cosas.",
    "Me encanta que lo menciones porque..."
]

cuerpos = [
    "cuando estamos en un momento de cambio, suelen aparecer dudas, pero también oportunidades. ",
    "muchas veces las emociones no son buenas ni malas, simplemente son señales que nos invitan a escuchar. ",
    "las pequeñas decisiones cotidianas construyen realidades más grandes de lo que imaginamos. ",
    "hay algo de mágico en parar un momento y observar lo que sentimos sin juzgarlo. ",
    "puede que lo que hoy parece confusión, mañana se entienda como un paso necesario. "
]

cierres = [
    "Quizá no tengas todas las respuestas hoy, pero estás avanzando.",
    "Lo importante es que sigas en movimiento, aunque sea lento.",
    "Sigue preguntándote cosas, ahí está la clave.",
    "Y eso, en sí mismo, ya es crecimiento.",
    "No subestimes lo que sientes, ahí hay pistas valiosas."
]

def generar_respuesta_sofia():
    respuesta = random.choice(inicios) + " "
    respuesta += random.choice(cuerpos) * random.randint(1, 3)
    respuesta += random.choice(cierres)

    if len(respuesta) < 70:
        return generar_respuesta_sofia()
    return respuesta[:400]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ia/mensaje")
def responder_a_usuario(usuario_id: int, texto: str, db: Session = Depends(get_db)):
    """
    Guarda el mensaje del usuario y genera una respuesta tipo Sofía.
    """
    # Verifica que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Guarda el mensaje del usuario
    mensaje_usuario = Mensaje(
        usuario_id=usuario_id,
        texto=texto,
        origen="usuario",
        momento=datetime.utcnow()
    )
    db.add(mensaje_usuario)

    # Genera y guarda respuesta de Sofía
    respuesta = generar_respuesta_sofia()
    mensaje_sofia = Mensaje(
        usuario_id=usuario_id,
        texto=respuesta,
        origen="sofia",
        momento=datetime.utcnow()
    )
    db.add(mensaje_sofia)

    db.commit()

    return {"respuesta": respuesta}
