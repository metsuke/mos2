"""Carga de help() desde ficheros de comando. No es un comando."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from moslib.core.cmd_loader import invocation_names
from moslib.core.user import get_username, get_user_mos_dir


def load_help_from_file(file_path: Path) -> str:
    if not file_path.is_file():
        return "Sin descripción disponible."
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


def system_commands_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "commands"


def user_commands_dir() -> Path:
    return get_user_mos_dir(get_username()) / "commands"


def list_commands(directory: Path) -> list[tuple[str, str]]:
    result = []
    if not directory.is_dir():
        return result
    for filename in sorted(directory.iterdir()):
        if filename.suffix == ".py" and not filename.name.startswith("__"):
            result.append((filename.stem, load_help_from_file(filename)))
    return result


def list_app_commands(root: Path) -> list[tuple[str, str, str]]:
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
            result.append((filename.stem, aliases, load_help_from_file(filename)))
    return result


def find_app_file(cmd_name: str, root: Path) -> Path | None:
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


def print_bloque(titulo: str, lineas: list[str]) -> None:
    print()
    print("=" * 60)
    print(f" {titulo}")
    print("=" * 60)
    if lineas:
        for linea in lineas:
            print(linea)
    else:
        print("  (ninguno)")