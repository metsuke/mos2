"""Apps locales. Git: apps_git. Validación: apps_val."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.apps_git import install_from_repo
from moslib.core.apps_val import install_from_path, remove_app
from moslib.core.user import (
    ensure_user_space,
    get_project_root,
    get_system_apps_dir,
    get_user_apps_dir,
)

META_NAME = "app.json"
REQUIRED = ("id", "nombre", "version", "comandos", "acceso")
AMBITOS = ("usuario", "sistema")


def _user_root() -> Path:
    ensure_user_space()
    root = get_user_apps_dir()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _system_root() -> Path:
    return get_system_apps_dir()


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
    if not all(k in data for k in REQUIRED) or not isinstance(data["comandos"], list):
        return None
    if "ambito" not in data:
        data["ambito"] = "usuario"
    if data["ambito"] not in AMBITOS:
        return None
    return data


def _dest_root(ambito: str) -> Path:
    return _system_root() if ambito == "sistema" else _user_root()


def list_apps() -> list[dict]:
    found = []
    for root, ambito_fijo in ((_system_root(), "sistema"), (_user_root(), "usuario")):
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            meta = _read_meta(child)
            if not meta:
                continue
            meta = dict(meta)
            meta["ambito"] = meta.get("ambito", ambito_fijo)
            meta["_path"] = str(child)
            found.append(meta)
    return found


def show_app(app_id: str) -> dict | None:
    for meta in list_apps():
        if meta["id"] == app_id:
            return meta
    return None


def resolve_source(src: str | Path) -> Path:
    raw = Path(src).expanduser()
    if raw.is_absolute():
        return raw.resolve()
    return (get_project_root() / raw).resolve()
