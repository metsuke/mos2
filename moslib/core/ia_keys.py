"""
moslib.core.ia_keys
Claves en el espacio de usuario, envueltas con moslib.core.secreto.
Si hay variable de entorno y no hay clave en .mos, se copia al almacén.
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path

from moslib.core.secreto import desenvolver, envolver, leer_wrap
from moslib.core.user import ensure_user_space, get_user_mos_dir

ENV_KEY = {
    "grok": "XAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "jan": "JAN_API_KEY",
    "gpt4all": "GPT4ALL_API_KEY",
}


def _dir() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d


def wrap_path() -> Path:
    return _dir() / ".ia_wrap"


def keys_path() -> Path:
    return _dir() / "ia_keys.json"


def _chmod_private(path: Path) -> None:
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def _wrap_bytes() -> bytes:
    return leer_wrap(wrap_path())


def _load_store() -> dict:
    path = keys_path()
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_store(data: dict) -> None:
    path = keys_path()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    _chmod_private(path)
    _chmod_private(wrap_path())


def save_key(provider: str, raw: str) -> tuple[bool, str]:
    pid = provider.lower().strip()
    if pid not in ENV_KEY:
        return False, f"Proveedor desconocido: {pid}"
    texto = raw.strip()
    if not texto:
        return False, "La clave no puede estar vacía."
    blob = envolver(texto.encode("utf-8"), _wrap_bytes())
    store = _load_store()
    store[pid] = base64.b64encode(blob).decode("ascii")
    _save_store(store)
    return True, f"Clave de {pid} guardada en el espacio de usuario."


def delete_key(provider: str) -> tuple[bool, str]:
    pid = provider.lower().strip()
    store = _load_store()
    if pid not in store:
        return False, f"No hay clave guardada para {pid}."
    del store[pid]
    _save_store(store)
    return True, f"Clave de {pid} eliminada."


def load_key(provider: str) -> str | None:
    pid = provider.lower().strip()
    token = _load_store().get(pid)
    if not token:
        return None
    try:
        blob = base64.b64decode(str(token).encode("ascii"))
        return desenvolver(blob, _wrap_bytes()).decode("utf-8")
    except Exception:
        return None


def ingest_env() -> list[str]:
    """Copia al .mos las claves que estén en el entorno y aún no guardadas."""
    hechos = []
    for pid, env in ENV_KEY.items():
        if load_key(pid):
            continue
        val = os.environ.get(env)
        if val and val.strip():
            ok, _ = save_key(pid, val)
            if ok:
                hechos.append(pid)
    return hechos


def resolve_key(provider: str) -> str | None:
    ingest_env()
    stored = load_key(provider)
    if stored:
        return stored
    env = ENV_KEY.get(provider.lower().strip())
    if env:
        val = os.environ.get(env)
        if val:
            save_key(provider, val)
            return val.strip()
    return None


def has_stored_key(provider: str) -> bool:
    return load_key(provider) is not None


def has_any_key(provider: str) -> bool:
    return resolve_key(provider) is not None