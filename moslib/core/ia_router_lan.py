"""Descubrimiento LAN/cache de Jan y GPT4All."""

from __future__ import annotations

import json
import re
import socket
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path

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


def hosts_extra() -> list[tuple[str, str]]:
    extra = []
    try:
        for line in Path("/etc/resolv.conf").read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("nameserver"):
                ip = line.split()[1]
                if ip and not ip.startswith("127."):
                    extra.append((ip, "resolv.conf"))
    except OSError:
        pass
    for exe in (
        Path("/mnt/c/Windows/System32/ipconfig.exe"),
        Path("/mnt/c/WINDOWS/System32/ipconfig.exe"),
    ):
        if not exe.is_file():
            continue
        try:
            r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=8)
        except Exception:
            continue
        for m in re.finditer(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", (r.stdout or "") + (r.stderr or "")):
            ip = m.group(1)
            if es_privada(ip) and not ip.endswith(".0") and not ip.endswith(".255"):
                extra.append((ip, "ipconfig.exe"))
    vistos, out = set(), []
    for ip, origen in extra:
        if ip not in vistos:
            vistos.add(ip)
            out.append((ip, origen))
    return out


def escanear_lan(puertos: list[int]) -> tuple[str, int] | None:
    encontrados: list[tuple[str, int]] = []
    lock = threading.Lock()

    def prueba(ip: str, port: int) -> None:
        url = probar_host(ip, port)
        if url:
            with lock:
                encontrados.append((url, port))

    hosts = []
    for ip in local_ipv4():
        if es_privada(ip):
            pref = ".".join(ip.split(".")[:3])
            hosts.extend(f"{pref}.{n}" for n in range(1, 255))
    hilos = []
    for ip in hosts:
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