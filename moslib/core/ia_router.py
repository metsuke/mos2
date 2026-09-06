"""
moslib.core.ia_router
Fachada de modelos. Política en disco; la IA no la escribe.
Locales C6: Jan y GPT4All (HTTP OpenAI-compatible).
Grok y OpenRouter: C7.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from moslib.core.user import ensure_user_space, get_user_mos_dir

DEFAULT_POLICY = {
    "enabled": False,
    "provider": "jan",
    "cost_ceiling": None,
    "project": None,
    "allow_mos_paths": [],
    "jan_url": "http://127.0.0.1:1337/v1/chat/completions",
    "jan_model": "jan",
    "gpt4all_url": "http://127.0.0.1:4891/v1/chat/completions",
    "gpt4all_model": "gpt4all",
}

LOCAL_PROVIDERS = ("jan", "gpt4all")


def policy_path() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d / "ia_router.json"


def load_policy() -> dict:
    path = policy_path()
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
        "providers": list(LOCAL_PROVIDERS),
        "jan_url": p.get("jan_url"),
        "gpt4all_url": p.get("gpt4all_url"),
    }


def _complete_openai_local(prompt: str, url: str, model: str, etiqueta: str) -> tuple[bool, str]:
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")
    req = Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        return False, f"{etiqueta} HTTP {exc.code}: {exc.reason}"
    except URLError as exc:
        return False, f"{etiqueta} no alcanzable ({url}): {exc.reason}"
    except Exception as exc:
        return False, f"Error {etiqueta}: {exc}"
    try:
        data = json.loads(raw)
        text = data["choices"][0]["message"]["content"]
        return True, text
    except (KeyError, IndexError, json.JSONDecodeError):
        return False, f"Respuesta {etiqueta} no válida: {raw[:300]}"


def complete(prompt: str, meta: dict | None = None) -> tuple[bool, str]:
    meta = meta or {}
    p = load_policy()
    if not p.get("enabled"):
        return False, "Enrutador desactivado (enabled=false). No hay llamada de red."
    blob = prompt + json.dumps(meta, ensure_ascii=False)
    if _mentions_mos(blob, list(p.get("allow_mos_paths") or [])):
        return False, "El payload menciona .mos y no está en allow_mos_paths."
    provider = (meta.get("provider") or p.get("provider") or "jan").lower()
    if provider == "jan":
        return _complete_openai_local(
            prompt,
            p.get("jan_url") or DEFAULT_POLICY["jan_url"],
            p.get("jan_model") or "jan",
            "Jan",
        )
    if provider == "gpt4all":
        return _complete_openai_local(
            prompt,
            p.get("gpt4all_url") or DEFAULT_POLICY["gpt4all_url"],
            p.get("gpt4all_model") or "gpt4all",
            "GPT4All",
        )
    return False, f"Proveedor '{provider}' no implementado aún (C6: jan, gpt4all)."