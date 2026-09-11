"""
moslib.core.ia_share
Diagnóstico y publicación explícita de puertos Jan/GPT4All en LAN.
publicar no se llama solo. No abre Internet: solo perfil privado / LAN.
"""

from __future__ import annotations

import shutil
import socket
import subprocess
import sys
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

JAN_PORT = 1337
GPT4ALL_PORT = 4891
PUENTE_PORT = 17337
PUERTOS = (("jan", JAN_PORT), ("gpt4all", GPT4ALL_PORT))


def _perfil() -> str:
    plat = sys.platform
    if plat == "darwin":
        return "macos/native"
    if plat.startswith("win"):
        return "windows"
    if plat.startswith("linux"):
        return "linux/native"
    return plat


def _run(cmd: list[str], stdin_tty: bool = False) -> tuple[bool, str]:
    try:
        r = subprocess.run(
            cmd,
            capture_output=not stdin_tty,
            text=True,
            timeout=120,
        )
    except Exception as exc:
        return False, str(exc)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode == 0, out


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


def _netstat_puerto(puerto: int) -> str:
    if sys.platform.startswith("win"):
        ok, out = _run(["netstat", "-an"])
    else:
        ok, out = _run(["netstat", "-an"])
        if not ok:
            ok, out = _run(["ss", "-ltn"])
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
        ("127.0.0.1" in ln or "[::1]" in ln) and "0.0.0.0" not in ln
        for ln in lineas
    )
    if solo_local and todas_local:
        return f"LISTEN solo en localhost: {texto}. Jan no es visible en la LAN. Usa puente o bind 0.0.0.0."
    if "0.0.0.0:" + str(puerto) in texto or ":::" in texto:
        return f"LISTEN en todas las interfaces: {texto}"
    return texto


def _perfil_firewall_windows() -> str:
    ok, out = _run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-NetConnectionProfile | Select-Object -ExpandProperty NetworkCategory",
        ]
    )
    if not ok or not out.strip():
        return "no se pudo leer el perfil de red"
    cats = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if any(c.lower() == "public" for c in cats):
        return (
            "perfil de red Public. La regla de publicar es Private y no aplica. "
            "En Configuración > Red, pon esta red como Privada. " + " ".join(cats)
        )
    return "perfil de red: " + " ".join(cats)


def _guia(perfil: str, puerto: int) -> str:
    if perfil == "macos/native":
        return (
            f"En macOS el servidor debe escuchar en 0.0.0.0:{puerto}, no solo en 127.0.0.1. "
            f"En Firewall de aplicaciones, permite el binario de Jan o GPT4All."
        )
    if perfil.startswith("windows"):
        return (
            f"En Windows el servidor debe escuchar en 0.0.0.0:{puerto}. "
            f"Regla de entrada TCP {puerto} solo en perfil privado. "
            f"Plan B: iarouter puente on y abrir TCP {PUENTE_PORT}."
        )
    return (
        f"El servidor debe escuchar en 0.0.0.0:{puerto}. "
        f"Abre TCP {puerto} hacia la LAN, no hacia Internet."
    )


