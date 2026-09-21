"""Indice docgen en disco + alias que espera docgen.py."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.docgen_index_paths import get_index_path, get_project_root


def get_docgen_dir() -> Path:
    return get_project_root() / "docs" / "docgen"


def get_backup_dir() -> Path:
    return get_docgen_dir() / "backup"


def get_areas_path() -> Path:
    return get_docgen_dir() / "areas.json"


def ensure_docgen_dirs() -> None:
    for d in (get_docgen_dir(), get_backup_dir(), get_docgen_dir() / "pages"):
        d.mkdir(parents=True, exist_ok=True)


def load_index() -> dict:
    path = get_index_path()
    if not path.is_file():
        return {"schema": "metsuos-docgen-index-1", "documentos": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_index(data: dict) -> None:
    path = get_index_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def documentos() -> list:
    return list(load_index().get("documentos") or [])


def todos_documentos() -> list:
    return documentos()


def list_document_ids() -> list:
    return [x.get("id") for x in documentos() if x.get("id")]


def man_documentos() -> list:
    return [x for x in documentos() if str(x.get("rel", "")).startswith("docs/man/")]


def get_documento(doc_id: str):
    for item in documentos():
        if item.get("id") == doc_id:
            return item
    return None


def resolve_path(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None:
        raise KeyError(doc_id)
    return get_project_root() / item["rel"]


resuelve_path = resolve_path
DOCUMENTOS = tuple((x.get("id"), x.get("rel")) for x in documentos())
