from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nombre: str
    email: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    about: str | None = None
    ai_mode: str