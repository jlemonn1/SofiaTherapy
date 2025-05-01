# app/ia/estado.py
from enum import Enum

class EstadoConversacional(str, Enum):
    """Estados del diálogo según el diagrama de la máquina."""
    GENERAL          = "CONVERSACION_GENERAL"
    CONFIRM_NUEVO    = "CONFIRM_NUEVO"
    CONFIRM_RETOMAR  = "CONFIRM_RETOMAR"
    EN_FRENTE        = "EN_FRENTE"
