"""
moslib.core.docgen_req
Un JSON por requisito en docs/docgen/reqs/.
Al ingest: si aparece un área que no está en areas.json, se añade.
Al generate: no se toca areas.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from moslib.core import docgen as motor

REQ_ID = re.compile(r"REQ-([A-Z]+)-(\d+)")


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


def asegurar_area(area: str) -> bool:
    """Si el área no existe, la incorpora. Devuelve True si escribió."""
    area = (area or "").strip().upper()
    if not area:
        return False
    data = load_areas()
    actuales = data.setdefault("areas", [])
    if any(a.get("id") == area for a in actuales):
        return False
    actuales.append({"id": area, "nombre": area})
    save_areas(data)
    return True


def guardar_req(payload: dict) -> Path:
    req_id = payload["id"]
    dest = req_path(req_id)
    dest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return dest


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
        cabs = _celdas(lineas[i])
        if cabs and i + 1 < len(lineas) and _es_separador(lineas[i + 1]):
            i += 2
            while i < len(lineas):
                celdas = _celdas(lineas[i])
                if not celdas:
                    break
                i += 1
                req_id = None
                area = None
                for cel in celdas:
                    m = REQ_ID.search(cel)
                    if m:
                        area = m.group(1)
                        req_id = f"REQ-{area}-{m.group(2)}"
                        break
                if not req_id:
                    continue
                if asegurar_area(area):
                    print(f"[docgen] Área nueva en areas.json: {area}")
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


def list_reqs() -> list[dict]:
    out = []
    for path in sorted(reqs_dir().glob("REQ-*.json")):
        out.append(json.loads(path.read_text(encoding="utf-8")))
    return out


def tablas_por_area() -> str:
    grupos = {}
    for item in list_reqs():
        grupos.setdefault(item.get("area") or "?", []).append(item)
    orden = [a.get("id") for a in load_areas().get("areas") or [] if a.get("id")]
    extras = sorted(a for a in grupos if a not in orden)
    data_areas = {
        a.get("id"): a.get("nombre") or a.get("id")
        for a in load_areas().get("areas") or []
    }
    bloques = []
    for area in orden + extras:
        filas = grupos.get(area) or []
        if not filas:
            continue
        nombre = data_areas.get(area, area)
        lineas = [
            f"### {nombre}",
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