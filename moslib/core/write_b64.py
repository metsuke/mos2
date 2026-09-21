"""Escritura Base64/gzip con hash y backup. Solo via multi."""

from __future__ import annotations

import base64
import gzip
import time
from pathlib import Path

from moslib.core.hostfs import project_root, resolver
from moslib.core.integridad import registrar, sha256_bytes
from moslib.core.user import ensure_user_space, get_username, get_user_mos_dir

PERMISO_MULTI = False
BORDE = "─" * 52


def _tmp_dir() -> Path:
    d = get_user_mos_dir(get_username()) / "tmp" / "write"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _preview(datos: bytes) -> str:
    texto = datos.decode("utf-8", errors="replace").splitlines()
    cabeza = "\n".join(texto[:3])
    cola = "\n".join(texto[-3:])
    return f"{BORDE}\n{cabeza}\n{BORDE}\n…\n{BORDE}\n{cola}\n{BORDE}"


def _decodificar(bruto: str) -> bytes:
    s = bruto.strip()
    gz = s.startswith("gz:")
    if gz:
        s = s[3:]
    crudo = base64.b64decode(s, validate=True)
    if gz:
        return gzip.decompress(crudo)
    return crudo


def aplicar(rel: str, lineas: list[str]) -> tuple[bool, str]:
    if not PERMISO_MULTI:
        return False, "write solo se usa en multi"
    if not lineas:
        return False, "falta hash esperado y Base64"
    esperado = lineas[0].strip().lower().replace("sha256:", "").replace("esperado:", "").strip()
    if len(esperado) != 64 or any(c not in "0123456789abcdef" for c in esperado):
        return False, "la primera linea debe ser el sha256 hex"
    b64 = "".join(x.strip() for x in lineas[1:] if x.strip() and x.strip() != ".")
    try:
        datos = _decodificar(b64)
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
        bak.unlink(missing_ok=True)
    return True, f"OK {real}\n{_preview(datos)}"
