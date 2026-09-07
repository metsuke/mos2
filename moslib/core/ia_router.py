"""
moslib.core.ia_router
Fachada de modelos. Política en disco; la IA no la escribe.
Proveedores: jan, gpt4all (locales), grok, openrouter (remotos).
Claves solo en variables de entorno, nunca en git.
"""

from __future__ import annotations

import json
import os
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
    "jan_model": "auto",
    "gpt4all_url": "http://127.0.0.1:4891/v1/chat/completions",
    "gpt4all_model": "auto",
    "grok_url": "https://api.x.ai/v1/chat/completions",
    "grok_model": "grok-3",
    "openrouter_url": "https://openrouter.ai/api/v1/chat/completions",
    "openrouter_model": "openrouter/auto",
}

PROVIDERS = ("jan", "gpt4all", "grok", "openrouter")
ENV_KEY = {
    "grok": "XAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "jan": "JAN_API_KEY",
    "gpt4all": "GPT4ALL_API_KEY",
}
PLACEHOLDER_MODELS = {"", "auto", "jan", "gpt4all"}


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
    merged = load_policy()
    merged.update(policy)
    if merged.get("provider") not in PROVIDERS:
        raise ValueError("proveedor no válido")
    policy_path().write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def set_provider(name: str) -> tuple[bool, str]:
    name = name.lower().strip()
    if name not in PROVIDERS:
        return False, f"Proveedor desconocido: {name}. Usa: {', '.join(PROVIDERS)}"
    avail = {d["id"]: d for d in detectar()}
    if not avail[name]["disponible"]:
        return False, f"{name} no está disponible: {avail[name]['motivo']}"
    save_policy({"provider": name, "enabled": True})
    return True, f"Proveedor activo: {name} (enabled=true)"


def _mentions_mos(text: str, allow: list) -> bool:
    if ".mos" not in text:
        return False
    for allowed in allow:
        if allowed and allowed in text:
            return False
    return True


def _models_url(chat_url: str) -> str:
    base = chat_url.rstrip("/")
    if base.endswith("chat/completions"):
        return base[: -len("chat/completions")] + "models"
    if base.endswith("/v1"):
        return base + "/models"
    return base + "/models"


def _root_v1(chat_url: str) -> str:
    base = chat_url.rstrip("/")
    if base.endswith("chat/completions"):
        return base[: -len("/chat/completions")]
    if base.endswith("/v1"):
        return base
    return base


def _auth_headers(provider: str) -> dict:
    headers = {"Content-Type": "application/json"}
    env = ENV_KEY.get(provider)
    key = os.environ.get(env) if env else None
    if key:
        headers["Authorization"] = f"Bearer {key}"
    return headers


def _listar_modelos(chat_url: str, provider: str) -> tuple[list[str], str]:
    url = _models_url(chat_url)
    req = Request(url, method="GET", headers=_auth_headers(provider))
    try:
        with urlopen(req, timeout=5) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        try:
            detalle = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            detalle = str(exc.reason)
        return [], f"GET {url} HTTP {exc.code}: {detalle}"
    except Exception as exc:
        return [], f"GET {url}: {exc}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return [], f"GET {url} no es JSON: {raw[:200]}"
    items = data.get("data")
    if items is None and isinstance(data, list):
        items = data
    ids = []
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("id"):
                ids.append(str(item["id"]))
            elif isinstance(item, str):
                ids.append(item)
    return ids, raw[:300]


def _primer_modelo(chat_url: str, provider: str) -> str | None:
    ids, _ = _listar_modelos(chat_url, provider)
    return ids[0] if ids else None


def _probe_http(url: str) -> tuple[bool, str]:
    root = _root_v1(url)
    candidatos = [root, root + "/models", root + "/chat/completions"]
    visto = []
    for target in candidatos:
        req = Request(target, method="GET")
        try:
            with urlopen(req, timeout=3) as resp:
                resp.read(64)
            return True, f"responde {target}"
        except HTTPError as exc:
            if exc.code in (400, 401, 404, 405, 422):
                return True, f"responde {target} (HTTP {exc.code})"
            visto.append(f"{target} HTTP {exc.code}")
        except URLError as exc:
            visto.append(f"{target} {exc.reason}")
        except Exception as exc:
            visto.append(f"{target} {exc}")
    return False, "; ".join(visto)


