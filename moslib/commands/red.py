"""
red – inventario de red del anfitrión.
Solo datos lícitos del sistema: interfaces, pasarela, DNS, caché ARP.
No barre la LAN ni abre puertos ajenos.
"""

import os
import socket
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
    except Exception as exc:
        return f"(no disponible: {exc})"
    out = (r.stdout or "") + (r.stderr or "")
    return out.strip() or "(sin salida)"


def _hostname() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "?"


def _ips() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    try:
        for info in socket.getaddrinfo(_hostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                found.add(ip)
    except Exception:
        pass
    return sorted(found)


def _dns() -> list[str]:
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


def _pasarela() -> str:
    if sys.platform.startswith("win"):
        return _run(["route", "print", "0.0.0.0"])
    if shutil_which("ip"):
        return _run(["ip", "route"])
    return _run(["netstat", "-rn"])


def shutil_which(name: str) -> bool:
    from shutil import which

    return which(name) is not None


def _arp() -> str:
    return _run(["arp", "-a"])


def _perfil() -> str:
    if sys.platform == "darwin":
        return "macos/native"
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform.startswith("linux"):
        if "microsoft" in Path("/proc/version").read_text(encoding="utf-8", errors="ignore").lower() if Path("/proc/version").is_file() else False:
            return "linux/wsl"
        return "linux/native"
    return sys.platform


def execute(args):
    args = list(args or [])
    print("Red del anfitrión (inventario lícito)")
    print()
    print(f"Perfil: {_perfil()}")
    print(f"Hostname: {_hostname()}")
    print(f"Usuario proceso: {os.environ.get('USER') or os.environ.get('USERNAME') or '?'}")
    print()
    print("Direcciones IPv4 de esta máquina")
    print("--------------------------------")
    ips = _ips()
    if not ips:
        print("(ninguna además de localhost)")
    else:
        for ip in ips:
            print(ip)
    print()
    print("DNS (resolv.conf si existe)")
    print("---------------------------")
    dns = _dns()
    if dns:
        for d in dns:
            print(d)
    else:
        print("(no hay /etc/resolv.conf o está vacío)")
    print()
    print("Rutas / pasarela (salida del SO)")
    print("--------------------------------")
    print()
    print(_pasarela())
    print()
    print("Vecinos en caché ARP (no es un barrido)")
    print("---------------------------------------")
    print()
    print(_arp())
    print()
    print("Detalle")
    print("-------")
    print()
    print(
        "Esto no explora puertos ni hosts que el sistema no conozca ya. "
        "Un inventario ofensivo o reglas de enfrentamiento cibernético "
        "no forman parte de este comando."
    )


def help():
    return (
        "Uso: red - Muestra red local lícita: hostname, IP, DNS, pasarela y caché ARP. "
        "No barre la LAN."
    )