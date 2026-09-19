"""Claves en .mos, envueltas con secreto. Env se copia al almacén."""

from __future__ import annotations

import base64
import os
from pathlib import Path

from moslib.core.secreto import desenvolver, envolver
from moslib.core import ia_keys_store as _S

ENV_KEY = {
    "grok": "XAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "jan": "JAN_API_KEY",
    "gpt4all": "GPT4ALL_API_KEY",
}

keys_path = _S.keys_path
wrap_path = _S.wrap_path
load_store = _S.load_store
save_store = _S.save_store
wrap_bytes = _S.wrap_bytes
_load_store = _S.load_store
_save_store = _S.save_store
_wrap_bytes = _S.wrap_bytes


def _dir() -> Path:
    return _S._dir()


def save_key(provider: str, raw: str) -> tuple[bool, str]:
    pid = provider.lower().strip()
    if pid not in ENV_KEY:
        return False, f"Proveedor desconocido: {pid}"
    texto = raw.strip()
    if not texto:
        return False, "La clave no puede estar vacía."
    blob = envolver(texto.encode("utf-8"), wrap_bytes())
    store = load_store()
    store[pid] = base64.b64encode(blob).decode("ascii")
    save_store(store)
    return True, f"Clave de {pid} guardada en el espacio de usuario."


def delete_key(provider: str) -> tuple[bool, str]:
    pid = provider.lower().strip()
    store = load_store()
    if pid not in store:
        return False, f"No hay clave guardada para {pid}."
    del store[pid]
    save_store(store)
    return True, f"Clave de {pid} eliminada."


def load_key(provider: str) -> str | None:
    pid = provider.lower().strip()
    token = load_store().get(pid)
    if not token:
        return None
    try:
        blob = base64.b64decode(str(token).encode("ascii"))
        return desenvolver(blob, wrap_bytes()).decode("utf-8")
    except Exception:
        return None


def ingest_env() -> list[str]:
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