def detectar() -> list[dict]:
    p = load_policy()
    out = []
    ok, motivo = _probe_http(p.get("jan_url") or DEFAULT_POLICY["jan_url"])
    out.append({"id": "jan", "tipo": "local", "disponible": ok, "motivo": motivo})
    ok, motivo = _probe_http(p.get("gpt4all_url") or DEFAULT_POLICY["gpt4all_url"])
    out.append({"id": "gpt4all", "tipo": "local", "disponible": ok, "motivo": motivo})
    for pid in ("grok", "openrouter"):
        env = ENV_KEY[pid]
        if os.environ.get(env):
            out.append(
                {
                    "id": pid,
                    "tipo": "remoto",
                    "disponible": True,
                    "motivo": f"variable {env} presente",
                }
            )
        else:
            out.append(
                {
                    "id": pid,
                    "tipo": "remoto",
                    "disponible": False,
                    "motivo": f"falta variable {env}",
                }
            )
    return out


def status() -> dict:
    p = load_policy()
    return {
        "provider": p["provider"],
        "enabled": bool(p["enabled"]),
        "motivo": "" if p["enabled"] else "política enabled=false",
        "providers": list(PROVIDERS),
        "disponibles": detectar(),
        "jan_url": p.get("jan_url"),
        "gpt4all_url": p.get("gpt4all_url"),
    }


def _complete_openai(
    prompt: str,
    url: str,
    model: str,
    etiqueta: str,
    provider: str,
) -> tuple[bool, str]:
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")
    req = Request(url, data=body, method="POST", headers=_auth_headers(provider))
    try:
        with urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        try:
            detalle = exc.read().decode("utf-8", errors="replace")[:400]
        except Exception:
            detalle = str(exc.reason)
        return False, f"{etiqueta} HTTP {exc.code} model={model} url={url} {detalle}"
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
        url = p.get("jan_url") or DEFAULT_POLICY["jan_url"]
        model = p.get("jan_model") or "auto"
        ids, raw_models = _listar_modelos(url, "jan")
        if model in PLACEHOLDER_MODELS:
            model = ids[0] if ids else model
        if model in PLACEHOLDER_MODELS:
            return False, f"Jan no listó modelos. /v1/models: {raw_models}"
        return _complete_openai(prompt, url, model, "Jan", "jan")

    if provider == "gpt4all":
        url = p.get("gpt4all_url") or DEFAULT_POLICY["gpt4all_url"]
        model = p.get("gpt4all_model") or "auto"
        ids, raw_models = _listar_modelos(url, "gpt4all")
        if model in PLACEHOLDER_MODELS:
            model = ids[0] if ids else model
        if model in PLACEHOLDER_MODELS:
            return False, f"GPT4All no listó modelos. /v1/models: {raw_models}"
        return _complete_openai(prompt, url, model, "GPT4All", "gpt4all")

    if provider == "grok":
        key = os.environ.get(ENV_KEY["grok"])
        if not key:
            return False, f"Falta {ENV_KEY['grok']}."
        return _complete_openai(
            prompt,
            p.get("grok_url") or DEFAULT_POLICY["grok_url"],
            p.get("grok_model") or "grok-3",
            "Grok",
            "grok",
        )

    if provider == "openrouter":
        key = os.environ.get(ENV_KEY["openrouter"])
        if not key:
            return False, f"Falta {ENV_KEY['openrouter']}."
        return _complete_openai(
            prompt,
            p.get("openrouter_url") or DEFAULT_POLICY["openrouter_url"],
            p.get("openrouter_model") or "openrouter/auto",
            "OpenRouter",
            "openrouter",
        )

    return False, f"Proveedor '{provider}' desconocido."