"""Sello SHA-256 del propio manifiesto de integridad."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_fichero(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sello_path(json_path: Path) -> Path:
    return json_path.with_name(json_path.name + ".sha256")


def escribir_sello(json_path: Path) -> Path:
    dest = sello_path(json_path)
    dest.write_text(sha256_fichero(json_path) + "\n", encoding="utf-8")
    return dest


def comprobar_sello(json_path: Path) -> str | None:
    dest = sello_path(json_path)
    if not json_path.is_file():
        return f"falta manifiesto {json_path}"
    if not dest.is_file():
        return f"falta sello {dest.name}"
    esperado = dest.read_text(encoding="utf-8").strip().lower()
    real = sha256_fichero(json_path)
    if real != esperado:
        return f"sello roto {json_path.name} esperado={esperado} real={real}"
    return None