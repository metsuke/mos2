"""
Comando help de MetsuOS
Sistema, apps de sistema, apps de usuario, comandos user_.
"""

import importlib.util
from pathlib import Path

from moslib.core.cmd_loader import invocation_names
from moslib.core.user import (
    get_username,
    get_user_mos_dir,
    get_user_apps_dir,
    get_system_apps_dir,
)


def _load_help_from_file(file_path: Path) -> str:
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
    result = []
    if not directory.is_dir():
        return result
    for filename in sorted(directory.iterdir()):
        if filename.suffix == ".py" and not filename.name.startswith("__"):
            result.append((filename.stem, _load_help_from_file(filename)))
    return result


def _list_app_commands(root: Path) -> list[tuple[str, str, str]]:
    result = []
    if not root.is_dir():
        return result
    for app_dir in sorted(root.iterdir()):
        cmd_dir = app_dir / "commands"
        if not cmd_dir.is_dir():
            continue
        aid = app_dir.name
        for filename in sorted(cmd_dir.glob("*.py")):
            if filename.stem.startswith("__"):
                continue
            aliases = " ".join(sorted(invocation_names(aid, filename.stem)))
            result.append((filename.stem, aliases, _load_help_from_file(filename)))
    return result


def _find_app_file(cmd_name: str, root: Path) -> Path | None:
    if not root.is_dir():
        return None
    for app_dir in sorted(root.iterdir()):
        cmd_dir = app_dir / "commands"
        if not cmd_dir.is_dir():
            continue
        aid = app_dir.name
        for filename in cmd_dir.glob("*.py"):
            if cmd_name in invocation_names(aid, filename.stem):
                return filename
    return None


def execute(args):
    system_dir = _get_system_commands_dir()
    user_dir = _get_user_commands_dir()
    sys_apps = get_system_apps_dir()
    usr_apps = get_user_apps_dir()

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
        print(" Comandos de app (sistema)")
        print("=" * 60)
        sapps = _list_app_commands(sys_apps)
        if sapps:
            for name, aliases, help_text in sapps:
                print(f"  {name}  [{aliases}]")
                print(f"      {help_text}")
        else:
            print("  (ninguno)")

        print()
        print("=" * 60)
        print(" Comandos de app (usuario)")
        print("=" * 60)
        uapps = _list_app_commands(usr_apps)
        if uapps:
            for name, aliases, help_text in uapps:
                print(f"  {name}  [{aliases}]")
                print(f"      {help_text}")
        else:
            print("  (ninguno)")

        print()
        print("=" * 60)
        print(" Comandos de usuario")
        print("=" * 60)
        user_cmds = _list_commands(user_dir)
        if user_cmds:
            for name, help_text in user_cmds:
                short_name = name[5:] if name.startswith("user_") else name
                display = (
                    f"{name}  (o solo '{short_name}')"
                    if name.startswith("user_")
                    else name
                )
                print(f"  {display.ljust(32)} - {help_text}")
        else:
            print("  (ninguno todavía)")
            print("  Crea archivos user_*.py en:")
            print(f"  {user_dir}")

        print("=" * 60)
        print()
        return

    cmd_name = args[0]

    system_file = system_dir / f"{cmd_name}.py"
    if system_file.is_file():
        print()
        print(f"[Comando del sistema]  {cmd_name}")
        print("-" * 50)
        print(_load_help_from_file(system_file))
        print()
        return

    app_sys = _find_app_file(cmd_name, sys_apps)
    if app_sys is not None:
        print()
        print(f"[Comando de app de sistema]  {app_sys.stem}")
        print("-" * 50)
        print(_load_help_from_file(app_sys))
        print()
        return

    app_usr = _find_app_file(cmd_name, usr_apps)
    if app_usr is not None:
        print()
        print(f"[Comando de app de usuario]  {app_usr.stem}")
        print("-" * 50)
        print(_load_help_from_file(app_usr))
        print()
        return

    if cmd_name.startswith("user_"):
        user_file = user_dir / f"{cmd_name}.py"
        if user_file.is_file():
            print()
            print(f"[Comando de usuario]  {cmd_name}")
            print("-" * 50)
            print(_load_help_from_file(user_file))
            print()
            return

    user_file = user_dir / f"user_{cmd_name}.py"
    if user_file.is_file():
        print()
        print(f"[Comando de usuario]  user_{cmd_name}  (también '{cmd_name}')")
        print("-" * 50)
        print(_load_help_from_file(user_file))
        print()
        return

    print(f"help: comando no encontrado: '{cmd_name}'")


def help():
    return (
        "Uso: help [comando] - Lista sistema, apps y usuario, "
        "o la ayuda de uno indicando el origen."
    )