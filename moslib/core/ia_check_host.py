"""IPs del anfitrión, listen y proxy para ia_check."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from moslib.core.ia_check_net import es_privada


def ips_de_texto(texto: str) -> list[str]:
    ips = []
    for m in re.finditer(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", texto or ""):
        ip = m.group(1)
        if es_privada(ip) and not ip.endswith(".0") and not ip.endswith(".255"):
            if ip not in ips:
                ips.append(ip)
    return ips


def ips_windows() -> list[str]:
    cmds = []
    for exe in (
        Path("/mnt/c/Windows/System32/ipconfig.exe"),
        Path("/mnt/c/WINDOWS/System32/ipconfig.exe"),
        Path("/mnt/c/Windows/System32/cmd.exe"),
        Path("/mnt/c/WINDOWS/System32/cmd.exe"),
    ):
        if not exe.is_file():
            continue
        if exe.name.lower() == "cmd.exe":
            cmds.append([str(exe), "/c", "ipconfig"])
        else:
            cmds.append([str(exe)])
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        except Exception:
            continue
        ips = ips_de_texto((r.stdout or "") + (r.stderr or ""))
        if ips:
            return ips
    return []


def pasarela() -> list[str]:
    found = []
    try:
        r = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=5)
        for m in re.finditer(r"default via (\d{1,3}(?:\.\d{1,3}){3})", r.stdout or ""):
            ip = m.group(1)
            if ip not in found:
                found.append(ip)
    except Exception:
        pass
    resolv = Path("/etc/resolv.conf")
    if resolv.is_file():
        try:
            for line in resolv.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("nameserver"):
                    ip = line.split()[1]
                    if ip and not ip.startswith("127.") and ip not in found:
                        found.append(ip)
        except OSError:
            pass
    return found


def listen(puerto: int) -> str:
    try:
        r = subprocess.run(["netstat", "-an"], capture_output=True, text=True, timeout=8)
        texto = (r.stdout or "") + (r.stderr or "")
    except Exception:
        return ""
    lineas = [
        ln
        for ln in texto.splitlines()
        if str(puerto) in ln and ("LISTEN" in ln.upper() or "LISTENING" in ln.upper())
    ]
    return " | ".join(ln.strip() for ln in lineas[:3])


def perfil_windows() -> str:
    if not sys.platform.startswith("win"):
        return ""
    try:
        r = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-NetConnectionProfile | Select-Object -ExpandProperty NetworkCategory",
            ],
            capture_output=True,
            text=True,
            timeout=8,
        )
        return (r.stdout or "").strip()
    except Exception:
        return ""


def proxy_env() -> str:
    keys = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY")
    found = []
    for k in keys:
        v = os.environ.get(k)
        if v:
            found.append(f"{k}=***")
    return ", ".join(found) if found else ""