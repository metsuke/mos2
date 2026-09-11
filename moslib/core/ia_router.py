"""
moslib.core.ia_router
Fachada de modelos. Política en disco; la IA no la escribe.
Claves: moslib.core.ia_keys.
Jan/GPT4All: localhost, resolv/WSL, ipconfig.exe, pasarela, cache, /24, puente 17337.
"""

from __future__ import annotations

import json
import re
import socket
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from moslib.core import ia_keys
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


def _cache_path(nombre: str) -> Path:
    ensure_user_space()
    d = get_user_mos_dir() / "config"
    d.mkdir(parents=True, exist_ok=True)
    return d / nombre


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
    if name in ("grok", "openrouter"):
        ia_keys.ingest_env()
        if not ia_keys.has_any_key(name):
            return False, (
                f"No hay clave para {name}. "
                f"Usa: iarouter clave {name} "
                f"o define {ia_keys.ENV_KEY[name]} (se copiará a .mos)."
            )
    avail = {d["id"]: d for d in detectar()}
    if not avail[name]["disponible"]:
        return False, f"{name} no está disponible: {avail[name]['motivo']}"
    save_policy({"provider": name, "enabled": True})
    return True, f"Proveedor activo: {name} (enabled=true)"


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


def _campo_modelo(provider: str) -> str:
    return {
        "jan": "jan_model",
        "gpt4all": "gpt4all_model",
        "grok": "grok_model",
        "openrouter": "openrouter_model",
    }[provider]


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
    key = ia_keys.resolve_key(provider)
    if key:
        headers["Authorization"] = f"Bearer {key}"
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://metsuke.com"
        headers["X-Title"] = "MetsuOS"
    return headers


def _listar_modelos(chat_url: str, provider: str) -> tuple[list[str], str]:
    url = _models_url(chat_url)
    req = Request(url, method="GET", headers=_auth_headers(provider))
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


def _probe_http(url: str) -> tuple[bool, str]:
    root = _root_v1(url)
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


def _load_url_cache(nombre: str) -> dict | None:
    path = _cache_path(nombre)
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
    if (datetime.now(timezone.utc) - ts).total_seconds() > CACHE_TTL_SEC:
        return None
    return data


