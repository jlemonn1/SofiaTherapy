"""
Fixtures compartidos: engine SQLite en memoria, SessionLocal parcheado
y datos mínimos (usuario #1).
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models               # registra tablas
from app.db.base import Base
import app.back_local as bl


@pytest.fixture(scope="session", autouse=True)
def _in_memory_db():
    """Sobrescribe bl.SessionLocal con SQLite en memoria."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)

    testing_session = sessionmaker(bind=engine, future=True, autoflush=False, autocommit=False)
    # parche global
    bl.SessionLocal = testing_session
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def session():
    """Devuelve una sesión explícita para inserciones directas."""
    with bl.SessionLocal() as db:
        yield db


@pytest.fixture()
def usuario_1(session):
    from app.models.usuario import Usuario

    u = Usuario(id=1, id_telegram="demo_tg", nombre="Demo")
    session.add(u)
    session.commit()
    return 1  # id
