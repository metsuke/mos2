"""Almacén cifrado de claves IA en el espacio de usuario."""

from __future__ import annotations

import json
import os
from pathlib import Path

from moslib.core.secreto import leer_wrap
from moslib.core.user import ensure_user_space, get_user_mos_dir


def _dir() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _base() -> Path:
    try:
        from moslib.core import ia_keys as K
        fn = getattr(K, "_dir", None)
        if callable(fn):
            return fn()
    except Exception:
        pass
    return _dir()


def wrap_path() -> Path:
    return _base() / ".ia_wrap"


def keys_path() -> Path:
    return _base() / "ia_keys.json"


def _chmod_privado(path: Path) -> None:
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def wrap_bytes() -> bytes:
    return leer_wrap(wrap_path())


def load_store() -> dict:
    path = keys_path()
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_store(data: dict) -> None:
    path = keys_path()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    _chmod_privado(path)
    _chmod_privado(wrap_path())
