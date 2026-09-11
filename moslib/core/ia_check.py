"""
moslib.core.ia_check
Diagnóstico de compartición.
En WSL sondea 127.0.0.1, nameserver e ipconfig de Windows.
No ofrece la IP LAN de esta máquina Windows como destino a guardar.
"""

from __future__ import annotations

import re
import socket
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

JAN = 1337
GPT4ALL = 4891
PUENTE = 17337
SERVICIOS = (("jan", JAN), ("gpt4all", GPT4ALL), ("puente", PUENTE))


def _item(ident: str, ok: bool, motivo: str, url: str = "") -> dict:
    return {"id": ident, "ok": ok, "motivo": motivo, "url": url}


def _tcp(ip: str, port: int, timeout: float = 0.8) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((ip, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def _http(url: str) -> tuple[bool, str]:
    req = Request(url, method="GET")
    try:
        with urlopen(req, timeout=3) as resp:
            return True, resp.read(80).decode("utf-8", errors="replace")
    except HTTPError as exc:
        if exc.code in (400, 401, 404, 405, 422):
            return True, f"HTTP {exc.code}"
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, str(exc)


def _es_privada(ip: str) -> bool:
    try:
        p = [int(x) for x in ip.split(".")]
    except ValueError:
        return False
    return (
        p[0] == 10
        or (p[0] == 192 and p[1] == 168)
        or (p[0] == 172 and 16 <= p[1] <= 31)
    )


def _es_wsl() -> bool:
    if Path("/mnt/c/Windows").is_dir():
        return True
    proc = Path("/proc/version")
    if not proc.is_file():
        return False
    try:
        return "microsoft" in proc.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False


def _ipv4_propia() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return [ip for ip in found if not ip.startswith("127.")]


def _ips_de_texto(texto: str) -> list[str]:
    ips = []
    for m in re.finditer(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", texto or ""):
        ip = m.group(1)
        if _es_privada(ip) and not ip.endswith(".0") and not ip.endswith(".255"):
            if ip not in ips:
                ips.append(ip)
    return ips


def _ips_windows() -> list[str]:
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
        ips = _ips_de_texto((r.stdout or "") + (r.stderr or ""))
        if ips:
            return ips
    return []


def _pasarela() -> list[str]:
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


def _listen(puerto: int) -> str:
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


def _perfil_windows() -> str:
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


def _puente_sesion() -> bool:
    try:
        from moslib.core import ia_bridge

        return bool(ia_bridge.estado().get("activo"))
    except Exception:
        return False


def _hechos() -> dict:
    lan = _ipv4_propia()
    win_ips = _ips_windows()
    extra = _pasarela()
    propias_lan = set(lan)
    ip_lan = lan[0] if lan else None
    listen = {n: _listen(p) for n, p in SERVICIOS}
    local = {n: _tcp("127.0.0.1", p) for n, p in SERVICIOS}
    lan_ok = {n: (_tcp(ip_lan, p) if ip_lan else False) for n, p in SERVICIOS}
    solo_loop = {
        n: bool(listen[n]) and "127.0.0.1" in listen[n] and "0.0.0.0" not in listen[n]
        for n, _p in SERVICIOS
    }
    urls = []
    pruebas = []
    destinos = []
    if _es_wsl():
        destinos.append(("127.0.0.1", "wsl-localhost"))
        for ip in extra:
            destinos.append((ip, "wsl-host"))
        for ip in win_ips:
            destinos.append((ip, "windows-host"))
    else:
        destinos.append(("127.0.0.1", "localhost"))
        for ip in extra:
            if ip not in propias_lan:
                destinos.append((ip, "pasarela"))
    vistos = set()
    for ip, origen in destinos:
        if ip in vistos:
            continue
        vistos.add(ip)
        for n, p in SERVICIOS:
            ruta = "/health" if n == "puente" else "/v1/models"
            if not _tcp(ip, p):
                pruebas.append(_item(f"prueba-{n}-{origen}-{ip}", False, f"cerrado {ip}:{p}"))
                continue
            ok, det = _http(f"http://{ip}:{p}{ruta}")
            chat = f"http://{ip}:{p}/v1/chat/completions"
            pruebas.append(_item(f"prueba-{n}-{origen}-{ip}", ok, det, chat if ok else ""))
            if not ok:
                continue
            if _es_wsl():
                urls.append(chat)
            elif ip not in propias_lan and ip != "127.0.0.1":
                urls.append(chat)
    return {
        "wsl": _es_wsl(),
        "ip_lan": ip_lan,
        "listen": listen,
        "local": local,
        "lan_ok": lan_ok,
        "solo_loop": solo_loop,
        "perfil": _perfil_windows(),
        "puente_sesion": _puente_sesion(),
        "ips_windows": win_ips,
        "pasarela": extra,
        "urls": urls,
        "pruebas": pruebas,
        "probadas": [f"{o}:{i}" for i, o in destinos],
    }


def _decidir(h: dict) -> tuple[str, str, str]:
    urls = h["urls"]
    if urls:
        return (
            "Esta instancia ya ve una compartición usable.",
            "Cuando pregunte si guardar la URL, responde s. "
            "Después: iarouter usar jan   y   iarouter preguntar hola",
            urls[0],
        )

    if (not h["wsl"]) and (h["local"]["jan"] or h["local"]["gpt4all"] or h["local"]["puente"]):
        if h["perfil"] and "Public" in h["perfil"]:
            return (
                "Hay servidor local, pero esta red Windows está en perfil Público.",
                "Pon la red en Privada. Luego: iarouter publicar. En WSL o Mac: iarouter check.",
                "",
            )
        if not h["puente_sesion"]:
            return (
                "Hay Jan en localhost y no hay puente en esta sesión.",
                "iarouter puente on    Luego: iarouter publicar    En WSL/Mac: iarouter check",
                "",
            )
        return (
            "Hay proceso local. Esta instancia usa 127.0.0.1.",
            "Deja este MOSh abierto. En Mac/WSL: iarouter check",
            "",
        )

    if h["wsl"]:
        vistos = ", ".join(h.get("probadas") or []) or "ninguna"
        return (
            "Estás en WSL y no se alcanza Jan ni el puente de Windows. "
            f"IPs sondeadas: {vistos}.",
            "En Git Bash: puente on y publicar, MOSh abierto. "
            "Si Mac ya funciona, la LAN está bien; WSL2 no usa esa ruta. "
            "Acepta 127.0.0.1 si este check lo ofrece.",
            "",
        )
    return (
        "Aquí no hay servidor local ni se ve ninguno ajeno.",
        "En el win que comparte: iarouter puente on, publicar. Aquí: iarouter check.",
        "",
    )


def check(detalle: bool = False) -> list[dict]:
    h = _hechos()
    conclusion, accion, url = _decidir(h)
    out = [
        _item("conclusion", bool(url), conclusion, url),
        _item("accion", True, accion, url),
    ]
    if not detalle:
        return out
    out.append(
        _item(
            "detalle-entorno",
            h["wsl"],
            f"wsl={h['wsl']} ip_lan={h['ip_lan']} win={h['ips_windows']} pasarela={h['pasarela']}",
        )
    )
    out.append(_item("detalle-puente-sesion", h["puente_sesion"], "puente en ESTE MOSh"))
    for n, p in SERVICIOS:
        out.append(
            _item(
                f"detalle-listen-{n}",
                h["local"][n],
                f"local={h['local'][n]} lan={h['lan_ok'][n]} loop_only={h['solo_loop'][n]} listen={h['listen'][n] or 'nadie'} puerto={p}",
            )
        )
    out.extend(h["pruebas"])
    return out