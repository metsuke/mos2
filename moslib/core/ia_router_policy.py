"""Política en disco de ia_router. La IA no la escribe."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.user import ensure_user_space, get_user_mos_dir

DEFAULT_POLICY = {
    "enabled": False,
    "provider": "jan",
    "cost_ceiling": None,
    "project": None,
    "allow_mos_paths": [],
    "jan_url": "http://127.0.0.1:1337/v1/chat/completions",
    "jan_model": "auto",
    "gpt4all_url": "http://127.0.0.1:4891/v1/chat/completions",
    "gpt4all_model": "auto",
    "grok_url": "https://api.x.ai/v1/chat/completions",
    "grok_model": "auto",
    "openrouter_url": "https://openrouter.ai/api/v1/chat/completions",
    "openrouter_model": "auto",
}
PROVIDERS = ("jan", "gpt4all", "grok", "openrouter")
PLACEHOLDER_MODELS = {"", "auto", "jan", "gpt4all"}
JAN_PORT = 1337
GPT4ALL_PORT = 4891
PUENTE_PORT = 17337
CACHE_TTL_SEC = 600


def policy_path() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d / "ia_router.json"


def cache_path(nombre: str) -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d / nombre


def campo_modelo(provider: str) -> str:
    return {
        "jan": "jan_model",
        "gpt4all": "gpt4all_model",
        "grok": "grok_model",
        "openrouter": "openrouter_model",
    }[provider]


def load_policy() -> dict:
    from moslib.core import ia_router as R

    path = R.policy_path()
    out = dict(DEFAULT_POLICY)
    if not path.is_file():
        return out
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return out
    if isinstance(data, dict):
        out.update({k: data[k] for k in DEFAULT_POLICY if k in data})
    return out


def save_policy(policy: dict) -> None:
    from moslib.core import ia_router as R

    merged = load_policy()
    merged.update(policy)
    if merged.get("provider") not in PROVIDERS:
        raise ValueError("proveedor no válido")
    R.policy_path().write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def set_destino(provider: str, url: str) -> tuple[bool, str]:
    pid = provider.lower().strip()
    campo = {"jan": "jan_url", "gpt4all": "gpt4all_url"}.get(pid)
    if not campo:
        return False, f"No se puede fijar URL de {pid}."
    u = url.strip()
    if not u.startswith("http://") and not u.startswith("https://"):
        return False, "La URL debe ser http(s)."
    if not u.rstrip("/").endswith("chat/completions"):
        u = u.rstrip("/") + "/chat/completions"
    save_policy({campo: u})
    return True, f"{campo} = {u}"