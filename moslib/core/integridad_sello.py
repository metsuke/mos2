"""Sello SHA-256 canónico del manifiesto de integridad."""

from __future__ import annotations

import hashlib
from pathlib import Path


def normalizar_eol(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_canonico_bytes(data: bytes) -> str:
    return hashlib.sha256(normalizar_eol(data)).hexdigest()


def sha256_fichero(path: Path) -> str:
    return sha256_canonico_bytes(path.read_bytes())


def sha256_canonico(path: Path) -> str:
    return sha256_fichero(path)


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
    esperado = dest.read_text(encoding="utf-8").replace("\r", "").strip().lower()
    real = sha256_fichero(json_path)
    if real != esperado:
        return f"sello roto {json_path.name} esperado={esperado} real={real}"
    return None