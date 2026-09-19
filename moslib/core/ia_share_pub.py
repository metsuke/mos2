"""Reglas de firewall LAN para Jan/GPT4All/puente."""

from __future__ import annotations

import shutil

from moslib.core.ia_share import diagnostico, _guia
from moslib.core.ia_share_net import PUENTE_PORT, PUERTOS, perfil, run


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
    ok, detalle = run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Start-Process -FilePath netsh -ArgumentList "
            f"'{args}' -Verb RunAs -Wait",
        ]
    )
    if ok:
        return True, detalle or f"regla {nombre} (UAC)."
    return False, "No se pudo elevar. Pega en PowerShell admin:\n" + _ps_manual(puerto)


def _publicar_linux(puerto: int) -> tuple[bool, str]:
    if shutil.which("ufw"):
        print(f"sudo ufw: clave para el puerto {puerto}.")
        return run(
            ["sudo", "ufw", "allow", "from", "10.0.0.0/8", "to", "any", "port", str(puerto)],
            True,
        )
    print(f"sudo iptables: clave para el puerto {puerto}.")
    return run(
        ["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(puerto),
         "-s", "10.0.0.0/8", "-j", "ACCEPT"],
        True,
    )


def _publicar_macos(puerto: int) -> tuple[bool, str]:
    return (
        False,
        "macOS no deja a MetsuOS crear la regla. "
        f"Permite Jan/GPT4All en Firewall y bind 0.0.0.0:{puerto}.",
    )


def publicar() -> list[dict]:
    p = perfil()
    items = list(diagnostico())
    for nombre, puerto in list(PUERTOS) + [("puente", PUENTE_PORT)]:
        if p.startswith("windows"):
            ok, detalle = _publicar_windows(puerto)
        elif p.startswith("linux"):
            ok, detalle = _publicar_linux(puerto)
        else:
            ok, detalle = _publicar_macos(puerto)
        items.append({"id": f"publicar-{nombre}", "ok": ok, "motivo": detalle or _guia(p, puerto)})
    return items
