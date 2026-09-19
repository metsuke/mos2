"""Un JSON por requisito. Áreas vía CRUD."""

from __future__ import annotations

import json
import re
from pathlib import Path

from moslib.core import docgen as motor
from moslib.core.docgen_req_area import (
    area_add, area_ids, area_rm, area_set, asegurar_area,
    list_areas, load_areas, save_areas,
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


def req_add(req_id: str, texto: str, prioridad: str = "Must", verificacion: str = "Test") -> Path:
    req_id, area = parse_req_id(req_id)
    if area not in area_ids():
        raise ValueError(f"área {area} no existe; docgen area add {area} <nombre>")
    if req_path(req_id).is_file():
        raise FileExistsError(req_id)
    return guardar_req({
        "schema": "metsuos-docgen-req-1", "id": req_id, "area": area,
        "titulo": texto, "texto": texto, "prioridad": prioridad,
        "verificacion": verificacion, "notas": "",
    })


def req_set(req_id: str, campo: str, valor: str) -> Path:
    req_id, _ = parse_req_id(req_id)
    if campo not in CAMPOS_REQ:
        raise ValueError(f"campo no válido: {campo}")
    data = load_req(req_id)
    if campo == "area":
        valor = valor.strip().upper()
        if valor not in area_ids():
            raise ValueError(f"área {valor} no existe; docgen area add {valor}")
    data[campo] = valor
    return guardar_req(data)


def req_rm(req_id: str) -> Path:
    req_id, _ = parse_req_id(req_id)
    path = req_path(req_id)
    if not path.is_file():
        raise FileNotFoundError(req_id)
    path.unlink()
    return path


def list_reqs() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(reqs_dir().glob("REQ-*.json"))]


def tablas_por_area() -> str:
    grupos = {}
    for item in list_reqs():
        grupos.setdefault(item.get("area") or "?", []).append(item)
    orden = [a.get("id") for a in list_areas() if a.get("id")]
    extras = sorted(a for a in grupos if a not in orden)
    nombres = {a.get("id"): a.get("nombre") or a.get("id") for a in list_areas()}
    bloques = []
    for area in orden + extras:
        filas = grupos.get(area) or []
        if not filas:
            continue
        lineas = [f"### {nombres.get(area, area)}", "", "| Id | Texto | Prioridad | Verificación |", "|-----|-------|-----------|--------------|"]
        for item in sorted(filas, key=lambda r: r.get("id") or ""):
            t = item.get("texto") or item.get("titulo") or ""
            lineas.append(f"| {item.get('id')} | {t} | {item.get('prioridad') or ''} | {item.get('verificacion') or ''} |")
        bloques.append("\n".join(lineas))
    return "\n\n".join(bloques)
