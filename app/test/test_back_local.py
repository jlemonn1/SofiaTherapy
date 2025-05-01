import datetime as _dt
import pytest

import app.back_local as bl
from app.models.enums import TipoRecuerdo
from app.ia.estado import EstadoConversacional


def test_estado_basico(usuario_1):
    assert bl.get_estado_usuario(usuario_1) == EstadoConversacional.GENERAL

    bl.set_estado_usuario(usuario_1, EstadoConversacional.CONFIRM_NUEVO)
    assert bl.get_estado_usuario(usuario_1) == EstadoConversacional.CONFIRM_NUEVO

    bl.reset_estado_usuario(usuario_1)
    assert bl.get_estado_usuario(usuario_1) == EstadoConversacional.GENERAL


def test_crear_y_listar_frentes(usuario_1):
    fid = bl.create_frente(usuario_1, "Proyecto IA", "desc")
    frentes = bl.obtener_frentes(usuario_1)
    assert any(f.id == fid and f.titulo == "Proyecto IA" for f in frentes)


def test_frente_actual(usuario_1):
    fid = bl.create_frente(usuario_1, "Tema A")
    bl.set_frente_actual(usuario_1, fid)
    assert bl.get_frente_actual(usuario_1) == fid

    bl.set_frente_actual(usuario_1, None)
    assert bl.get_frente_actual(usuario_1) is None


def test_guardar_mensaje_y_contador(usuario_1):
    fid = bl.create_frente(usuario_1, "Contador")
    # enviamos 9 mensajes, contador debe ser 9 y sin recuerdo auto
    for i in range(9):
        bl.guardar_mensaje(usuario_1, f"msg {i+1}", "usuario", frente_id=fid)

    fr = next(f for f in bl.obtener_frentes(usuario_1) if f.id == fid)
    assert fr.contador_mensajes == 9

    recs = bl.recordar_frente(fid, limite=10)
    assert len(recs) == 0  # aún no hay recuerdo auto

    # décimo mensaje → se crea recuerdo automático
    bl.guardar_mensaje(usuario_1, "msg 10", "usuario", frente_id=fid)
    fr = next(f for f in bl.obtener_frentes(usuario_1) if f.id == fid)
    assert fr.contador_mensajes == 10

    recs = bl.recordar_frente(fid, limite=10)
    assert len(recs) == 1
    assert "Mensaje #10" in recs[0]


def test_obtener_ultimos_mensajes(usuario_1):
    fid = bl.create_frente(usuario_1, "Historial")
    bl.guardar_mensaje(usuario_1, "hola", "usuario", frente_id=fid)
    bl.guardar_mensaje(usuario_1, "respuesta", "sofia", frente_id=fid)

    ultimos = bl.obtener_ultimos_mensajes(usuario_1)
    assert len(ultimos) >= 2
    assert ultimos[0].texto in {"respuesta", "hola"}


def test_recuerdos_manuales(usuario_1):
    fid = bl.create_frente(usuario_1, "Notas")
    rid = bl.añadir_recuerdo(fid, "idea", "anotar idea A")
    recs = bl.recordar_frente(fid)
    assert any("idea A" in r for r in recs)
    assert rid is not None


def test_diario(usuario_1, session):
    from app.models.entrada_diaria import EntradaDiaria

    # 2 entradas: una hoy, otra hace 10 días
    hoy = EntradaDiaria(usuario_id=usuario_1, eventos="hoy")
    antes = EntradaDiaria(
        usuario_id=usuario_1,
        fecha=_dt.datetime.utcnow() - _dt.timedelta(days=10),
        eventos="antes",
    )
    session.add_all([hoy, antes])
    session.commit()

    todas = bl.ver_todas_entradas(usuario_1)
    assert len(todas) == 2

    semana = bl.ver_entradas_semana(usuario_1)
    assert len(semana) == 1
    assert semana[0].eventos == "hoy"
