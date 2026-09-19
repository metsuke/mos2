"""Inventario lícito de red: host, IPs, DNS, pasarela, ARP."""

from __future__ import annotations

import socket
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
    except Exception as exc:
        return f"(no disponible: {exc})"
    out = (r.stdout or "") + (r.stderr or "")
    return out.strip() or "(sin salida)"


def hostname() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "?"


def ips() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    try:
        for info in socket.getaddrinfo(hostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                found.add(ip)
    except Exception:
        pass
    return sorted(found)


def dns() -> list[str]:
    servidores = []
    path = Path("/etc/resolv.conf")
    if path.is_file():
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("nameserver"):
                    servidores.append(line.split()[1])
        except OSError:
            pass
    return servidores


def which(name: str) -> bool:
    from shutil import which as w
    return w(name) is not None


def pasarela() -> str:
    if sys.platform.startswith("win"):
        return run(["route", "print", "0.0.0.0"])
    if which("ip"):
        return run(["ip", "route"])
    return run(["netstat", "-rn"])


def arp() -> str:
    return run(["arp", "-a"])


def perfil() -> str:
    if sys.platform == "darwin":
        return "macos/native"
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform.startswith("linux"):
        ver = Path("/proc/version")
        txt = ver.read_text(encoding="utf-8", errors="ignore").lower() if ver.is_file() else ""
        return "linux/wsl" if "microsoft" in txt else "linux/native"
    return sys.platform