def diagnostico() -> list[dict]:
    perfil = _perfil()
    lan = _local_ipv4()
    ip_lan = lan[0] if lan else None
    items = []

    ok_j, mot_j = _escucha("127.0.0.1", JAN_PORT)
    items.append({"id": "jan-local", "ok": ok_j, "motivo": mot_j})
    items.append({"id": "jan-listen", "ok": ok_j, "motivo": _netstat_puerto(JAN_PORT)})

    if ip_lan:
        ok_jl, mot_jl = _escucha(ip_lan, JAN_PORT)
        items.append({"id": "jan-lan", "ok": ok_jl, "motivo": mot_jl})
        http_ok, http_m = _http(f"http://{ip_lan}:{JAN_PORT}/v1")
        items.append({"id": "jan-http-lan", "ok": http_ok, "motivo": http_m})
    else:
        items.append({"id": "jan-lan", "ok": False, "motivo": "sin IPv4 privada"})

    ok_g, mot_g = _escucha("127.0.0.1", GPT4ALL_PORT)
    items.append({"id": "gpt4all-local", "ok": ok_g, "motivo": mot_g})
    items.append({"id": "gpt4all-listen", "ok": ok_g, "motivo": _netstat_puerto(GPT4ALL_PORT)})
    if ip_lan:
        ok_gl, mot_gl = _escucha(ip_lan, GPT4ALL_PORT)
        items.append({"id": "gpt4all-lan", "ok": ok_gl, "motivo": mot_gl})
    else:
        items.append({"id": "gpt4all-lan", "ok": False, "motivo": "sin IPv4 privada"})

    ok_p, mot_p = _escucha("127.0.0.1", PUENTE_PORT)
    items.append({"id": "puente-local", "ok": ok_p, "motivo": mot_p + ". iarouter puente on si está parado."})
    items.append({"id": "puente-listen", "ok": ok_p, "motivo": _netstat_puerto(PUENTE_PORT)})
    if ip_lan:
        ok_pl, mot_pl = _escucha(ip_lan, PUENTE_PORT)
        items.append({"id": "puente-lan", "ok": ok_pl, "motivo": mot_pl})

    if perfil.startswith("windows"):
        fw = _perfil_firewall_windows()
        items.append({"id": "firewall-perfil", "ok": "Public" not in fw, "motivo": fw})

    items.append(
        {
            "id": "perfil",
            "ok": True,
            "motivo": f"entorno {perfil}; IP LAN {ip_lan or 'desconocida'}",
        }
    )
    if not any(i["id"] == "jan-lan" and i["ok"] for i in items):
        items.append({"id": "guia-jan", "ok": False, "motivo": _guia(perfil, JAN_PORT)})
    if not any(i["id"] == "gpt4all-lan" and i["ok"] for i in items):
        items.append({"id": "guia-gpt4all", "ok": False, "motivo": _guia(perfil, GPT4ALL_PORT)})
    return items


def _ps_manual(puerto: int) -> str:
    return (
        "New-NetFirewallRule -DisplayName "
        f"'MetsuOS-LAN-{puerto}' -Direction Inbound -Protocol TCP "
        f"-LocalPort {puerto} -Action Allow -Profile Private"
    )


def _publicar_windows(puerto: int) -> tuple[bool, str]:
    nombre = f"MetsuOS-LAN-{puerto}"
    args = (
        f"advfirewall firewall add rule name={nombre} dir=in action=allow "
        f"protocol=TCP localport={puerto} profile=private"
    )
    print(f"Windows: se pedirá permiso UAC para el puerto {puerto}.")
    ok, detalle = _run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Start-Process -FilePath netsh -ArgumentList "
            f"'{args}' -Verb RunAs -Wait",
        ]
    )
    if ok:
        return True, detalle or f"regla {nombre} (UAC). Si aceptaste el diálogo, está creada."
    manual = _ps_manual(puerto)
    return (
        False,
        "No se pudo elevar. Pega esto en PowerShell como administrador:\n" + manual,
    )


def _publicar_linux(puerto: int) -> tuple[bool, str]:
    if shutil.which("ufw"):
        print(f"sudo ufw: se pedirá la clave para el puerto {puerto}.")
        return _run(
            ["sudo", "ufw", "allow", "from", "10.0.0.0/8", "to", "any", "port", str(puerto)],
            stdin_tty=True,
        )
    print(f"sudo iptables: se pedirá la clave para el puerto {puerto}.")
    return _run(
        [
            "sudo",
            "iptables",
            "-A",
            "INPUT",
            "-p",
            "tcp",
            "--dport",
            str(puerto),
            "-s",
            "10.0.0.0/8",
            "-j",
            "ACCEPT",
        ],
        stdin_tty=True,
    )


def _publicar_macos(puerto: int) -> tuple[bool, str]:
    return (
        False,
        "macOS no deja a MetsuOS crear la regla del Firewall de aplicaciones. "
        f"Permite Jan/GPT4All en Ajustes > Red > Firewall y bind 0.0.0.0:{puerto}.",
    )


def publicar() -> list[dict]:
    perfil = _perfil()
    items = list(diagnostico())
    destinos = list(PUERTOS) + [("puente", PUENTE_PORT)]
    for nombre, puerto in destinos:
        if perfil.startswith("windows"):
            ok, detalle = _publicar_windows(puerto)
        elif perfil.startswith("linux"):
            ok, detalle = _publicar_linux(puerto)
        else:
            ok, detalle = _publicar_macos(puerto)
        items.append(
            {
                "id": f"publicar-{nombre}",
                "ok": ok,
                "motivo": detalle or _guia(perfil, puerto),
            }
        )
    return items