def _save_url_cache(nombre: str, url: str, origen: str) -> None:
    payload = {
        "url": url,
        "origen": origen,
        "cuando": datetime.now(timezone.utc).isoformat(),
    }
    _cache_path(nombre).write_text(
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


def _ips_windows_desde_wsl() -> list[str]:
    candidatos = [
        Path("/mnt/c/Windows/System32/ipconfig.exe"),
        Path("/mnt/c/WINDOWS/system32/ipconfig.exe"),
    ]
    exe = next((p for p in candidatos if p.is_file()), None)
    if exe is None:
        return []
    try:
        r = subprocess.run(
            [str(exe)],
            capture_output=True,
            text=True,
            timeout=8,
        )
    except Exception:
        return []
    texto = (r.stdout or "") + (r.stderr or "")
    ips = []
    for m in re.finditer(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", texto):
        ip = m.group(1)
        if _es_privada(ip) and not ip.endswith(".255") and not ip.endswith(".0"):
            ips.append(ip)
    vistos = []
    for ip in ips:
        if ip not in vistos:
            vistos.append(ip)
    return vistos


def _hosts_extra() -> list[tuple[str, str]]:
    extra = []
    try:
        for line in Path("/etc/resolv.conf").read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("nameserver"):
                ip = line.split()[1]
                if ip and not ip.startswith("127."):
                    extra.append((ip, "resolv.conf / WSL DNS"))
    except OSError:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        yo = s.getsockname()[0]
        s.close()
        partes = yo.split(".")
        if len(partes) == 4:
            extra.append((".".join(partes[:3] + ["1"]), "posible pasarela .1"))
    except Exception:
        pass
    for ip in _ips_windows_desde_wsl():
        extra.append((ip, "ipconfig.exe (Windows en este host)"))
    vistos = set()
    out = []
    for ip, origen in extra:
        if ip not in vistos:
            vistos.add(ip)
            out.append((ip, origen))
    return out


def _puerto_abierto(ip: str, port: int, timeout: float = 0.2) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((ip, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def _probar_host(ip: str, port: int) -> str | None:
    if not _puerto_abierto(ip, port):
        return None
    url = f"http://{ip}:{port}/v1/chat/completions"
    ok, _ = _probe_http(url)
    return url if ok else None


def _escanear_lan(puertos: list[int]) -> tuple[str, int] | None:
    encontrados: list[tuple[str, int]] = []
    lock = threading.Lock()

    def prueba(ip: str, port: int) -> None:
        url = _probar_host(ip, port)
        if url:
            with lock:
                encontrados.append((url, port))

    hilos = []
    for ip in _hosts_lan():
        for port in puertos:
            t = threading.Thread(target=prueba, args=(ip, port), daemon=True)
            hilos.append(t)
            t.start()
            if len(hilos) >= 64:
                for h in hilos:
                    h.join()
                hilos = []
    for h in hilos:
        h.join()
    return encontrados[0] if encontrados else None


def _resolver_local(
    url_cfg: str,
    cache_name: str,
    puertos: list[int],
    etiqueta: str,
) -> tuple[str, str]:
    ok, motivo = _probe_http(url_cfg)
    if ok:
        return url_cfg, f"local o configurada: {motivo}"
    cache = _load_url_cache(cache_name)
    if cache:
        ok, motivo = _probe_http(cache["url"])
        if ok:
            return cache["url"], f"cache: {motivo}"
    for ip, origen in _hosts_extra():
        for port in puertos:
            url = _probar_host(ip, port)
            if url:
                _save_url_cache(cache_name, url, origen)
                return url, f"{origen} puerto {port}: {url}"
    hallado = _escanear_lan(puertos)
    if hallado:
        url, port = hallado
        _save_url_cache(cache_name, url, "lan")
        return url, f"LAN puerto {port}: {url}"
    return url_cfg, f"no hay {etiqueta} en localhost, host WSL, puente ni LAN visible"


def resolver_jan_url(policy: dict) -> tuple[str, str]:
    return _resolver_local(
        policy.get("jan_url") or DEFAULT_POLICY["jan_url"],
        "ia_jan_cache.json",
        [JAN_PORT, PUENTE_PORT],
        "Jan",
    )


def resolver_gpt4all_url(policy: dict) -> tuple[str, str]:
    return _resolver_local(
        policy.get("gpt4all_url") or DEFAULT_POLICY["gpt4all_url"],
        "ia_gpt4all_cache.json",
        [GPT4ALL_PORT],
        "GPT4All",
    )


def _url_chat(provider: str, policy: dict) -> str:
    if provider == "jan":
        url, _ = resolver_jan_url(policy)
        return url
    if provider == "gpt4all":
        url, _ = resolver_gpt4all_url(policy)
        return url
    if provider == "grok":
        return policy.get("grok_url") or DEFAULT_POLICY["grok_url"]
    if provider == "openrouter":
        return policy.get("openrouter_url") or DEFAULT_POLICY["openrouter_url"]
    raise ValueError(provider)


def listar_modelos(provider: str | None = None) -> tuple[bool, str, list[str]]:
    p = load_policy()
    pid = (provider or p.get("provider") or "jan").lower()
    if pid not in PROVIDERS:
        return False, f"Proveedor desconocido: {pid}", []
    url = _url_chat(pid, p)
    ids, raw = _listar_modelos(url, pid)
    if not ids:
        return False, raw or "sin modelos", []
    return True, pid, ids


def modelo_activo(provider: str | None = None) -> str:
    p = load_policy()
    pid = (provider or p.get("provider") or "jan").lower()
    return str(p.get(_campo_modelo(pid)) or "auto")


def set_modelo(model_id: str, provider: str | None = None) -> tuple[bool, str]:
    pid = (provider or load_policy().get("provider") or "jan").lower()
    if pid not in PROVIDERS:
        return False, f"Proveedor desconocido: {pid}"
    mid = model_id.strip()
    if not mid:
        return False, "Indica un id de modelo."
    if mid != "auto":
        ok, msg, ids = listar_modelos(pid)
        if ok and ids and mid not in ids:
            return False, f"'{mid}' no está en la lista de {pid}."
        if not ok and pid in ("grok", "openrouter"):
            return False, f"No se pudo validar el modelo: {msg}"
    save_policy({_campo_modelo(pid): mid})
    return True, f"Modelo de {pid}: {mid}"


def detectar() -> list[dict]:
    ia_keys.ingest_env()
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
    urlg, motivog = resolver_gpt4all_url(p)
    okg = "no hay GPT4All" not in motivog
    out.append(
        {
            "id": "gpt4all",
            "tipo": "local",
            "disponible": okg,
            "motivo": motivog,
            "url": urlg,
        }
    )
    for pid in ("grok", "openrouter"):
        if ia_keys.has_any_key(pid):
            origen = "almacén .mos" if ia_keys.has_stored_key(pid) else "entorno (ingerido)"
            out.append(
                {
                    "id": pid,
                    "tipo": "remoto",
                    "disponible": True,
                    "motivo": f"clave presente ({origen})",
                }
            )
        else:
            out.append(
                {
                    "id": pid,
                    "tipo": "remoto",
                    "disponible": False,
                    "motivo": f"falta clave; iarouter clave {pid}",
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
        "modelo": modelo_activo(),
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
    if provider not in PROVIDERS:
        return False, f"Proveedor '{provider}' desconocido."
    if provider in ("grok", "openrouter") and not ia_keys.has_any_key(provider):
        return False, f"Falta clave de {provider}. iarouter clave {provider}"

    url = _url_chat(provider, p)
    model = p.get(_campo_modelo(provider)) or "auto"
    if model in PLACEHOLDER_MODELS:
        ids, raw_models = _listar_modelos(url, provider)
        model = ids[0] if ids else model
        if model in PLACEHOLDER_MODELS:
            return False, f"{provider} no listó modelos: {raw_models}"
    etiqueta = {"jan": "Jan", "gpt4all": "GPT4All", "grok": "Grok", "openrouter": "OpenRouter"}[
        provider
    ]
    return _complete_openai(prompt, url, model, etiqueta, provider)