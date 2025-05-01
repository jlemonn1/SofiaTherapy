# app/ia/modelos/desviometro.py
"""
es_desvio(texto, contexto=None) -> bool

• `contexto` debe ser una string que resuma el frente (título + recuerdos),
  opcional pero recomendable para mayor precisión.
• Devuelve True cuando el mensaje NO pertenece al tema.
"""

from __future__ import annotations
from typing import Dict, List, Optional

from app.ia.llm import chat_json

# ───────────────────────── Prompt ─────────────────────────
_SYSTEM_PROMPT: str = """
Responde SOLO con JSON: { "desvio": true | false }

Criterios:
- desvio = false → el mensaje pertenece claramente al mismo tema/contexto.
- desvio = true  → el mensaje introduce un asunto distinto.
No añadas comentarios.
""".strip()

# ───────────────────────── API ─────────────────────────
def es_desvio(texto: str, *, contexto: Optional[str] = None) -> bool:
    user_prompt = (
        f"CONTEXTO DEL TEMA:\n{contexto}\n\nMENSAJE:\n{texto}"
        if contexto
        else texto
    )
    data: Dict = chat_json(user_prompt, system_prompt=_SYSTEM_PROMPT, max_tokens=64)
    return data.get("desvio") is True


__all__: List[str] = ["es_desvio"]
