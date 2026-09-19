"""Descubrimiento LAN/cache de Jan y GPT4All."""

from __future__ import annotations

import json
import socket
from datetime import datetime, timezone

from moslib.core.ia_router_http import probe_http
from moslib.core.ia_router_policy import CACHE_TTL_SEC, cache_path


def load_url_cache(nombre: str) -> dict | None:
    path = cache_path(nombre)
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


def save_url_cache(nombre: str, url: str, origen: str) -> None:
    payload = {
        "url": url,
        "origen": origen,
        "cuando": datetime.now(timezone.utc).isoformat(),
    }
    cache_path(nombre).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def es_privada(ip: str) -> bool:
    try:
        p = [int(x) for x in ip.split(".")]
    except ValueError:
        return False
    return p[0] == 10 or (p[0] == 192 and p[1] == 168) or (p[0] == 172 and 16 <= p[1] <= 31)


def local_ipv4() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return [ip for ip in found if not ip.startswith("127.")]


def puerto_abierto(ip: str, port: int, timeout: float = 0.2) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((ip, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def probar_host(ip: str, port: int) -> str | None:
    if not puerto_abierto(ip, port):
        return None
    url = f"http://{ip}:{port}/v1/chat/completions"
    ok, _ = probe_http(url)
    return url if ok else None


def hosts_extra():
    from moslib.core.ia_router_lan_scan import hosts_extra as _fn
    return _fn()


def escanear_lan(puertos: list[int]):
    from moslib.core.ia_router_lan_scan import escanear_lan as _fn
    return _fn(puertos)
