"""Humo de tuplas docgen."""

from moslib.core.docgen_tupla_path import normalizar_id, tupla_path


def test_normalizar_id():
    assert normalizar_id("/req/REQ-INT-001/") == "req/REQ-INT-001"


def test_tupla_path_respeta_ruta():
    path = tupla_path("req/REQ-INT-001")
    assert path.as_posix().endswith("tuplas/req/REQ-INT-001.json")


def test_id_con_puntos_se_rechaza():
    try:
        normalizar_id("req/../sec")
    except ValueError:
        return
    raise AssertionError("debía rechazar ..")
