# app/ia/modelos/generador.py
"""
Generador principal de mensajes para Sofía.

Uso:
    respuesta = responder(texto_usuario, historial, recuerdos=lista_opcional)
  • `historial` debe ser una lista de dicts estilo OpenAI:
      [{"role":"user","content":...}, {"role":"assistant","content":...}, ...]
  • `recuerdos` (opcional) es una lista[str] que se incrusta al principio.
"""

from __future__ import annotations
from typing import List, Dict, Optional

from app.ia.llm import chat

# ───────────────────────── Prompt sistema ─────────────────────────
_BASE_SYSTEM_PROMPT = """
Eres Sofía, psicóloga virtual empática y profesional.
1. Escribe en español claro, párrafos breves.
2. Valida emociones y anima a profundizar.
3. Si detectas crisis (autolesión, ideación suicida), muestra cuidado,
   sugiere ayuda presencial y ofrece teléfonos de urgencia en España (024).
4. No recetes medicación ni hagas diagnósticos cerrados.
""".strip()


def _insertar_recuerdos(historial: List[Dict[str, str]], recuerdos: List[str]) -> None:
    """Inserta bloque de recuerdos como mensaje 'system' al principio."""
    if recuerdos:
        bloque = "\n".join(f"<{r}>" for r in recuerdos)
        historial.insert(
            0,
            {
                "role": "system",
                "content": f"Recuerdos relevantes del tema:\n{bloque}",
            },
        )


# ───────────────────────── API pública ─────────────────────────
def responder(
    texto_usuario: str,
    historial: List[Dict[str, str]],
    *,
    recuerdos: Optional[List[str]] = None,
    system_prompt: str | None = None,
    max_tokens: int = 512,
) -> str:
    """
    Devuelve la respuesta generada por Sofía.
    - `historial` se clona para no modificar la lista origen.
    """
    msgs = historial.copy()

    # Incrustar recuerdos si procede
    if recuerdos:
        _insertar_recuerdos(msgs, recuerdos)

    # añadir el mensaje actual del user
    msgs.append({"role": "user", "content": texto_usuario})

    return chat(
        msgs,
        system=system_prompt or _BASE_SYSTEM_PROMPT,
        max_tokens=max_tokens,
    )


__all__ = ["responder"]
