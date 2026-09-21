"""Escritura con hash: b64/b85 + gzip/lzma. Solo via multi."""

from __future__ import annotations

import base64
import gzip
import lzma
import time
from pathlib import Path

from moslib.core.hostfs import project_root, resolver
from moslib.core.integridad import registrar, sha256_bytes
from moslib.core.user import ensure_user_space, get_username, get_user_mos_dir

PERMISO_MULTI = False
BORDE = "─" * 52
PREFS = ("xzb85:", "gzb85:", "b85:", "xz:", "gz:")


def _tmp_dir() -> Path:
    d = get_user_mos_dir(get_username()) / "tmp" / "write"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _preview(datos: bytes) -> str:
    texto = datos.decode("utf-8", errors="replace").splitlines()
    return (
        f"{BORDE}\n" + "\n".join(texto[:3]) + f"\n{BORDE}\n…\n{BORDE}\n"
        + "\n".join(texto[-3:]) + f"\n{BORDE}"
    )


def _decodificar(bruto: str) -> bytes:
    s = bruto.strip()
    pref = next((p for p in PREFS if s.startswith(p)), "")
    s = s[(len(pref)):] if pref else s
    if pref.endswith("b85:"):
        crudo = base64.a85decode(s)
    else:
        crudo = base64.b64decode(s, validate=True)
    if pref.startswith("gz"):
        return gzip.decompress(crudo)
    if pref.startswith("xz"):
        return lzma.decompress(crudo)
    return crudo


def aplicar(rel: str, lineas: list[str]) -> tuple[bool, str]:
    if not PERMISO_MULTI:
        return False, "write solo se usa en multi"
    if not lineas:
        return False, "falta hash esperado y payload"
    esperado = lineas[0].strip().lower().replace("sha256:", "").replace("esperado:", "").strip()
    if len(esperado) != 64 or any(c not in "0123456789abcdef" for c in esperado):
        return False, "la primera linea debe ser el sha256 hex"
    payload = "".join(x.strip() for x in lineas[1:] if x.strip() and x.strip() != ".")
    try:
        datos = _decodificar(payload)
    except Exception as exc:
        return False, f"payload invalido: {exc}"
    real = sha256_bytes(datos)
    if real != esperado:
        return False, f"NO COINCIDE esperado={esperado} real={real}"
    dest = resolver(rel)
    root = project_root()
    dest.relative_to(root)
    ensure_user_space(get_username())
    bak = None
    existia = dest.is_file()
    if existia:
        bak = _tmp_dir() / f"{int(time.time())}-{dest.name}"
        bak.write_bytes(dest.read_bytes())
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(datos)
        registrar(dest.relative_to(root).as_posix(), real)
    except Exception as exc:
        if bak is not None and bak.is_file():
            dest.write_bytes(bak.read_bytes())
        elif dest.is_file() and not existia:
            dest.unlink()
        return False, f"escritura fallida, restaurado: {exc}"
    if bak is not None:
        bak.unlink( missing_ok=True)
    return True, f"OK {real}\n{_preview(datos)}"
