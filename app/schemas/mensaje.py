from pydantic import BaseModel
from datetime import datetime

class MensajeCreate(BaseModel):
    usuario_id: int
    texto: str
    origen: str  # 'usuario' | 'sofia'

class MensajeOut(BaseModel):
    id: int
    texto: str
    origen: str
    momento: datetime
