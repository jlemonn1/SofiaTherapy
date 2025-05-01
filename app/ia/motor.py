# app/ia/motor.py
"""
MotorConversacion – orquesta el flujo de diálogo según el diagrama de estados.

Punto de entrada:
    respuesta = procesar(usuario_id: int, texto_usuario: str) -> str
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from app.ia.estado import EstadoConversacional as EC
from app.ia.modelos import (
    clasificador,
    confirmador,
    desviometro,
    generador,
    nuevo_frente,
)
from app import back_local as bl


# ───────────────────────── Helpers internos ─────────────────────────
def _obtener_titulos_frentes(uid: int) -> List[str]:
    return [f.titulo for f in bl.obtener_frentes(uid)]


def _detectar_frente_por_titulo(uid: int, titulo: str) -> Optional[int]:
    for f in bl.obtener_frentes(uid):
        if f.titulo.lower() == titulo.lower():
            return f.id
    return None


def _mensajes_historial(uid: int, frente_id: int | None = None) -> List[dict]:
    msgs = bl.obtener_ultimos_mensajes(uid, limite=15)
    if frente_id:
        msgs = [m for m in msgs if m.frente_id == frente_id]
    return [
        {"role": "user" if m.origen == "usuario" else "assistant", "content": m.texto}
        for m in msgs
    ]


def _texto_completo_historial(uid: int) -> str:
    """Concatena los últimos mensajes del usuario como contexto para nombrar frentes."""
    mensajes = bl.obtener_ultimos_mensajes(uid, limite=10)
    return "\n".join(m.texto for m in mensajes if m.origen == "usuario")


# ───────────────────────── Estado GENERAL ─────────────────────────
def _manejar_general(uid: int, texto: str) -> Tuple[str, EC]:
    etiqueta, frente_titulo = clasificador.detect(texto, _obtener_titulos_frentes(uid))

    if etiqueta == "hablar_frente" and frente_titulo:
        return (
            f"¿Quieres retomar el frente «{frente_titulo}» ahora?",
            EC.CONFIRM_RETOMAR,
        )

    if etiqueta == "nuevo_frente":
        return "¿Abrimos un frente nuevo para este tema?", EC.CONFIRM_NUEVO

    historial = _mensajes_historial(uid)
    respuesta = generador.responder(texto, historial)
    return respuesta, EC.GENERAL


# ──────────────────────── Estado CONFIRM_* ────────────────────────
def _manejar_confirm(uid: int, texto: str, tipo: EC) -> Tuple[str, EC]:
    afirmativo = confirmador.es_si(texto)

    if not afirmativo:
        return "Entendido, seguimos con lo que comentabas 😊", EC.GENERAL

    if tipo == EC.CONFIRM_NUEVO:
        contexto = _texto_completo_historial(uid)
        resumen = nuevo_frente.generar_titulo_descripcion(contexto)
        titulo = resumen.get("titulo", "Nuevo frente")[:60]
        descripcion = resumen.get("descripcion", "")[:500]
        frente_id = bl.crear_frente(uid, titulo=titulo, descripcion=descripcion)
        bl.set_frente_actual(uid, frente_id)
        return "¡Perfecto! Cuéntame más…", EC.EN_FRENTE

    if tipo == EC.CONFIRM_RETOMAR:
        frente_id = _detectar_frente_por_titulo(uid, texto)
        if not frente_id:
            return "No estoy segura de a qué tema te refieres 🙈", EC.GENERAL
        bl.set_frente_actual(uid, frente_id)
        recuerdos = bl.recordar_frente(frente_id)
        recap = "\n".join(f"- {r}" for r in recuerdos) or "Retomemos donde lo dejamos."
        return f"{recap}\n\n¿En qué punto seguimos?", EC.EN_FRENTE

    return "Vale, seguimos charlando.", EC.GENERAL


# ───────────────────────── Estado EN_FRENTE ────────────────────────
def _manejar_en_frente(uid: int, texto: str) -> Tuple[str, EC]:
    frente_id = bl.get_frente_actual(uid)
    if not frente_id:
        return "Ups, parece que no hay un tema activo. ¿De qué hablamos?", EC.GENERAL

    if texto.lower().startswith("dejemos este tema"):
        bl.set_frente_actual(uid, None)
        return "Claro, cambiamos de tema 😊", EC.GENERAL

    contexto = " | ".join(bl.recordar_frente(frente_id, limite=3))
    if desviometro.es_desvio(texto, contexto=contexto):
        bl.set_frente_actual(uid, None)
        return "Entiendo, dejamos eso aparte. ¿Sobre qué más te gustaría hablar?", EC.GENERAL

    historial = _mensajes_historial(uid, frente_id=frente_id)
    n_msgs = next(f for f in bl.obtener_frentes(uid) if f.id == frente_id).contador_mensajes
    recuerdos: Optional[List[str]] = bl.recordar_frente(frente_id) if n_msgs % 10 == 0 else None
    respuesta = generador.responder(texto, historial, recuerdos=recuerdos)
    return respuesta, EC.EN_FRENTE


# ───────────────────────── API pública ─────────────────────────
def procesar(usuario_id: int, texto_usuario: str) -> str:
    print("Nuevo mensjae")
    usuario_id = usuario_id or 1

    if not bl.usuario_existe(usuario_id):
        bl.crear_usuario(usuario_id)

    estado = bl.get_estado_usuario(usuario_id)
    bl.guardar_mensaje(usuario_id, texto_usuario, "usuario", frente_id=bl.get_frente_actual(usuario_id))

    if estado == EC.GENERAL:
        respuesta, nuevo = _manejar_general(usuario_id, texto_usuario)

    elif estado in {EC.CONFIRM_NUEVO, EC.CONFIRM_RETOMAR}:
        respuesta, nuevo = _manejar_confirm(usuario_id, texto_usuario, estado)

    else:
        respuesta, nuevo = _manejar_en_frente(usuario_id, texto_usuario)

    bl.guardar_mensaje(
        usuario_id,
        respuesta,
        "sofia",
        frente_id=bl.get_frente_actual(usuario_id) if nuevo == EC.EN_FRENTE else None,
    )
    bl.set_estado_usuario(usuario_id, nuevo)
    return respuesta
