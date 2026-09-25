"""Rutas de tupla = id con barras."""

from __future__ import annotations

from pathlib import Path

from moslib.core.docgen_index import get_docgen_dir


def tuplas_root() -> Path:
    dest = get_docgen_dir() / "tuplas"
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def normalizar_id(ident: str) -> str:
    texto = (ident or "").strip().strip("/")
    if not texto or ".." in texto:
        raise ValueError(f"id inválido: {ident}")
    partes = texto.split("/")
    for parte in partes:
        if not parte or not all(c.isalnum() or c in "-_." for c in parte):
            raise ValueError(f"id inválido: {ident}")
    return "/".join(partes)


def tupla_path(ident: str) -> Path:
    ident = normalizar_id(ident)
    dest = tuplas_root().joinpath(*ident.split("/"))
    return dest.with_suffix(".json")
