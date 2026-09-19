"""Corte de markdown y preámbulo de documentos."""

from __future__ import annotations

import re

from moslib.core.docgen_index import get_backup_dir
from pathlib import Path


def list_backups_local(doc_id: str) -> list[Path]:
    folder = get_backup_dir() / doc_id
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_file())


def partir_markdown(texto: str, titulo_defecto: str):
    lineas = texto.splitlines()
    if not any(linea.startswith("## ") for linea in lineas):
        titulo = titulo_defecto
        if lineas and lineas[0].startswith("# "):
            titulo = lineas[0][2:].strip()
        return titulo, "", [], texto
    titulo = titulo_defecto
    preambulo_lineas = []
    secciones = []
    actual = None
    buf = []
    visto_h1 = False

    def _cerrar():
        nonlocal actual, buf
        if actual is None:
            buf = []
            return
        secciones.append({"titulo": actual, "cuerpo": "\n".join(buf).strip()})
        actual = None
        buf = []

    for linea in lineas:
        if linea.startswith("## "):
            _cerrar()
            actual = linea[3:].strip()
            continue
        if linea.startswith("# "):
            titulo = linea[2:].strip()
            visto_h1 = True
            continue
        if actual is None and visto_h1:
            preambulo_lineas.append(linea)
            continue
        if actual is not None:
            buf.append(linea)
    _cerrar()
    return titulo, "\n".join(preambulo_lineas).strip(), secciones, None


def preambulo_completo(preambulo: str) -> bool:
    return "versión del documento" in preambulo.lower()


def recuperar_preambulo(doc_id: str, preambulo: str) -> str:
    if preambulo_completo(preambulo):
        return preambulo
    for path in reversed(list_backups_local(doc_id)):
        try:
            texto = path.read_text(encoding="utf-8")
        except OSError:
            continue
        _, cand, _, cuerpo = partir_markdown(texto, "")
        if preambulo_completo(cand):
            return cand
        if cuerpo and preambulo_completo(cuerpo):
            return cuerpo
    return preambulo


def sin_version(texto: str) -> str:
    return re.sub(
        r"\*\*Versión del documento:\*\*\s*[0-9.]+",
        "**Versión del documento:**",
        texto,
    )


def bump_preambulo(texto: str) -> str:
    def _sub(match):
        piezas = match.group(1).split(".")
        piezas[-1] = str(int(piezas[-1]) + 1)
        return f"**Versión del documento:** {'.'.join(piezas)}"

    nuevo, n = re.subn(
        r"\*\*Versión del documento:\*\*\s*([0-9.]+)",
        _sub,
        texto,
        count=1,
    )
    return nuevo if n else texto
