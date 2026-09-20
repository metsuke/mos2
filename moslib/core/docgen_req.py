"""Un JSON por requisito. Áreas vía CRUD."""

from __future__ import annotations

import json
import re
from pathlib import Path

from moslib.core import docgen as motor
from moslib.core.docgen_req_area import (
    area_add,
    area_ids,
    area_rm,
    area_set,
    asegurar_area,
    list_areas,
    load_areas,
    save_areas,
)

REQ_ID = re.compile(r"^REQ-([A-Z]+)-(\d+)$")
CAMPOS_REQ = ("titulo", "texto", "prioridad", "verificacion", "notas", "area")


def ingest_reqs_desde_texto(texto: str, origen: str):
    from moslib.core.docgen_req_ingest import ingest_reqs_desde_texto as _fn
    return _fn(texto, origen)


def ingest_reqs_srs():
    from moslib.core.docgen_req_ingest import ingest_reqs_srs as _fn
    return _fn()


def reqs_dir() -> Path:
    d = motor.get_docgen_dir() / "reqs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def req_path(req_id: str) -> Path:
    return reqs_dir() / f"{req_id}.json"


def guardar_req(payload: dict) -> Path:
    dest = req_path(payload["id"])
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def load_req(req_id: str) -> dict:
    path = req_path(req_id)
    if not path.is_file():
        raise FileNotFoundError(req_id)
    return json.loads(path.read_text(encoding="utf-8"))


def parse_req_id(req_id: str) -> tuple[str, str]:
    m = REQ_ID.match((req_id or "").strip())
    if not m:
        raise ValueError(f"id inválido: {req_id}")
    return f"REQ-{m.group(1)}-{m.group(2)}", m.group(1)


def req_add(*a, **k):
    from moslib.core.docgen_req_crud import req_add as _fn
    return _fn(*a, **k)


def req_set(*a, **k):
    from moslib.core.docgen_req_crud import req_set as _fn
    return _fn(*a, **k)


def req_rm(*a, **k):
    from moslib.core.docgen_req_crud import req_rm as _fn
    return _fn(*a, **k)


def list_reqs():
    from moslib.core.docgen_req_crud import list_reqs as _fn
    return _fn()


def tablas_por_area():
    from moslib.core.docgen_req_crud import tablas_por_area as _fn
    return _fn()
