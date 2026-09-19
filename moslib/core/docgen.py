"""Fachada docgen. Fuente JSON. generate no ingiere."""

from moslib.core.docgen_index import (
    DOCUMENTOS,
    ensure_docgen_dirs,
    get_areas_path,
    get_backup_dir,
    get_docgen_dir,
    get_documento,
    get_project_root,
    list_document_ids,
    man_documentos,
    resolve_path,
    todos_documentos,
)
from moslib.core.docgen_io import (
    backup_document,
    backup_stamp,
    escribir,
    list_backups,
    mejor_origen,
    partir_markdown,
    recuperar_preambulo,
)
from moslib.core.docgen_man_run import (
    generate_man,
    generate_man_todos,
    ingest_man,
    ingest_man_todos,
    list_man_nombres,
    man_store_path,
    render_man,
    scan_command_help,
)
from moslib.core.docgen_page_run import (
    generate_doc,
    generate_page_todos,
    ingest_doc,
    ingest_page_todos,
    list_page_ids,
    render_doc,
    store_path_doc,
)
from moslib.core.docgen_spec_run import (
    generate_spec,
    generate_spec_todos,
    ingest_spec,
    ingest_spec_todos,
    list_spec_ids,
    render_spec,
    spec_store_path,
)

_escribir = escribir
_mejor_origen = mejor_origen
_partir_markdown = partir_markdown
_recuperar_preambulo = recuperar_preambulo


def ingest_todo() -> list:
    return ingest_man_todos(True) + ingest_spec_todos(True) + ingest_page_todos(True)


def generate_todo() -> list:
    return generate_man_todos() + generate_spec_todos() + generate_page_todos()
