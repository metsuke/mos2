"""HTTP de modelos y probe para ia_router."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from moslib.core import ia_keys


def models_url(chat_url: str) -> str:
    base = chat_url.rstrip("/")
    if base.endswith("chat/completions"):
        return base[: -len("chat/completions")] + "models"
    if base.endswith("/v1"):
        return base + "/models"
    return base + "/models"


def root_v1(chat_url: str) -> str:
    base = chat_url.rstrip("/")
    if base.endswith("chat/completions"):
        return base[: -len("/chat/completions")]
    if base.endswith("/v1"):
        return base
    return base


def auth_headers(provider: str) -> dict:
    headers = {"Content-Type": "application/json"}
    key = ia_keys.resolve_key(provider)
    if key:
        headers["Authorization"] = f"Bearer {key}"
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://metsuke.com"
        headers["X-Title"] = "MetsuOS"
    return headers


def listar_modelos_url(chat_url: str, provider: str) -> tuple[list[str], str]:
    url = models_url(chat_url)
    req = Request(url, method="GET", headers=auth_headers(provider))
    try:
        with urlopen(req, timeout=15) as resp:
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


def probe_http(url: str) -> tuple[bool, str]:
    root = root_v1(url)
    candidatos = [root, root + "/models", root + "/chat/completions", root + "/health"]
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