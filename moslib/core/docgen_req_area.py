"""CRUD de áreas docgen."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core import docgen as motor


def load_areas() -> dict:
    path = motor.get_areas_path()
    if not path.is_file():
        return {"schema": "metsuos-docgen-areas-1", "areas": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_areas(data: dict) -> Path:
    path = motor.get_areas_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from moslib.core.docgen_hash import registrar_destino
    registrar_destino(path)
    return path


def area_ids() -> set[str]:
    return {a["id"] for a in load_areas().get("areas") or [] if a.get("id")}


def list_areas() -> list[dict]:
    return list(load_areas().get("areas") or [])


def area_add(area_id: str, nombre: str = "") -> Path:
    area_id = (area_id or "").strip().upper()
    if not area_id:
        raise ValueError("falta id de área")
    data = load_areas()
    actuales = data.setdefault("areas", [])
    if any(a.get("id") == area_id for a in actuales):
        raise FileExistsError(area_id)
    actuales.append({"id": area_id, "nombre": nombre or area_id})
    return save_areas(data)


def area_set(area_id: str, nombre: str) -> Path:
    area_id = (area_id or "").strip().upper()
    data = load_areas()
    for item in data.get("areas") or []:
        if item.get("id") == area_id:
            item["nombre"] = nombre
            return save_areas(data)
    raise FileNotFoundError(area_id)


def area_rm(area_id: str) -> Path:
    area_id = (area_id or "").strip().upper()
    from moslib.core.docgen_req import list_reqs
    usados = [r["id"] for r in list_reqs() if r.get("area") == area_id]
    if usados:
        raise ValueError(f"área {area_id} tiene requisitos: {', '.join(usados)}")
    data = load_areas()
    antes = len(data.get("areas") or [])
    data["areas"] = [a for a in data.get("areas") or [] if a.get("id") != area_id]
    if len(data["areas"]) == antes:
        raise FileNotFoundError(area_id)
    return save_areas(data)


def asegurar_area(area: str) -> bool:
    area = (area or "").strip().upper()
    if not area or area in area_ids():
        return False
    area_add(area, area)
    return True
