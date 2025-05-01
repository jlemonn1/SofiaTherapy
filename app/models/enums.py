# app/models/enums.py
from enum import Enum

class TipoRecuerdo(str, Enum):
    REFLEXION = "reflexión"
    EMOCION   = "emoción"
    AVANCE    = "avance"
    IDEA      = "idea"
    RETROCESO = "retroceso"
