# app/back_local.py
"""
Back-end mínimo con todas las funciones que usará el motor de IA.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.models import (
    Usuario,
    Frente,
    Mensaje,
    Recuerdo,
    EntradaDiaria,
    TipoRecuerdo,
)
from app.ia.estado import EstadoConversacional


# ───────────────────────────── Decorador ──────────────────────────────
def usar_sesion(func):
    def wrapper(*args, **kwargs):
        db: Session = SessionLocal()
        try:
            return func(db, *args, **kwargs)
        finally:
            db.close()

    return wrapper


# ──────────────────────────── Mensajes ────────────────────────────────
@usar_sesion
def guardar_mensaje(
    db: Session,
    usuario_id: int,
    texto: str,
    origen: str,
    frente_id: int | None = None,
):
    mensaje = Mensaje(
        usuario_id=usuario_id,
        frente_id=frente_id,
        texto=texto,
        origen=origen,
        momento=datetime.utcnow(),
    )
    db.add(mensaje)

    if frente_id:
        frente: Frente = db.get(Frente, frente_id)
        frente.contador_mensajes += 1

        if frente.contador_mensajes % 10 == 0:
            db.add(
                Recuerdo(
                    frente_id=frente_id,
                    tipo=TipoRecuerdo.AVANCE,
                    contenido=f"⏱️ Mensaje #{frente.contador_mensajes}: {texto[:180]}",
                )
            )

    db.commit()
    return mensaje


@usar_sesion
def obtener_ultimos_mensajes(db: Session, usuario_id: int, limite: int = 20):
    return (
        db.query(Mensaje)
        .filter_by(usuario_id=usuario_id)
        .order_by(Mensaje.momento.desc())
        .limit(limite)
        .all()
    )


# ──────────────────────────── Frentes ─────────────────────────────────
@usar_sesion
def crear_frente(db: Session, usuario_id: int, titulo: str, descripcion: str = ""):
    frente = Frente(
        usuario_id=usuario_id,
        titulo=titulo,
        descripcion=descripcion,
    )
    db.add(frente)
    db.commit()
    db.refresh(frente)
    return frente.id


@usar_sesion
def obtener_frentes(db: Session, usuario_id: int):
    return db.query(Frente).filter_by(usuario_id=usuario_id).all()


@usar_sesion
def recordar_frente(db: Session, frente_id: int, limite: int = 5):
    return [
        r.contenido
        for r in (
            db.query(Recuerdo)
            .filter_by(frente_id=frente_id)
            .order_by(Recuerdo.fecha.desc())
            .limit(limite)
            .all()
        )
    ]


# ─────────────────────────── Recuerdos ────────────────────────────────
@usar_sesion
def añadir_recuerdo(db: Session, frente_id: int, tipo: str, contenido: str):
    r = Recuerdo(frente_id=frente_id, tipo=TipoRecuerdo(tipo), contenido=contenido)
    db.add(r)
    db.commit()
    return r.id


# ──────────────────────────── Diario ──────────────────────────────────
@usar_sesion
def ver_todas_entradas(db: Session, usuario_id: int):
    return (
        db.query(EntradaDiaria)
        .filter_by(usuario_id=usuario_id)
        .order_by(EntradaDiaria.fecha.desc())
        .all()
    )


@usar_sesion
def ver_entradas_semana(db: Session, usuario_id: int):
    desde = datetime.utcnow() - timedelta(days=7)
    return (
        db.query(EntradaDiaria)
        .filter(
            EntradaDiaria.usuario_id == usuario_id,
            EntradaDiaria.fecha >= desde,
        )
        .order_by(EntradaDiaria.fecha.desc())
        .all()
    )


# ─────────────────────── Estado conversacional ───────────────────────
def get_estado_usuario(usuario_id: int) -> EstadoConversacional:
    db: Session = SessionLocal()
    try:
        u = db.get(Usuario, usuario_id)
        return (
            EstadoConversacional(u.estado_conversacional)
            if u and u.estado_conversacional
            else EstadoConversacional.GENERAL
        )
    finally:
        db.close()


def set_estado_usuario(usuario_id: int, estado: EstadoConversacional):
    db: Session = SessionLocal()
    try:
        if (u := db.get(Usuario, usuario_id)):
            u.estado_conversacional = estado.value
            db.commit()
    finally:
        db.close()


def reset_estado_usuario(usuario_id: int):
    set_estado_usuario(usuario_id, EstadoConversacional.GENERAL)


# ───────────────────────── Frente actual ──────────────────────────────
@usar_sesion
def set_frente_actual(db: Session, usuario_id: int, frente_id: int | None):
    u = db.get(Usuario, usuario_id)
    u.frente_actual_id = frente_id
    db.commit()


@usar_sesion
def get_frente_actual(db, usuario_id: int):
    """Devuelve el id del frente activo o None."""
    u = db.get(Usuario, usuario_id)
    return u.frente_actual_id if u else None


@usar_sesion
def usuario_existe(db, usuario_id: int) -> bool:
    return db.query(Usuario).filter_by(id=usuario_id).first() is not None

@usar_sesion
def crear_usuario(db, usuario_id: int):
    u = Usuario(id=usuario_id, id_telegram=str(usuario_id))
    db.add(u)
    db.commit()
