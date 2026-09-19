"""Barrido LAN de Jan/GPT4All."""

from __future__ import annotations

import re
import subprocess
import threading
from pathlib import Path

from moslib.core.ia_router_lan import es_privada, local_ipv4, probar_host


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
