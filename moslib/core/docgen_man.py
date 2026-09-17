"""SINOPSIS del man desde sinopsis(). Sin bloque HELP DEL COMANDO."""

from __future__ import annotations

import importlib
import json

from moslib.core import docgen as motor

MARCA_SINOPSIS = "(generado desde sinopsis(); no editar)"


def es_sinopsis(titulo: str) -> bool:
    return titulo.strip().lower().replace("ó", "o") in ("sinopsis", "synopsis")


def es_help_cmd(titulo: str) -> bool:
    clave = titulo.strip().lower().replace("é", "e")
    return clave in ("help del comando", "help") or clave.startswith("help del")


def marcar_sinopsis_en_store(nombre: str) -> None:
    path = motor.man_store_path(nombre)
    if not path.is_file():
        return
    extra = json.loads(path.read_text(encoding="utf-8"))
    extra["cuerpo_completo"] = None
    secciones = []
    hay = False
    for sec in extra.get("secciones") or []:
        tit = sec.get("titulo") or ""
        if es_help_cmd(tit):
            continue
        if es_sinopsis(tit):
            sec["cuerpo"] = MARCA_SINOPSIS
            sec["fuente"] = "sinopsis()"
            hay = True
        secciones.append(sec)
    if not hay:
        secciones.insert(
            1 if secciones else 0,
            {"titulo": "SINOPSIS", "cuerpo": MARCA_SINOPSIS, "fuente": "sinopsis()"},
        )
    extra["secciones"] = secciones
    path.write_text(json.dumps(extra, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def scan_usos_comando(nombre: str) -> list[str]:
    mod = importlib.import_module(f"moslib.commands.{nombre}")
    fn = getattr(mod, "sinopsis", None)
    if callable(fn):
        filas = fn()
        if isinstance(filas, (list, tuple)) and filas:
            return [str(x) for x in filas if str(x).strip()]
    return [nombre]


def armar_man(nombre: str, extra: dict) -> str:
    bloques = [f"# {extra.get('titulo', nombre)}", ""]
    if extra.get("preambulo"):
        bloques.extend([extra["preambulo"], ""])
    usos = "\n".join(scan_usos_comando(nombre))
    hecha = False
    for sec in extra.get("secciones") or []:
        titulo = sec.get("titulo") or "SECCIÓN"
        if es_help_cmd(titulo):
            continue
        cuerpo = usos if es_sinopsis(titulo) else (sec.get("cuerpo") or "")
        if es_sinopsis(titulo):
            hecha = True
        bloques.extend([f"## {titulo}", cuerpo, ""])
    if not hecha:
        bloques.extend(["## SINOPSIS", usos, ""])
    return "\n".join(bloques)