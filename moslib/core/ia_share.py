"""
moslib.core.ia_share
Diagnóstico de si Jan/GPT4All se pueden usar desde la LAN.
No cambia el firewall. Eso es iarouter publicar (M6).
"""

from __future__ import annotations

import socket
import sys
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

JAN_PORT = 1337
GPT4ALL_PORT = 4891


def _perfil() -> str:
    plat = sys.platform
    if plat == "darwin":
        return "macos/native"
    if plat.startswith("win"):
        return "windows"
    if plat.startswith("linux"):
        return "linux/native"
    return plat


def _local_ipv4() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return [ip for ip in found if not ip.startswith("127.")]


def _escucha(host: str, port: int) -> tuple[bool, str]:
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


def _http(url: str) -> tuple[bool, str]:
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


def _guia(perfil: str, puerto: int) -> str:
    if perfil == "macos/native":
        return (
            f"En macOS el servidor debe escuchar en 0.0.0.0:{puerto}, no solo en 127.0.0.1. "
            f"En Firewall de aplicaciones, permite el binario de Jan o GPT4All. "
            f"Luego: iarouter publicar (autorización explícita)."
        )
    if perfil.startswith("windows"):
        return (
            f"En Windows el servidor debe escuchar en 0.0.0.0:{puerto}. "
            f"En el firewall de Windows, regla de entrada TCP {puerto} solo para la LAN. "
            f"Luego: iarouter publicar."
        )
    return (
        f"El servidor debe escuchar en 0.0.0.0:{puerto}. "
        f"Abre TCP {puerto} en el firewall hacia la LAN, no hacia Internet. "
        f"Luego: iarouter publicar."
    )


def diagnostico() -> list[dict]:
    perfil = _perfil()
    lan = _local_ipv4()
    ip_lan = lan[0] if lan else None
    items = []

    ok_j, mot_j = _escucha("127.0.0.1", JAN_PORT)
    items.append({"id": "jan-local", "ok": ok_j, "motivo": mot_j})
    if ip_lan:
        ok_jl, mot_jl = _escucha(ip_lan, JAN_PORT)
        items.append({"id": "jan-lan", "ok": ok_jl, "motivo": mot_jl})
        http_ok, http_m = _http(f"http://{ip_lan}:{JAN_PORT}/v1")
        items.append({"id": "jan-http-lan", "ok": http_ok, "motivo": http_m})
    else:
        items.append({"id": "jan-lan", "ok": False, "motivo": "sin IPv4 privada"})

    ok_g, mot_g = _escucha("127.0.0.1", GPT4ALL_PORT)
    items.append({"id": "gpt4all-local", "ok": ok_g, "motivo": mot_g})
    if ip_lan:
        ok_gl, mot_gl = _escucha(ip_lan, GPT4ALL_PORT)
        items.append({"id": "gpt4all-lan", "ok": ok_gl, "motivo": mot_gl})
    else:
        items.append({"id": "gpt4all-lan", "ok": False, "motivo": "sin IPv4 privada"})

    items.append(
        {
            "id": "perfil",
            "ok": True,
            "motivo": f"entorno {perfil}; IP LAN {ip_lan or 'desconocida'}",
        }
    )
    if not (ip_lan and any(i["id"] == "jan-lan" and i["ok"] for i in items)):
        items.append({"id": "guia-jan", "ok": False, "motivo": _guia(perfil, JAN_PORT)})
    if not (ip_lan and any(i["id"] == "gpt4all-lan" and i["ok"] for i in items)):
        items.append({"id": "guia-gpt4all", "ok": False, "motivo": _guia(perfil, GPT4ALL_PORT)})
    return items