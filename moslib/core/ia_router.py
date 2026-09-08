"""
moslib.core.ia_router
Fachada de modelos. Política en disco; la IA no la escribe.
Proveedores: jan, gpt4all (locales), grok, openrouter (remotos).
Jan: 127.0.0.1 y, si falta, barrido de /24 privadas en puerto 1337 con cache.
Claves solo en variables de entorno, nunca en git.
"""

from __future__ import annotations

import json
import os
import socket
import threading
from datetime import datetime, timezone
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
JAN_PORT = 1337
CACHE_TTL_SEC = 600


def policy_path() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d / "ia_router.json"


def _jan_cache_path() -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d / "ia_jan_cache.json"


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


def _load_jan_cache() -> dict | None:
    path = _jan_cache_path()
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or not data.get("url"):
        return None
    try:
        ts = datetime.fromisoformat(data["cuando"])
    except Exception:
        return None
    edad = (datetime.now(timezone.utc) - ts).total_seconds()
    if edad > CACHE_TTL_SEC:
        return None
    return data


def _save_jan_cache(url: str, origen: str) -> None:
    payload = {
        "url": url,
        "origen": origen,
        "cuando": datetime.now(timezone.utc).isoformat(),
    }
    _jan_cache_path().write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _local_ipv4() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            found.add(info[4][0])
    except Exception:
        pass
    return [ip for ip in found if not ip.startswith("127.")]


def _es_privada(ip: str) -> bool:
    try:
        parts = [int(x) for x in ip.split(".")]
    except ValueError:
        return False
    if parts[0] == 10:
        return True
    if parts[0] == 192 and parts[1] == 168:
        return True
    if parts[0] == 172 and 16 <= parts[1] <= 31:
        return True
    return False


def _hosts_lan() -> list[str]:
    hosts = []
    vistos = set()
    for ip in _local_ipv4():
        if not _es_privada(ip):
            continue
        prefijo = ".".join(ip.split(".")[:3])
        for n in range(1, 255):
            h = f"{prefijo}.{n}"
            if h not in vistos:
                vistos.add(h)
                hosts.append(h)
    return hosts


def _puerto_abierto(ip: str, port: int, timeout: float = 0.12) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((ip, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def _escanear_jan_lan() -> str | None:
    encontrados: list[str] = []
    lock = threading.Lock()

    def prueba(ip: str) -> None:
        if not _puerto_abierto(ip, JAN_PORT):
            return
        url = f"http://{ip}:{JAN_PORT}/v1/chat/completions"
        ok, _ = _probe_http(url)
        if ok:
            with lock:
                encontrados.append(url)

    hilos = []
    for ip in _hosts_lan():
        t = threading.Thread(target=prueba, args=(ip,), daemon=True)
        hilos.append(t)
        t.start()
        if len(hilos) >= 64:
            for h in hilos:
                h.join()
            hilos = []
    for h in hilos:
        h.join()
    return encontrados[0] if encontrados else None


def resolver_jan_url(policy: dict) -> tuple[str, str]:
    configurada = policy.get("jan_url") or DEFAULT_POLICY["jan_url"]
    ok, motivo = _probe_http(configurada)
    if ok:
        return configurada, f"local o configurada: {motivo}"
    cache = _load_jan_cache()
    if cache:
        ok, motivo = _probe_http(cache["url"])
        if ok:
            return cache["url"], f"cache: {motivo}"
    lan = _escanear_jan_lan()
    if lan:
        _save_jan_cache(lan, "lan")
        return lan, f"encontrada en LAN: {lan}"
    return configurada, "no hay Jan en localhost ni en la LAN visible"


def detectar() -> list[dict]:
    p = load_policy()
    url, motivo = resolver_jan_url(p)
    ok = "no hay Jan" not in motivo
    out = [
        {
            "id": "jan",
            "tipo": "local",
            "disponible": ok,
            "motivo": motivo,
            "url": url,
        }
    ]
    okg, motivog = _probe_http(p.get("gpt4all_url") or DEFAULT_POLICY["gpt4all_url"])
    out.append({"id": "gpt4all", "tipo": "local", "disponible": okg, "motivo": motivog})
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
        url, _ = resolver_jan_url(p)
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
        if not os.environ.get(ENV_KEY["grok"]):
            return False, f"Falta {ENV_KEY['grok']}."
        return _complete_openai(
            prompt,
            p.get("grok_url") or DEFAULT_POLICY["grok_url"],
            p.get("grok_model") or "grok-3",
            "Grok",
            "grok",
        )

    if provider == "openrouter":
        if not os.environ.get(ENV_KEY["openrouter"]):
            return False, f"Falta {ENV_KEY['openrouter']}."
        return _complete_openai(
            prompt,
            p.get("openrouter_url") or DEFAULT_POLICY["openrouter_url"],
            p.get("openrouter_model") or "openrouter/auto",
            "OpenRouter",
            "openrouter",
        )

    return False, f"Proveedor '{provider}' desconocido."