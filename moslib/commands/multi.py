"""Lote de líneas: pegar primero, ejecutar con :e, cancelar con :q."""

from pathlib import Path

from moslib.core.cmd_loader import CommandManager
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
        except EOFError:
            print("[multi] Cancelado.")
            return
        except KeyboardInterrupt:
            print("\n[multi] Cancelado.")
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
    print(f"[multi] Ejecutando {len(lote)} línea(s).")
    for line in lote:
        parts = line.split()
        nombre, args = parts[0], parts[1:]
        print(f"mosh$ {line}")
        if nombre in ("multi", "m"):
            print("[multi] ignorado (no anidar).")
            continue
        mod = mgr.get_command(nombre)
        if mod and hasattr(mod, "execute"):
            mod.execute(args)
        else:
            print(f"mosh: comando no encontrado: {nombre}")


def help():
    return (
        "Uso: multi (o m) - Entra en lote. Pega líneas, :e ejecuta, :q cancela."
    )


def sinopsis():
    return ["multi", "m"]