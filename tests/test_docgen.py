"""Humo del motor y del comando docgen."""

from moslib.commands import docgen as cmd
from moslib.core import docgen as motor


def test_inventario_tiene_srs_y_manual():
    ids = motor.list_document_ids()
    assert "02-srs" in ids
    assert "user-manual" in ids
    assert "readme" in ids


def test_resolve_srs():
    path = motor.resolve_path("02-srs")
    assert path is not None
    assert path.name.endswith("Software-Requirements.md")


def test_id_desconocido():
    assert motor.get_documento("no-existe") is None
    assert motor.resolve_path("no-existe") is None


def test_comando_help_no_vacio():
    texto = cmd.help()
    assert isinstance(texto, str)
    assert "docgen" in texto


def test_comando_list_no_lanza():
    cmd.execute(["list"])

def test_render_man_echo_incluye_ayuda():
    texto = motor.render_man_echo()
    assert texto.startswith("# echo")
    assert "echo" in texto
    assert "Imprime texto" in texto or "imprime texto" in texto


def test_ingest_echo_escribe_json():
    dest = motor.ingest_man("echo")
    assert dest.is_file()
    texto = dest.read_text(encoding="utf-8")
    assert "echo" in texto