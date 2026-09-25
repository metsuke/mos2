"""Migrar requisitos existentes a tuplas tipo=req."""

from __future__ import annotations

from moslib.core.docgen_req import list_reqs
from moslib.core.docgen_tupla import guardar_tupla, plantilla
from moslib.core.docgen_tupla_path import tupla_path


def req_a_tupla(item: dict) -> dict:
    ident = "req/" + (item.get("id") or "")
    data = plantilla(ident, "req")
    data["titulo"] = item.get("titulo") or item.get("texto") or ""
    data["cuerpo"] = item.get("texto") or item.get("titulo") or ""
    data["prioridad"] = item.get("prioridad") or "Must"
    data["verificacion"] = item.get("verificacion") or ""
    data["area"] = item.get("area") or ""
    data["notas"] = item.get("notas") or ""
    data["render"] = "tabla"
    data["para_humano"] = item.get("para_humano") or ""
    data["para_ia"] = item.get("para_ia") or ""
    return data


def migrar_reqs(forzar: bool = False) -> list:
    escritos = []
    for item in list_reqs():
        ident = "req/" + item["id"]
        if tupla_path(ident).is_file() and not forzar:
            continue
        escritos.append(guardar_tupla(req_a_tupla(item)))
    return escritos
