"""
moslib.core.ia_check
Diagnóstico de compartición.
Modo corto: conclusión + una acción.
Modo detalle: lo mismo y las pruebas que lo justifican.
Nunca ofrece la IP de esta máquina como destino a guardar.
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


def _tcp(ip: str, port: int, timeout: float = 0.6) -> bool:
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


def _ips_windows() -> list[str]:
    for exe in (
        Path("/mnt/c/Windows/System32/ipconfig.exe"),
        Path("/mnt/c/WINDOWS/system32/ipconfig.exe"),
    ):
        if not exe.is_file():
            continue
        try:
            r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=8)
        except Exception:
            return []
        ips = []
        for m in re.finditer(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", (r.stdout or "") + (r.stderr or "")):
            ip = m.group(1)
            if _es_privada(ip) and not ip.endswith(".0") and not ip.endswith(".255"):
                if ip not in ips:
                    ips.append(ip)
        return ips
    return []


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
    propias = set(lan) | {"127.0.0.1"}
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
    if not (local["jan"] or local["gpt4all"] or local["puente"]):
        destinos.append(("127.0.0.1", "localhost"))
    for ip in _ips_windows():
        if ip not in propias:
            destinos.append((ip, "windows-host"))
    resolv = Path("/etc/resolv.conf")
    if resolv.is_file():
        try:
            for line in resolv.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("nameserver"):
                    ip = line.split()[1]
                    if ip and not ip.startswith("127.") and ip not in propias:
                        destinos.append((ip, "resolv"))
        except OSError:
            pass
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
            if ok and ip not in propias:
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
        "ips_windows": _ips_windows(),
        "urls": urls,
        "pruebas": pruebas,
    }


def _decidir(h: dict) -> tuple[str, str, str]:
    urls = h["urls"]
    if urls:
        return (
            "Esta instancia ya ve una compartición AJENA en la red (no es esta máquina).",
            "Cuando pregunte si guardar la URL, responde s. "
            "Después escribe: iarouter usar jan   y cuando esté activo: iarouter preguntar hola",
            urls[0],
        )

    if h["local"]["jan"] or h["local"]["gpt4all"] or h["local"]["puente"]:
        if h["perfil"] and "Public" in h["perfil"]:
            return (
                "Hay servidor local, pero esta red Windows está en perfil Público. "
                "publicar crea reglas solo para perfil Privado, así que el firewall sigue tapando 1337/17337.",
                "En esta Windows: 1) Clic derecho en el icono de red de la bandeja o Configuración > Red e Internet. "
                "2) Entra en Wi‑Fi o Ethernet, la conexión activa. "
                "3) Tipo de perfil de red: Privado (no Público). "
                "4) Vuelve a MOSh y escribe: iarouter publicar   (acepta el UAC). "
                "5) En la otra instancia (WSL o Mac): iarouter check. "
                "No guardes aquí la URL de tu propia IP. Esta máquina usa 127.0.0.1. "
                "Si no encuentras la opción: PowerShell como administrador: "
                "Set-NetConnectionProfile -InterfaceAlias 'Wi-Fi' -NetworkCategory Private "
                "(cambia Wi-Fi por el alias que salga en Get-NetConnectionProfile).",
                "",
            )
        if (h["local"]["jan"] or h["local"]["gpt4all"]) and h["solo_loop"]["jan"] and not h["puente_sesion"]:
            return (
                "Jan o GPT4All solo escuchan en 127.0.0.1. Otra máquina o WSL no pueden usar ese puerto.",
                "En ESTA sesión de MOSh escribe: iarouter puente on   "
                "No cierres este MOSh. Luego: iarouter publicar   y en la otra instancia: iarouter check. "
                "No cambies jan_url de esta máquina a su IP LAN.",
                "",
            )
        if h["puente_sesion"] and not h["lan_ok"]["puente"]:
            return (
                "El puente está activo en este MOSh y no responde en la IP LAN. El puerto 17337 no entra por el firewall.",
                "En ESTA sesión: iarouter publicar   y acepta UAC. "
                "Si falla, PowerShell administrador: "
                "New-NetFirewallRule -DisplayName 'MetsuOS-Puente-LAN' -Direction Inbound -Protocol TCP -LocalPort 17337 -Action Allow -Profile Private. "
                "Luego en la otra instancia: iarouter check",
                "",
            )
        if h["local"]["jan"] and not h["lan_ok"]["jan"] and not h["puente_sesion"]:
            return (
                "Jan responde en localhost y no en la IP de la LAN.",
                "En ESTA sesión: iarouter puente on    Luego: iarouter publicar    Luego en la otra instancia: iarouter check",
                "",
            )
        return (
            "Hay proceso local. Esta instancia debe seguir usando 127.0.0.1, no su IP LAN.",
            "Si el puente no está: iarouter puente on. Luego: iarouter publicar. "
            "En WSL o Mac: iarouter check. "
            "Si alguna vez guardaste http://TU-IP:17337 en esta Windows, escribe: iarouter usar jan",
            "",
        )

    if h["wsl"] and h["ips_windows"]:
        return (
            "Estás en WSL. Las IPs de Windows se ven y no abren Jan ni el puente.",
            "No lo arregles desde WSL. Abre Git Bash en Windows, cd al clone, ./mos2.sh, "
            "escribe: iarouter check    y sigue la acción de esa instancia (casi siempre puente on y publicar). "
            "Deja ese MOSh abierto. Vuelve a este WSL y escribe: iarouter check",
            "",
        )
    return (
        "Aquí no hay servidor local ni se ve ninguno ajeno.",
        "Ve a la máquina o entorno que debe compartir (win con Jan, no este WSL si Jan corre en Windows). "
        "Ahí: ./mos2.sh    y    iarouter check    Aplica solo esa acción. Vuelve aquí: iarouter check",
        "",
    )


def check(detalle: bool = False) -> list[dict]:
    h = _hechos()
    conclusion, accion, url = _decidir(h)
    ok_conc = bool(url) or ("Hay proceso local" in conclusion)
    out = [
        _item("conclusion", ok_conc, conclusion, url),
        _item("accion", True, accion, url),
    ]
    if not detalle:
        return out
    out.append(_item("detalle-wsl", h["wsl"], f"wsl={h['wsl']} ip_lan={h['ip_lan']} perfil={h['perfil'] or '-'}"))
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