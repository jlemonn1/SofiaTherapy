from typing import Dict
from app.ia.llm import chat_json

_PROMPT = """
Eres una IA que recibe un texto de conversación en español. Tu tarea es:

1. Generar un título breve (máximo 20 caracteres) para un nuevo frente.
2. Generar una descripción (máximo 150 caracteres) que resuma el contenido.

Responde SOLO en JSON como este ejemplo:

{
  "titulo": "Ansiedad antes de los exámenes",
  "descripcion": "Conversación sobre la presión que siente la usuaria al prepararse para los exámenes y su miedo a fallar."
}
""".strip()

def generar_titulo_descripcion(contexto: str) -> Dict[str, str]:
    return chat_json(contexto, system_prompt=_PROMPT, max_tokens=300)
