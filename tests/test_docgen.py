"""Humo de docgen, requisitos, áreas y HTML."""

from moslib.commands import docgen as cmd
from moslib.core import docgen as motor
from moslib.core import docgen_html
from moslib.core import docgen_req as reqs


def test_inventario_tiene_srs_y_manual():
    ids = motor.list_document_ids()
    assert "02-srs" in ids
    assert "user-manual" in ids
    assert "license" in ids


def test_resolve_srs():
    path = motor.resolve_path("02-srs")
    assert path is not None
    assert path.name.endswith("Software-Requirements.md")


def test_id_desconocido():
    assert motor.get_documento("no-existe") is None


def test_comando_help_incluye_req_y_area():
    texto = cmd.help()
    assert "docgen" in texto
    assert "req" in texto
    assert "area" in texto


def test_comando_list_no_lanza():
    cmd.execute(["list"])


def test_partir_sin_secciones_conserva_cuerpo():
    titulo, pre, secs, cuerpo = motor._partir_markdown(
        "GNU GENERAL PUBLIC LICENSE\nVersion 3\n",
        "license",
    )
    assert "GNU GENERAL PUBLIC LICENSE" in cuerpo
    assert secs == []


def test_partir_con_preambulo():
    texto = (
        "# 05 – SDD\n\n"
        "**Versión del documento:** 1.2\n\n"
        "---\n\n"
        "## Propósito\n\n"
        "Texto.\n"
    )
    titulo, pre, secs, cuerpo = motor._partir_markdown(texto, "05-sdd")
    assert "Versión del documento" in pre
    assert secs[0]["titulo"] == "Propósito"


def test_generate_spec_todos_no_es_ingest():
    src = motor.generate_spec_todos.__code__.co_names
    assert "ingest_spec_todos" not in src
    assert "ingest_spec" not in src


def test_markdown_a_html_titulos_y_tabla():
    md = "# T\n\n## S\n\n| A | B |\n|---|---|\n| 1 | 2 |\n"
    out = docgen_html.markdown_a_html(md, "t")
    assert "<h1>" in out
    assert "<table>" in out


def test_tablas_por_area_no_lanza():
    texto = reqs.tablas_por_area()
    assert isinstance(texto, str)


def test_parse_req_id():
    ident, area = reqs.parse_req_id("REQ-CMD-021")
    assert ident == "REQ-CMD-021"
    assert area == "CMD"


def test_list_areas_es_lista():
    items = reqs.list_areas()
    assert isinstance(items, list)