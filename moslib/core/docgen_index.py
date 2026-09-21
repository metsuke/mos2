"""Indice de documentos: JSON en disco + mans."""

from __future__ import annotations

import json
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def get_docgen_dir() -> Path:
    return get_project_root() / "docs" / "docgen"


def get_backup_dir() -> Path:
    return get_docgen_dir() / "backup"


def get_areas_path() -> Path:
    return get_docgen_dir() / "areas.json"


def get_index_path() -> Path:
    return get_docgen_dir() / "index.json"


def ensure_docgen_dirs():
    get_backup_dir().mkdir(parents=True, exist_ok=True)
    base = get_docgen_dir()
    for nombre in ("specs", "man", "pages", "root", "html", "reqs", "plans"):
        (base / nombre).mkdir(parents=True, exist_ok=True)


def load_index() -> list:
    path = get_index_path()
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    items = data.get("documentos", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        return []
    out = []
    for item in items:
        if isinstance(item, dict) and item.get("id") and item.get("rel"):
            out.append({"id": str(item["id"]).lower(), "rel": str(item["rel"])})
    return out


def save_index(items: list) -> Path:
    ensure_docgen_dirs()
    path = get_index_path()
    orden = sorted(items, key=lambda x: x["id"])
    payload = {"schema": "metsuos-docgen-index-1", "documentos": orden}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def man_documentos() -> list:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    return [
        {"id": "man-" + path.stem, "rel": "docs/man/" + path.name}
        for path in sorted(man_dir.glob("*.md"))
    ]


def todos_documentos() -> list:
    vistos = {}
    for item in load_index() + man_documentos():
        vistos[item["id"]] = item
    return list(vistos.values())


def list_document_ids() -> list:
    return [d["id"] for d in todos_documentos()]


def get_documento(doc_id: str):
    key = (doc_id or "").strip().lower()
    for item in todos_documentos():
        if item["id"] == key:
            return dict(item)
    return None


def resolve_path(doc_id: str):
    item = get_documento(doc_id)
    if item is None:
        return None
    return get_project_root() / item["rel"]


resuelve_path = resolve_path
DOCUMENTOS = ()
