from __future__ import annotations
from typing import List
from app.ia.llm import chat

_SYSTEM_PROMPT = """
You are an assistant that detects whether a Spanish message expresses clear affirmation.

You will receive a user message in Spanish. Your task is to answer only:

- "yes" → if the message is clearly affirmative (e.g. "sí", "vale", "claro", "por supuesto", "de acuerdo", etc.)
- "no" → if the message expresses rejection, doubt, questions, or anything else.

Respond with a single word only: "yes" or "no". No punctuation, no explanations.
""".strip()

def es_si(texto: str) -> bool:
    """Returns True if the model responds 'yes', meaning the message is clearly affirmative."""
    try:
        respuesta = chat(
            [{"role": "user", "content": texto}],
            system=_SYSTEM_PROMPT,
            max_tokens=4
        ).strip().lower()

        print(f"[confirmador] Model replied: {respuesta}")
        return respuesta == "yes"
    except Exception as e:
        print(f"[confirmador] ⚠️ Error en confirmador: {e}")
        return False


__all__: List[str] = ["es_si"]
