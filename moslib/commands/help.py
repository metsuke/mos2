"""
Comando help de MetsuOS
Muestra comandos del sistema y de usuario por separado,
y ayuda específica indicando el origen del comando.
"""

import os
from pathlib import Path
import importlib.util

from moslib.core.user import get_username, get_user_mos_dir


def _load_help_from_file(file_path: Path) -> str:
    """Carga la función help() de un archivo de comando."""
    if not file_path.is_file():
        return None

    try:
        spec = importlib.util.spec_from_file_location(file_path.stem, str(file_path))
        if spec is None or spec.loader is None:
            return "Error al leer la ayuda del comando."

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "help"):
            return module.help()
        return "Sin descripción disponible."
    except Exception:
        return "Error al leer la ayuda del comando."


def _get_system_commands_dir() -> Path:
    return Path(__file__).resolve().parent


def _get_user_commands_dir() -> Path:
    return get_user_mos_dir(get_username()) / "commands"


def _list_commands(directory: Path) -> list[tuple[str, str]]:
    """Devuelve lista de (nombre, ayuda) de todos los .py de un directorio."""
    result = []
    if not directory.is_dir():
        return result

    for filename in sorted(directory.iterdir()):
        if filename.suffix == ".py" and not filename.name.startswith("__"):
            cmd_name = filename.stem
            help_text = _load_help_from_file(filename)
            result.append((cmd_name, help_text))
    return result


def execute(args):
    system_dir = _get_system_commands_dir()
    user_dir = _get_user_commands_dir()

    # =====================================================
    # CASO 1: help  (sin argumentos) → listar todo
    # =====================================================
    if len(args) == 0:
        print()
        print("=" * 60)
        print(" Comandos del sistema")
        print("=" * 60)

        system_cmds = _list_commands(system_dir)
        if system_cmds:
            for name, help_text in system_cmds:
                print(f"  {name.ljust(16)} - {help_text}")
        else:
            print("  (ninguno)")

        print()
        print("=" * 60)
        print(" Comandos de usuario")
        print("=" * 60)

        user_cmds = _list_commands(user_dir)
        if user_cmds:
            for name, help_text in user_cmds:
                # Mostramos también el nombre corto si es posible
                short_name = name[5:] if name.startswith("user_") else name
                display = f"{name}  (o solo '{short_name}')" if name.startswith("user_") else name
                print(f"  {display.ljust(32)} - {help_text}")
        else:
            print("  (ninguno todavía)")
            print("  Crea archivos user_*.py en:")
            print(f"  {user_dir}")

        print("=" * 60)
        print()
        return

    # =====================================================
    # CASO 2: help <comando>  → ayuda específica
    # =====================================================
    cmd_name = args[0]

    # 1. ¿Es un comando del sistema?
    system_file = system_dir / f"{cmd_name}.py"
    if system_file.is_file():
        help_text = _load_help_from_file(system_file)
        print()
        print(f"[Comando del sistema]  {cmd_name}")
        print("-" * 50)
        print(help_text)
        print()
        return

    # 2. ¿El usuario escribió el nombre completo con prefijo?
    if cmd_name.startswith("user_"):
        user_file = user_dir / f"{cmd_name}.py"
        if user_file.is_file():
            help_text = _load_help_from_file(user_file)
            print()
            print(f"[Comando de usuario]  {cmd_name}")
            print("-" * 50)
            print(help_text)
            print()
            return

    # 3. Nombre corto → buscar user_<nombre>
    user_file = user_dir / f"user_{cmd_name}.py"
    if user_file.is_file():
        help_text = _load_help_from_file(user_file)
        print()
        print(f"[Comando de usuario]  user_{cmd_name}  (también invocable como '{cmd_name}')")
        print("-" * 50)
        print(help_text)
        print()
        return

    # No encontrado
    print(f"help: comando no encontrado: '{cmd_name}'")


def help():
    return "Uso: help [comando] - Muestra la lista de comandos (sistema + usuario) o la ayuda de uno específico."