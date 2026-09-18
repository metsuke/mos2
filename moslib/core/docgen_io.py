"""Backup, corte de markdown y escritura de docgen."""

from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from moslib.core.docgen_index import (
    ensure_docgen_dirs,
    get_backup_dir,
    resolve_path,
)


def backup_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def backup_document(doc_id: str) -> Path | None:
    src = resolve_path(doc_id)
    if src is None or not src.is_file():
        return None
    ensure_docgen_dirs()
    dest_dir = get_backup_dir() / doc_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{backup_stamp()}{src.suffix or '.md'}"
    shutil.copy2(src, dest)
    return dest


def list_backups(doc_id: str) -> list[Path]:
    folder = get_backup_dir() / doc_id
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_file())


def mejor_origen(doc_id: str, fallback: Path | None) -> Path:
    candidatos = []
    if fallback is not None and fallback.is_file():
        candidatos.append(fallback)
    candidatos.extend(list_backups(doc_id))
    if not candidatos:
        raise FileNotFoundError(f"no hay origen para {doc_id}")
    return max(candidatos, key=lambda p: p.stat().st_size)


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
    for path in reversed(list_backups(doc_id)):
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


def ultimo_backup_texto(doc_id: str) -> str | None:
    backups = list_backups(doc_id)
    if not backups:
        return None
    return backups[-1].read_text(encoding="utf-8")


def escribir(doc_id: str, nuevo: str, dest: Path) -> Path:
    from moslib.core.docgen_html import estructurar_listas_de_opciones, escribir_html

    nuevo = estructurar_listas_de_opciones(nuevo)
    anterior = ultimo_backup_texto(doc_id)
    if anterior is None and dest.is_file():
        anterior = dest.read_text(encoding="utf-8")
    if anterior is not None and sin_version(nuevo) != sin_version(anterior):
        nuevo = bump_preambulo(nuevo)
    if dest.is_file():
        if len(nuevo) < max(80, int(len(dest.read_text(encoding="utf-8")) * 0.5)):
            raise RuntimeError(f"docgen aborta: {doc_id} quedaría mucho más corto.")
        backup_document(doc_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(nuevo, encoding="utf-8")
    escribir_html(doc_id, nuevo)
    return dest