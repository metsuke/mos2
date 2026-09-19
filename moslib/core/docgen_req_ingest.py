"""Ingesta de requisitos desde tablas markdown."""

from __future__ import annotations

import re
from pathlib import Path


def _celdas(linea: str) -> list[str]:
    if not linea.strip().startswith("|"):
        return []
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def _es_separador(linea: str) -> bool:
    c = _celdas(linea)
    return bool(c) and all(set(x) <= set("-: ") and "-" in x for x in c)


def ingest_reqs_desde_texto(texto: str, origen: str) -> list[Path]:
    from moslib.core.docgen_req import guardar_req
    from moslib.core.docgen_req_area import asegurar_area

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
    from moslib.core.docgen_index import get_project_root
    from moslib.core.docgen_io import mejor_origen

    origen = mejor_origen(
        "02-srs",
        get_project_root() / "docs" / "specs" / "02-SRS-Software-Requirements.md",
    )
    return ingest_reqs_desde_texto(origen.read_text(encoding="utf-8"), str(origen))
