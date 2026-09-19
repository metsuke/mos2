"""Backup y escritura de documentos docgen."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from moslib.core.docgen_hash import registrar_destino
from moslib.core.docgen_index import ensure_docgen_dirs, get_backup_dir, resolve_path
from moslib.core.docgen_md import (
    bump_preambulo,
    partir_markdown,
    recuperar_preambulo,
    sin_version,
)

MAX_BACKUPS = 8


def backup_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def list_backups(doc_id: str) -> list[Path]:
    folder = get_backup_dir() / doc_id
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_file())


def podar_backups(doc_id: str, keep: int = MAX_BACKUPS) -> None:
    files = list_backups(doc_id)
    extra = files[:-keep] if keep else files
    for path in extra:
        try:
            path.unlink()
        except OSError:
            pass


def backup_document(doc_id: str) -> Path | None:
    src = resolve_path(doc_id)
    if src is None or not src.is_file():
        return None
    ensure_docgen_dirs()
    dest_dir = get_backup_dir() / doc_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{backup_stamp()}{src.suffix or '.md'}"
    shutil.copy2(src, dest)
    podar_backups(doc_id)
    return dest


def mejor_origen(doc_id: str, fallback: Path | None) -> Path:
    candidatos = []
    if fallback is not None and fallback.is_file():
        candidatos.append(fallback)
    candidatos.extend(list_backups(doc_id))
    if not candidatos:
        raise FileNotFoundError(f"no hay origen para {doc_id}")
    return max(candidatos, key=lambda p: p.stat().st_size)


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
    registrar_destino(dest)
    return dest
