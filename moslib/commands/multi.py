"""Lote: pegar, :e ejecuta, :q cancela. write consume hasta el punto."""

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
    aqui = Path(__file__).resolve().parent
    return CommandManager(
        system_commands_dir=aqui,
        user_commands_dir=get_user_mos_dir(get_username()) / "commands",
        apps_root=get_user_apps_dir(),
        system_apps_root=get_system_apps_dir(),
        enforce_security=True,
    )


def _partir(bruto: str) -> list[str]:
    out = []
    for line in bruto.replace("\r\n", "\n").split("\n"):
        line = line.strip()
        if line:
            out.append(line)
    return out


def execute(args):
    print("[multi] Pega comandos, uno por línea.")
    print("[multi] :e  ejecuta el lote   |   :q  cancela")
    lote = []
    while True:
        try:
            bruto = input("multi> ")
        except (EOFError, KeyboardInterrupt):
            print("[multi] Cancelado.")
            return
        for line in _partir(bruto):
            if line in (":q", ":Q"):
                print("[multi] Cancelado.")
                return
            if line in (":e", ":E", ":w"):
                _lanzar(lote)
                return
            lote.append(line)
            print(f"[multi] + {line}")


def _lanzar(lote: list[str]) -> None:
    if not lote:
        print("[multi] Lote vacío.")
        return
    mgr = _manager()
    print(f"[multi] Ejecutando lote ({len(lote)} línea(s)).")
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
        print(f"mosh$ {line}")
        if nombre in ("multi", "m"):
            print("[multi] ignorado (no anidar).")
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
    return "Uso: multi (o m) - Lote. :e ejecuta, :q cancela. write lee hasta ."


def sinopsis():
    return ["multi", "m"]