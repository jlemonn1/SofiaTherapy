# app/ia/modelos/clasificador.py
"""
Detecta la intención principal del usuario.

API:
    detect(texto: str, frentes: list[str]) -> tuple[str, str | None]
Devuelve:
    ("nuevo_frente" | "hablar_frente" | "conversacion", frente_sugerido_or_None)
"""

from __future__ import annotations

from typing import List, Tuple, Optional, Dict

from app.ia.llm import chat_json

# ──────────────────────────────────────────────────────────────────────────────
# Prompt
# ──────────────────────────────────────────────────────────────────────────────
_BASE_SYSTEM_PROMPT = """
Responde SOLO con JSON:
{{
  "intencion": "nuevo_frente" | "hablar_frente" | "conversacion",
  "frente": null | "<titulo>"
}}

Criterios:
- Si el mensaje menciona de forma directa (o muy obvia) un frente existente
  debe etiquetarse "hablar_frente" y devolver exactamente el título en "frente".
- Si el mensaje plantea un tema nuevo que no coincide con los frentes listados,
  responde "nuevo_frente" y deja "frente": null.
- En cualquier otro caso responde "conversacion" con "frente": null.
No añadas comentarios ni otros campos.
""".strip()


def _armar_prompt(frentes: List[str]) -> str:
    if not frentes:
        return _BASE_SYSTEM_PROMPT + "\n\n(No hay frentes creados todavía)"
    lista = "\n".join(f"- {t}" for t in frentes[:20])
    return (
        _BASE_SYSTEM_PROMPT
        + "\n\nLista de frentes del usuario (máx 20):\n"
        + lista
    )


# ──────────────────────────────────────────────────────────────────────────────
# API pública
# ──────────────────────────────────────────────────────────────────────────────
def detect(texto: str, frentes: List[str] | None = None) -> Tuple[str, Optional[str]]:
    """
    Retorna (intencion, frente_mencionado|None).

    • Si el LLM produce JSON inválido o un valor inesperado,
      hacemos fallback a ("conversacion", None).
    """
    system_prompt = _armar_prompt(frentes or [])
    data: Dict = chat_json(texto, system_prompt=system_prompt, max_tokens=64)

    etiqueta = data.get("intencion")
    if etiqueta not in {"nuevo_frente", "hablar_frente", "conversacion"}:
        etiqueta = "conversacion"

    frente = data.get("frente")
    if etiqueta != "hablar_frente":
        frente = None

    return etiqueta, frente


__all__ = ["detect"]
