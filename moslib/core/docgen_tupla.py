"""Schema metsuos-tupla-1. Un JSON por nodo."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from moslib.core.docgen_tupla_path import normalizar_id, tupla_path

SCHEMA = "metsuos-tupla-1"
CAMPOS = (
    "schema", "id", "tipo", "titulo", "cuerpo", "cuerpo_desde",
    "para_humano", "para_ia", "orden", "orden_por_que",
    "influye_de", "influye_a", "creado", "modificado",
    "render", "activo",
)
IGNORAR_CMP = frozenset({"modificado"})


def ahora() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def plantilla(ident: str, tipo: str = "elemento") -> dict:
    ident = normalizar_id(ident)
    marca = ahora()
    return {
        "schema": SCHEMA,
        "id": ident,
        "tipo": tipo or "elemento",
        "titulo": "",
        "cuerpo": "",
        "cuerpo_desde": "",
        "para_humano": "",
        "para_ia": "",
        "orden": 0,
        "orden_por_que": "",
        "influye_de": [],
        "influye_a": [],
        "creado": marca,
        "modificado": marca,
        "render": "parrafo",
        "activo": True,
    }


def load_tupla(ident: str) -> dict:
    path = tupla_path(ident)
    if not path.is_file():
        raise FileNotFoundError(ident)
    return json.loads(path.read_text(encoding="utf-8"))


def _util(data: dict) -> dict:
    return {k: data.get(k) for k in CAMPOS if k not in IGNORAR_CMP}


def guardar_tupla(data: dict):
    ident = normalizar_id(data["id"])
    data["id"] = ident
    data["schema"] = SCHEMA
    path = tupla_path(ident)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        try:
            viejo = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            viejo = None
        if isinstance(viejo, dict) and _util(viejo) == _util(data):
            return path
    data["modificado"] = ahora()
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    try:
        from moslib.core.integridad import registrar
        from moslib.core.docgen_index import get_project_root
        rel = path.resolve().relative_to(get_project_root().resolve()).as_posix()
        registrar(rel)
    except Exception:
        pass
    return path
