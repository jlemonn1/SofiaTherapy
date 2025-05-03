from pydantic import BaseModel
from datetime import datetime

class FrenteCreate(BaseModel):
    usuario_id: int
    titulo: str
    descripcion: str = ""

class FrenteOut(BaseModel):
    id: int
    nombre: str
    color: str = "gray"  # si en el modelo real usas colores
    creado_en: datetime
