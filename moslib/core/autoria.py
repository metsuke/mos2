"""Autoría del sistema y segmentos legales."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.docgen_index import get_project_root

CAMPOS = (
    "programa", "autor", "email", "email_alt",
    "anio_desde", "anio_hasta", "contacto",
)
DEFAULTS = {
    "schema": "metsuos-autoria-1",
    "programa": "MetsuOS",
    "autor": "Raul Carrillo Garrido aka metsuke",
    "email": "metsuke@gmail.com",
    "email_alt": "rcarrillo@metsuke.com, metsuke@icloud.com",
    "anio_desde": "2026",
    "anio_hasta": "2026",
    "contacto": "https://metsuke.com",
}


def ruta() -> Path:
    return get_project_root() / "docs" / "docgen" / "autoria.json"


def load() -> dict:
    data = dict(DEFAULTS)
    path = ruta()
    if path.is_file():
        data.update(json.loads(path.read_text(encoding="utf-8")))
    return data


def save(data: dict) -> Path:
    path = ruta()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        from moslib.core.integridad import registrar
        rel = path.resolve().relative_to(get_project_root().resolve()).as_posix()
        registrar(rel)
    except Exception:
        pass
    return path


def set_campo(clave: str, valor: str) -> Path:
    if clave not in CAMPOS:
        raise ValueError("campos: " + " ".join(CAMPOS))
    data = load()
    data[clave] = valor
    return save(data)


def anio_rango(data=None) -> str:
    d = data or load()
    a = str(d.get("anio_desde") or "").strip()
    b = str(d.get("anio_hasta") or a).strip()
    if not a:
        a = b
    if not b or a == b:
        return a or "2026"
    return f"{a}-{b}"


def aviso_gpl() -> str:
    d = load()
    prog = d.get("programa") or "MetsuOS"
    autor = d.get("autor") or DEFAULTS["autor"]
    email = d.get("email") or DEFAULTS["email"]
    alt = (d.get("email_alt") or "").strip()
    anio = anio_rango(d)
    extras = ", " + alt if alt else ""
    return (
        f"{prog} — sistema operativo documental.\n"
        f"Copyright (C) {anio}  {autor} <{email}{extras}>\n\n"
        "This program is free software: you can redistribute it and/or modify\n"
        "it under the terms of the GNU General Public License as published by\n"
        "the Free Software Foundation, either version 3 of the License, or\n"
        "(at your option) any later version.\n"
    )


SEGMENTOS = {"autoria.aviso_gpl": aviso_gpl}


def resolver(nombre: str) -> str:
    fn = SEGMENTOS.get((nombre or "").strip())
    if not fn:
        raise KeyError(nombre)
    return fn()
