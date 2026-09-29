"""Ejecuta el lote de multi y resume fallos."""

import shlex
from pathlib import Path

from moslib.core.cmd_loader import CommandManager
from moslib.core import write_b64
from moslib.core.user import (
    get_user_apps_dir,
    get_system_apps_dir,
    get_username,
    get_user_mos_dir,
)


def _manager():
    aqui = Path(__file__).resolve().parents[1] / "commands"
    return CommandManager(
        system_commands_dir=aqui,
        user_commands_dir=get_user_mos_dir(get_username()) / "commands",
        apps_root=get_user_apps_dir(),
        system_apps_root=get_system_apps_dir(),
        enforce_security=True,
    )


def _es_fallo(valor) -> bool:
    if valor is None or valor is True:
        return False
    if valor is False:
        return True
    if isinstance(valor, int):
        return valor != 0
    return False


def _una(mgr, lote, nombre, args, i):
    if nombre in ("write", "w"):
        payload = []
        i += 1
        while i < len(lote) and lote[i].strip() != ".":
            payload.append(lote[i])
            i += 1
        if i < len(lote) and lote[i].strip() == ".":
            i += 1
        write_b64.PERMISO_MULTI = True
        try:
            mod = mgr.get_command(nombre)
            valor = mod.execute(args, payload) if mod and hasattr(mod, "execute") else 1
        finally:
            write_b64.PERMISO_MULTI = False
        return i, valor
    mod = mgr.get_command(nombre)
    if not (mod and hasattr(mod, "execute")):
        print("mosh: comando no encontrado: %s" % nombre)
        return i + 1, 1
    return i + 1, mod.execute(args)


def lanzar(lote: list) -> int:
    if not lote:
        print("[multi] Lote vacio.")
        return 1
    mgr = _manager()
    print("[multi] Ejecutando lote (%s linea(s))." % len(lote))
    i = 0
    fallos = []
    ok = 0
    while i < len(lote):
        line = lote[i]
        if not line.strip():
            i += 1
            continue
        try:
            parts = shlex.split(line, posix=True)
        except ValueError as exc:
            fallos.append((line[:40], str(exc)))
            print("!!! [multi] comillas rotas: %s" % exc)
            i += 1
            continue
        if not parts:
            i += 1
            continue
        nombre, args = parts[0], parts[1:]
        print("mosh$ %s %s" % (nombre, " ".join(args)))
        if nombre in ("multi", "m"):
            i += 1
            continue
        try:
            i, valor = _una(mgr, lote, nombre, args, i)
        except Exception as exc:
            fallos.append((nombre, str(exc)))
            print("!!! [multi] %s: %s" % (nombre, exc))
            i += 1
            continue
        if _es_fallo(valor):
            fallos.append((nombre, str(valor)))
            print("!!! [multi] fallo %s" % nombre)
        else:
            ok += 1
    print("[multi] sumario: ok=%s  !!! fallos=%s" % (ok, len(fallos)))
    for nom, msg in fallos:
        print("!!!   %s — %s" % (nom, msg))
    return 1 if fallos else 0
