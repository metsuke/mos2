"""Red y listen de ia_share."""

from __future__ import annotations

import socket
import subprocess
import sys
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

JAN_PORT = 1337
GPT4ALL_PORT = 4891
PUENTE_PORT = 17337
PUERTOS = (("jan", JAN_PORT), ("gpt4all", GPT4ALL_PORT))


def perfil() -> str:
    plat = sys.platform
    if plat == "darwin":
        return "macos/native"
    if plat.startswith("win"):
        return "windows"
    if plat.startswith("linux"):
        return "linux/native"
    return plat


def run(cmd: list[str], stdin_tty: bool = False) -> tuple[bool, str]:
    try:
        r = subprocess.run(cmd, capture_output=not stdin_tty, text=True, timeout=120)
    except Exception as exc:
        return False, str(exc)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode == 0, out


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


def escucha(host: str, port: int) -> tuple[bool, str]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        ok = s.connect_ex((host, port)) == 0
        s.close()
        if ok:
            return True, f"{host}:{port} acepta TCP"
        return False, f"{host}:{port} no acepta TCP"
    except Exception as exc:
        return False, f"{host}:{port} error: {exc}"


def http(url: str) -> tuple[bool, str]:
    req = Request(url, method="GET")
    try:
        with urlopen(req, timeout=2) as resp:
            resp.read(32)
        return True, f"HTTP OK {url}"
    except HTTPError as exc:
        if exc.code in (400, 401, 404, 405, 422):
            return True, f"HTTP {exc.code} {url}"
        return False, f"HTTP {exc.code} {url}"
    except URLError as exc:
        return False, f"HTTP no: {exc.reason}"
    except Exception as exc:
        return False, str(exc)


def netstat_puerto(puerto: int) -> str:
    ok, out = run(["netstat", "-an"])
    if not ok:
        ok, out = run(["ss", "-ltn"])
    if not ok:
        return "no se pudo leer netstat/ss"
    lineas = [
        ln.strip()
        for ln in (out or "").splitlines()
        if str(puerto) in ln and ("LISTEN" in ln.upper() or "LISTENING" in ln.upper())
    ]
    if not lineas:
        return f"nadie en LISTEN en {puerto}"
    texto = " | ".join(lineas[:4])
    solo_local = any("127.0.0.1:" + str(puerto) in ln or "[::1]:" in ln for ln in lineas)
    todas_local = all(
        ("127.0.0.1" in ln or "[::1]" in ln) and "0.0.0.0" not in ln for ln in lineas
    )
    if solo_local and todas_local:
        return f"LISTEN solo en localhost: {texto}. Jan no es visible en la LAN."
    if "0.0.0.0:" + str(puerto) in texto or ":::" in texto:
        return f"LISTEN en todas las interfaces: {texto}"
    return texto
