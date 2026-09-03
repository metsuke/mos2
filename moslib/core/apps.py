"""
moslib.core.apps
Apps locales: instalar desde path, listar, metadatos, quitar.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from moslib.core.security import validate_command_file
from moslib.core.user import ensure_user_space, get_project_root, get_user_apps_dir


META_NAME = "app.json"
REQUIRED = ("id", "nombre", "version", "comandos", "acceso")


def _apps_root() -> Path:
    ensure_user_space()
    root = get_user_apps_dir()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _system_command_names() -> set[str]:
    d = get_project_root() / "moslib" / "commands"
    if not d.is_dir():
        return set()
    return {p.stem for p in d.glob("*.py") if p.stem != "__init__"}


def _read_meta(app_dir: Path) -> dict | None:
    meta_file = app_dir / META_NAME
    if not meta_file.is_file():
        return None
    try:
        data = json.loads(meta_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not all(k in data for k in REQUIRED):
        return None
    if not isinstance(data["comandos"], list):
        return None
    return data


def list_apps() -> list[dict]:
    root = _apps_root()
    found = []
    for child in sorted(root.iterdir()) if root.is_dir() else []:
        if not child.is_dir():
            continue
        meta = _read_meta(child)
        if meta:
            found.append(meta)
    return found


def show_app(app_id: str) -> dict | None:
    for meta in list_apps():
        if meta["id"] == app_id:
            return meta
    return None


def _validate_source(src: Path) -> tuple[dict | None, list[str]]:
    errors = []
    meta = _read_meta(src)
    if meta is None:
        return None, ["Falta app.json válido (id, nombre, version, comandos, acceso)."]
    if meta.get("acceso") != "local-owner":
        errors.append("En 07 solo se admite acceso local-owner.")
    system = _system_command_names()
    for name in meta["comandos"]:
        if name in system:
            errors.append(f"El comando '{name}' pisa un comando de sistema.")
        cmd_file = src / "commands" / f"{name}.py"
        if not cmd_file.is_file():
            errors.append(f"No está commands/{name}.py")
            continue
        ok, sec_err = validate_command_file(cmd_file)
        if not ok:
            errors.extend(sec_err)
    if errors:
        return meta, errors
    return meta, []


def install_from_path(src: str | Path) -> tuple[bool, str]:
    src = Path(src).expanduser().resolve()
    if not src.is_dir():
        return False, f"No es un directorio: {src}"
    meta, errors = _validate_source(src)
    if errors:
        return False, "No se acepta la app:\n  - " + "\n  - ".join(errors)
    dest = _apps_root() / meta["id"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return True, f"App '{meta['id']}' instalada en espacio de usuario."


def remove_app(app_id: str) -> tuple[bool, str]:
    dest = _apps_root() / app_id
    if not dest.is_dir():
        return False, f"No hay app instalada '{app_id}'."
    shutil.rmtree(dest)
    return True, f"App '{app_id}' eliminada."