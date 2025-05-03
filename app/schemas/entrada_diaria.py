from pydantic import BaseModel
from datetime import datetime
from typing import List

class EntradaDiariaCreate(BaseModel):
    usuario_id: int
    fecha: datetime
    titulo: str
    descripcion: str  # Se guardará como "reflexiones"
    emojis: List[int]   # Máximo 2

class EntradaDiariaOut(BaseModel):
    id: int
    date: datetime
    title: str
    description: str
    mood: List[int] 
