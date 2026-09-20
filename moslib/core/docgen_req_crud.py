"""CRUD y tablas markdown de requisitos docgen."""

from __future__ import annotations

import json

from moslib.core.docgen_req import (
    CAMPOS_REQ,
    area_ids,
    guardar_req,
    list_areas,
    load_req,
    parse_req_id,
    req_path,
    reqs_dir,
)


def req_add(req_id: str, texto: str, prioridad: str = "Must", verificacion: str = "Test"):
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


def req_set(req_id: str, campo: str, valor: str):
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


def req_rm(req_id: str):
    req_id, _ = parse_req_id(req_id)
    path = req_path(req_id)
    if not path.is_file():
        raise FileNotFoundError(req_id)
    path.unlink()
    return path


def list_reqs() -> list[dict]:
    return [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted(reqs_dir().glob("REQ-*.json"))
    ]


def tablas_por_area() -> str:
    grupos = {}
    for item in list_reqs():
        grupos.setdefault(item.get("area") or "?", []).append(item)
    orden = [a.get("id") for a in list_areas() if a.get("id")]
    extras = sorted(a for a in grupos if a not in orden)
    nombres = {a.get("id"): a.get("nombre") or a.get("id") for a in list_areas()}
    bloques = []
    nl = chr(10)
    for area in orden + extras:
        filas = grupos.get(area) or []
        if not filas:
            continue
        lineas = [
            f"### {nombres.get(area, area)}",
            "",
            "| Id | Texto | Prioridad | Verificación |",
            "|-----|-------|-----------|--------------|",
        ]
        for item in sorted(filas, key=lambda r: r.get("id") or ""):
            t = item.get("texto") or item.get("titulo") or ""
            lineas.append(
                f"| {item.get('id')} | {t} | "
                f"{item.get('prioridad') or ''} | {item.get('verificacion') or ''} |"
            )
        bloques.append(nl.join(lineas))
    return (nl + nl).join(bloques)
