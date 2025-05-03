from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base, engine
from app.routers import (
    usuarios,
    general,
    diario,
    mensajes,
    frentes,
    recuerdos,
    ia,
)

# Crea todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sofía Therapy API")

# CORS para permitir peticiones desde el frontend (React Native)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar todos los routers
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(general.router, tags=["General"])
app.include_router(diario.router, tags=["Diario"])
app.include_router(mensajes.router, tags=["Mensajes"])
app.include_router(frentes.router, tags=["Frentes"])
app.include_router(recuerdos.router, tags=["Recuerdos"])
app.include_router(ia.router, tags=["IA"])



