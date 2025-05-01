# app/db/base.py
"""
Configura el engine, SessionLocal y Base para toda la aplicación.
Lee las credenciales de variables de entorno (.env) y usa MySQL.
"""

from __future__ import annotations

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ───────────────────────────────────────────────
# Cargar variables de entorno (.env opcional)
# ───────────────────────────────────────────────
load_dotenv()  # busca .env en el cwd

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "chatbot_terapia")

# utf8mb4: admite emojis 👍
DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

# ───────────────────────────────────────────────
# Engine y Session
# ───────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    echo=False,          # pon True si quieres SQL en consola
    future=True,         # API 2.0
    pool_pre_ping=True,  # reconecta si la conexión se cae
    pool_recycle=3600,   # recicla conexiones viejas (segundos)
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# ───────────────────────────────────────────────
# Declarative Base (todos los modelos la heredan)
# ───────────────────────────────────────────────
Base = declarative_base()
