"""
moslib.core.docgen_req
Un JSON por requisito. Áreas en areas.json vía CRUD.
ingest puede alta áreas. generate no toca areas.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from moslib.core import docgen as motor

REQ_ID = re.compile(r"^REQ-([A-Z]+)-(\d+)$")
CAMPOS_REQ = ("titulo", "texto", "prioridad", "verificacion", "notas", "area")


def reqs_dir() -> Path:
    d = motor.get_docgen_dir() / "reqs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def req_path(req_id: str) -> Path:
    return reqs_dir() / f"{req_id}.json"


def load_areas() -> dict:
    path = motor.get_areas_path()
    if not path.is_file():
        return {"schema": "metsuos-docgen-areas-1", "areas": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_areas(data: dict) -> Path:
    path = motor.get_areas_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
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


def guardar_req(payload: dict) -> Path:
    dest = req_path(payload["id"])
    dest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
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
    return guardar_req(
        {
            "schema": "metsuos-docgen-req-1",
            "id": req_id,
            "area": area,
            "titulo": texto,
            "texto": texto,
            "prioridad": prioridad,
            "verificacion": verificacion,
            "notas": "",
        }
    )


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
    out = []
    for path in sorted(reqs_dir().glob("REQ-*.json")):
        out.append(json.loads(path.read_text(encoding="utf-8")))
    return out


def _celdas(linea: str) -> list[str]:
    if not linea.strip().startswith("|"):
        return []
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def _es_separador(linea: str) -> bool:
    c = _celdas(linea)
    return bool(c) and all(set(x) <= set("-: ") and "-" in x for x in c)


def ingest_reqs_desde_texto(texto: str, origen: str) -> list[Path]:
    escritos = []
    lineas = texto.splitlines()
    i = 0
    while i < len(lineas):
        if _celdas(lineas[i]) and i + 1 < len(lineas) and _es_separador(lineas[i + 1]):
            i += 2
            while i < len(lineas):
                celdas = _celdas(lineas[i])
                if not celdas:
                    break
                i += 1
                hallado = re.search(r"REQ-([A-Z]+)-(\d+)", " ".join(celdas))
                if not hallado:
                    continue
                area = hallado.group(1)
                req_id = f"REQ-{area}-{hallado.group(2)}"
                if asegurar_area(area):
                    print(f"[docgen] Área nueva: {area}")
                resto = [c for c in celdas if req_id not in c]
                payload = {
                    "schema": "metsuos-docgen-req-1",
                    "id": req_id,
                    "area": area,
                    "titulo": resto[0] if resto else "",
                    "texto": resto[0] if resto else "",
                    "prioridad": "",
                    "verificacion": "",
                    "notas": "",
                    "origen": origen,
                }
                for cel in resto:
                    baja = cel.lower()
                    if baja in ("must", "should", "may"):
                        payload["prioridad"] = cel
                    elif baja in ("test", "demo", "inspection", "análisis", "analisis"):
                        payload["verificacion"] = cel
                escritos.append(guardar_req(payload))
            continue
        i += 1
    return escritos


def ingest_reqs_srs() -> list[Path]:
    origen = motor._mejor_origen(
        "02-srs",
        motor.get_project_root()
        / "docs"
        / "specs"
        / "02-SRS-Software-Requirements.md",
    )
    return ingest_reqs_desde_texto(origen.read_text(encoding="utf-8"), str(origen))


def tablas_por_area() -> str:
    grupos = {}
    for item in list_reqs():
        grupos.setdefault(item.get("area") or "?", []).append(item)
    orden = [a.get("id") for a in list_areas() if a.get("id")]
    extras = sorted(a for a in grupos if a not in orden)
    data_areas = {a.get("id"): a.get("nombre") or a.get("id") for a in list_areas()}
    bloques = []
    for area in orden + extras:
        filas = grupos.get(area) or []
        if not filas:
            continue
        lineas = [
            f"### {data_areas.get(area, area)}",
            "",
            "| Id | Texto | Prioridad | Verificación |",
            "|----|-------|-----------|--------------|",
        ]
        for item in sorted(filas, key=lambda r: r.get("id") or ""):
            texto = item.get("texto") or item.get("titulo") or ""
            lineas.append(
                f"| {item.get('id')} | {texto} | {item.get('prioridad') or ''} | {item.get('verificacion') or ''} |"
            )
        bloques.append("\n".join(lineas))
    return "\n\n".join(bloques)