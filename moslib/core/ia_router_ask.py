"""detectar, status, set_provider y complete."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from moslib.core.ia_router_detect import (
    modelo_activo,
    resolver_gpt4all_url,
    resolver_jan_url,
    url_chat,
)
from moslib.core.ia_router_http import auth_headers
from moslib.core.ia_router_policy import PLACEHOLDER_MODELS, PROVIDERS, campo_modelo, load_policy, save_policy


def set_provider(name: str):
    from moslib.core import ia_router as R

    name = name.lower().strip()
    if name not in PROVIDERS:
        return False, f"Proveedor desconocido: {name}. Usa: {', '.join(PROVIDERS)}"
    if name in ("grok", "openrouter"):
        R.ia_keys.ingest_env()
        if not R.ia_keys.has_any_key(name):
            return False, f"No hay clave para {name}. Usa: iarouter clave {name}"
    avail = {d["id"]: d for d in R.detectar()}
    if not avail[name]["disponible"]:
        return False, f"{name} no está disponible: {avail[name]['motivo']}"
    save_policy({"provider": name, "enabled": True})
    return True, f"Proveedor activo: {name} (enabled=true)"


def detectar() -> list[dict]:
    from moslib.core import ia_router as R

    R.ia_keys.ingest_env()
    p = load_policy()
    url, motivo = resolver_jan_url(p)
    out = [{"id": "jan", "tipo": "local", "disponible": "no hay Jan" not in motivo, "motivo": motivo, "url": url}]
    urlg, motivog = resolver_gpt4all_url(p)
    out.append({"id": "gpt4all", "tipo": "local", "disponible": "no hay GPT4All" not in motivog, "motivo": motivog, "url": urlg})
    for pid in ("grok", "openrouter"):
        if R.ia_keys.has_any_key(pid):
            origen = "almacén .mos" if R.ia_keys.has_stored_key(pid) else "entorno (ingerido)"
            out.append({"id": pid, "tipo": "remoto", "disponible": True, "motivo": f"clave presente ({origen})"})
        else:
            out.append({"id": pid, "tipo": "remoto", "disponible": False, "motivo": f"falta clave; iarouter clave {pid}"})
    return out


def status() -> dict:
    p = load_policy()
    return {
        "provider": p["provider"],
        "enabled": bool(p["enabled"]),
        "motivo": "" if p["enabled"] else "política enabled=false",
        "providers": list(PROVIDERS),
        "modelo": modelo_activo(),
        "disponibles": detectar(),
        "jan_url": p.get("jan_url"),
        "gpt4all_url": p.get("gpt4all_url"),
    }


def _mentions_mos(text: str, allow: list) -> bool:
    if ".mos" not in text:
        return False
    return not any(allowed and allowed in text for allowed in allow)


def complete_openai(prompt: str, url: str, model: str, etiqueta: str, provider: str):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = Request(url, data=body, method="POST", headers=auth_headers(provider))
    try:
        with urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return True, json.loads(raw)["choices"][0]["message"]["content"]
    except HTTPError as exc:
        return False, f"{etiqueta} HTTP {exc.code} url={url}"
    except URLError as exc:
        return False, f"{etiqueta} no alcanzable ({url}): {exc.reason}"
    except Exception as exc:
        return False, f"Error {etiqueta}: {exc}"


def complete(prompt: str, meta: dict | None = None):
    from moslib.core import ia_router as R

    meta = meta or {}
    p = load_policy()
    if not p.get("enabled"):
        return False, "Enrutador desactivado (enabled=false). No hay llamada de red."
    blob = prompt + json.dumps(meta, ensure_ascii=False)
    if _mentions_mos(blob, list(p.get("allow_mos_paths") or [])):
        return False, "El payload menciona .mos y no está en allow_mos_paths."
    provider = (meta.get("provider") or p.get("provider") or "jan").lower()
    if provider not in PROVIDERS:
        return False, f"Proveedor '{provider}' desconocido."
    if provider in ("grok", "openrouter") and not R.ia_keys.has_any_key(provider):
        return False, f"Falta clave de {provider}."
    url = url_chat(provider, p)
    model = p.get(campo_modelo(provider)) or "auto"
    if model in PLACEHOLDER_MODELS:
        ids, raw_models = R._listar_modelos(url, provider)
        model = ids[0] if ids else model
        if model in PLACEHOLDER_MODELS:
            return False, f"{provider} no listó modelos: {raw_models}"
    etiqueta = {"jan": "Jan", "gpt4all": "GPT4All", "grok": "Grok", "openrouter": "OpenRouter"}[provider]
    return R._complete_openai(prompt, url, model, etiqueta, provider)