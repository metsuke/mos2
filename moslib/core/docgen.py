"""Fachada docgen. Fuente JSON. generate no ingiere."""

from __future__ import annotations

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
    bump_preambulo,
    escribir,
    list_backups,
    mejor_origen,
    partir_markdown,
    preambulo_completo,
    recuperar_preambulo,
    sin_version,
)
from moslib.core.docgen_man_run import (
    generate_man,
    generate_man_todos,
    ingest_man,
    ingest_man_todos,
    list_man_nombres,
    man_store_path,
    render_man,
)
from moslib.core.docgen_page_run import (
    generate_doc,
    ingest_doc,
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
_partir_markdown = partir_markdown
_recuperar_preambulo = recuperar_preambulo
_mejor_origen = mejor_origen
_bump_preambulo = bump_preambulo
_sin_version = sin_version
_preambulo_completo = preambulo_completo


def scan_command_help(nombre: str) -> str:
    import importlib

    mod = importlib.import_module(f"moslib.commands.{nombre}")
    texto = mod.help()
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"help() vacío en {nombre}")
    return texto.strip()


def ingest_page_todos(forzar: bool = True) -> list:
    ids = list_page_ids()
    if not forzar:
        ids = [i for i in ids if not store_path_doc(i).is_file()]
    return [ingest_doc(i) for i in ids]


def generate_page_todos() -> list:
    escritos = []
    for doc_id in list_page_ids():
        try:
            escritos.append(generate_doc(doc_id))
        except Exception as exc:
            print(f"[docgen] {doc_id}: {exc}")
    return escritos


def ingest_todo() -> list:
    return ingest_man_todos(True) + ingest_spec_todos(True) + ingest_page_todos(True)


def generate_todo() -> list:
    return generate_man_todos() + generate_spec_todos() + generate_page_todos()
