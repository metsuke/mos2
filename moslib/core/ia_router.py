"""
moslib.core.ia_router
Fachada de llamadas a modelos. Política en disco; la IA no la escribe.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from moslib.core.user import ensure_user_space, get_user_mos_dir

DEFAULT_POLICY = {
    "enabled": False,
    "provider": "grok",
    "cost_ceiling": None,
    "project": None,
    "allow_mos_paths": [],
}


def policy_path() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d / "ia_router.json"


def load_policy() -> dict:
    path = policy_path()
    if not path.is_file():
        return dict(DEFAULT_POLICY)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT_POLICY)
    out = dict(DEFAULT_POLICY)
    if isinstance(data, dict):
        out.update({k: data[k] for k in DEFAULT_POLICY if k in data})
    return out


def save_policy(policy: dict) -> None:
    merged = dict(DEFAULT_POLICY)
    merged.update(policy)
    policy_path().write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _mentions_mos(text: str, allow: list) -> bool:
    if ".mos" not in text:
        return False
    for allowed in allow:
        if allowed and allowed in text:
            return False
    return True


def status() -> dict:
    p = load_policy()
    return {
        "provider": p["provider"],
        "enabled": bool(p["enabled"]),
        "motivo": "" if p["enabled"] else "política enabled=false",
        "providers": [p["provider"]],
    }


def complete(prompt: str, meta: dict | None = None) -> tuple[bool, str]:
    meta = meta or {}
    p = load_policy()
    if not p.get("enabled"):
        return False, "Enrutador desactivado (enabled=false). No hay llamada de red."
    blob = prompt + json.dumps(meta, ensure_ascii=False)
    if _mentions_mos(blob, list(p.get("allow_mos_paths") or [])):
        return False, "El payload menciona .mos y no está en allow_mos_paths."
    endpoint = meta.get("endpoint")
    if not endpoint:
        return False, "enabled=true pero no hay endpoint configurado en meta."
    try:
        req = Request(endpoint, data=prompt.encode("utf-8"), method="POST")
        with urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        return True, body
    except URLError as exc:
        return False, f"Error de red: {exc}"
    except Exception as exc:
        return False, f"Error: {exc}"