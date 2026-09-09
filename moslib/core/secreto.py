"""
moslib.core.secreto
Envoltorio local de secretos (stdlib).
No es un HSM. Detecta manipulación. El wrap no sale del .mos.
"""

from __future__ import annotations

import hmac
import os
from hashlib import pbkdf2_hmac, sha256
from pathlib import Path

VERSION = b"MOS1"
ITER = 120000


def crear_wrap(path: Path) -> bytes:
    secret = os.urandom(32)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(secret)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return secret


def leer_wrap(path: Path) -> bytes:
    if not path.is_file():
        return crear_wrap(path)
    data = path.read_bytes()
    if len(data) < 32:
        return crear_wrap(path)
    return data[:32]


def _claves(wrap: bytes, n: int) -> tuple[bytes, bytes]:
    material = pbkdf2_hmac("sha256", wrap, b"metsuos-secreto-v1", ITER, dklen=n + 32)
    return material[:n], material[n:]


def envolver(claro: bytes, wrap: bytes) -> bytes:
    flujo, mac_key = _claves(wrap, len(claro))
    cuerpo = bytes(a ^ b for a, b in zip(claro, flujo))
    tag = hmac.new(mac_key, VERSION + cuerpo, sha256).digest()
    return VERSION + tag + cuerpo


def desenvolver(blob: bytes, wrap: bytes) -> bytes:
    if len(blob) < 4 + 32 or blob[:4] != VERSION:
        raise ValueError("secreto: formato no válido")
    tag = blob[4:36]
    cuerpo = blob[36:]
    flujo, mac_key = _claves(wrap, len(cuerpo))
    esperado = hmac.new(mac_key, VERSION + cuerpo, sha256).digest()
    if not hmac.compare_digest(tag, esperado):
        raise ValueError("secreto: integridad fallida")
    return bytes(a ^ b for a, b in zip(cuerpo, flujo))