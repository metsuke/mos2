"""Lote: pegar, :e ejecuta, :q cancela. write consume hasta el punto."""

import shlex
import sys
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
    aqui = Path(__file__).resolve().parent
    return CommandManager(
        system_commands_dir=aqui,
        user_commands_dir=get_user_mos_dir(get_username()) / "commands",
        apps_root=get_user_apps_dir(),
        system_apps_root=get_system_apps_dir(),
        enforce_security=True,
    )


def _meta(line: str) -> str:
    s = line.strip()
    return ":" + s[1:] if s.startswith(";") else s


def _eco(line: str) -> None:
    s = line.strip()
    if len(s) > 80 and not s.startswith(("write ", "w ", "docgen ", ":")):
        print(f"[multi] + ({len(s)} chars)")
        return
    print(f"[multi] + {s}")


def execute(args):
    print("[multi] Pega comandos. :e ejecuta  |  :q cancela")
    lote = []
    while True:
        try:
            bruto = sys.stdin.readline()
        except (EOFError, KeyboardInterrupt):
            print("[multi] Cancelado.")
            return
        if bruto == "":
            print("[multi] Cancelado.")
            return
        line = bruto.replace("\r", "").rstrip("\n")
        if not line.strip():
            continue
        meta = _meta(line).lower()
        if meta == ":q":
            print("[multi] Cancelado.")
            return
        if meta in (":e", ":w"):
            _lanzar(lote)
            return
        lote.append(line)
        _eco(line)


def _lanzar(lote: list[str]) -> None:
    if not lote:
        print("[multi] Lote vacio.")
        return
    mgr = _manager()
    print(f"[multi] Ejecutando lote ({len(lote)} linea(s)).")
    i = 0
    while i < len(lote):
        line = lote[i]
        try:
            parts = shlex.split(line, posix=True)
        except ValueError as exc:
            print(f"[multi] comillas rotas: {exc}")
            i += 1
            continue
        if not parts:
            i += 1
            continue
        nombre, args = parts[0], parts[1:]
        print(f"mosh$ {nombre} {' '.join(args)}")
        if nombre in ("multi", "m"):
            i += 1
            continue
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
                if mod and hasattr(mod, "execute"):
                    mod.execute(args, payload)
                else:
                    print("mosh: write no encontrado")
            finally:
                write_b64.PERMISO_MULTI = False
            continue
        mod = mgr.get_command(nombre)
        if mod and hasattr(mod, "execute"):
            mod.execute(args)
        else:
            print(f"mosh: comando no encontrado: {nombre}")
        i += 1


def help():
    return "Uso: multi (o m) o ./write.sh. :e ejecuta, :q cancela."


def sinopsis():
    return ["multi", "m"]