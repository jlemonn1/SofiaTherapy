from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TipoRecuerdo(str, Enum):
    reflexion = "reflexion"
    emocion = "emocion"
    avance = "avance"
    idea = "idea"
    retroceso = "retroceso"

class RecuerdoCreate(BaseModel):
    frente_id: int
    tipo: TipoRecuerdo
    contenido: str

class RecuerdoOut(BaseModel):
    id: int
    tipo: TipoRecuerdo
    contenido: str
    fecha: datetime
