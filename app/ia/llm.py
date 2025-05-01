# app/ia/llm.py
"""
Envoltorio ligero sobre `huggingface_hub.InferenceClient`
para evitar repetir boilerplate y facilitar respuestas JSON.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Dict, List, Optional

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
logger = logging.getLogger(__name__)

# ───────────── Config ─────────────
HF_API_KEY    = os.getenv("HF_API_KEY") or "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"
HF_PROVIDER   = "nebius"
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"

_client = InferenceClient(
    provider=HF_PROVIDER,
    api_key=HF_API_KEY,
)

FALLBACK_TEXT = "Lo siento, no puedo responder en este momento. ¿Puedes intentarlo más tarde?"


# ───────────── Helpers internos ─────────────
def _call_llm(
    messages: List[Dict[str, str]],
    model: str = DEFAULT_MODEL,
    max_tokens: int = 512,
) -> str:
    for intento in range(3):
        try:
            completion = _client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.warning(f"⚠️ Error al llamar al modelo (intento {intento+1}/3): {e}")
            time.sleep(1.5)

    logger.error("❌ No se pudo obtener respuesta del modelo tras 3 intentos.")
    return FALLBACK_TEXT


def _safe_json(text: str) -> Dict:
    """
    Limpia el texto devuelto por la IA y extrae un JSON válido.
    Admite formatos con ```json ... ``` y otros ruidos.
    """
    try:
        # Elimina cualquier bloque de código markdown
        text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).strip("` \n")

        # Busca el primer bloque JSON válido
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            logger.warning("⚠️ No se encontró JSON en: %s", text[:120])
            return {}
    except Exception as e:
        logger.warning(f"⚠️ JSON malformado o error inesperado: {e}")
        return {}
# ───────────── API pública ─────────────
def chat(
    messages: List[Dict[str, str]],
    *,
    system: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 512,
) -> str:
    """Devuelve texto libre (`content`) del modelo."""
    if system:
        messages = [{"role": "system", "content": system}] + messages
    return _call_llm(messages, model=model, max_tokens=max_tokens)


def chat_json(
    user_prompt: str,
    *,
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 256,
) -> Dict:
    """
    Envía system + user y devuelve dict (o {} si no parsea).
    Útil para clasificador / confirmador / desviometro.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    raw = _call_llm(messages, model=model, max_tokens=max_tokens)
    return _safe_json(raw)


__all__ = ["chat", "chat_json"]
