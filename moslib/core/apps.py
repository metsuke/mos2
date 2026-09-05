"""
moslib.core.apps
Apps locales y desde repositorio git.
Destino: usuario (.mos/apps) o sistema (rootfs/opt/apps).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from moslib.core.security import validate_command_file
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
    if not all(k in data for k in REQUIRED):
        return None
    if not isinstance(data["comandos"], list):
        return None
    if "ambito" not in data:
        data["ambito"] = "usuario"
    if data["ambito"] not in AMBITOS:
        return None
    return data


def _dest_root(ambito: str) -> Path:
    if ambito == "sistema":
        return _system_root()
    return _user_root()


def list_apps() -> list[dict]:
    found = []
    for root, ambito_fijo in ((_system_root(), "sistema"), (_user_root(), "usuario")):
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            meta = _read_meta(child)
            if meta:
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


def _validate_source(src: Path) -> tuple[dict | None, list[str]]:
    errors = []
    meta = _read_meta(src)
    if meta is None:
        return None, [
            "Falta app.json válido (id, nombre, version, comandos, acceso, ambito usuario|sistema)."
        ]
    if meta.get("acceso") not in ("local-owner", "system"):
        errors.append("acceso debe ser local-owner o system.")
    if meta.get("ambito") == "sistema" and meta.get("acceso") == "local-owner":
        errors.append("ambito=sistema requiere acceso=system.")
    system = _system_command_names()
    for name in meta["comandos"]:
        if name in system:
            errors.append(f"El comando '{name}' pisa un comando de sistema.")
        cmd_file = src / "commands" / f"{name}.py"
        if not cmd_file.is_file():
            errors.append(f"No está commands/{name}.py")
            continue
        ok, sec_err = validate_command_file(cmd_file, app_dir=src)
        if not ok:
            errors.extend(sec_err)
    if errors:
        return meta, errors
    return meta, []


def _copy_install(src: Path, meta: dict) -> tuple[bool, str]:
    dest = _dest_root(meta["ambito"]) / meta["id"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return True, f"App '{meta['id']}' instalada en ámbito {meta['ambito']}."


def install_from_path(src: str | Path) -> tuple[bool, str]:
    path = resolve_source(src)
    if not path.is_dir():
        return False, f"No es un directorio: {path}"
    meta, errors = _validate_source(path)
    if errors:
        return False, "No se acepta la app:\n  - " + "\n  - ".join(errors)
    return _copy_install(path, meta)


def install_from_repo(url: str, ref: str | None = None) -> tuple[bool, str]:
    cache = get_project_root() / ".mos-cache" / "app-repos"
    cache.mkdir(parents=True, exist_ok=True)
    name = url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    dest = cache / name
    try:
        if dest.exists():
            subprocess.run(
                ["git", "fetch", "--all"],
                cwd=str(dest),
                check=True,
                capture_output=True,
                text=True,
            )
            if ref:
                subprocess.run(
                    ["git", "checkout", ref],
                    cwd=str(dest),
                    check=True,
                    capture_output=True,
                    text=True,
                )
        else:
            cmd = ["git", "clone", url, str(dest)]
            if ref:
                cmd = ["git", "clone", "--branch", ref, url, str(dest)]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        return False, f"No se pudo clonar o actualizar el repo: {exc}"
    return install_from_path(dest)


def remove_app(app_id: str) -> tuple[bool, str]:
    for root in (_system_root(), _user_root()):
        dest = root / app_id
        if dest.is_dir():
            shutil.rmtree(dest)
            return True, f"App '{app_id}' eliminada de {root}."
    return False, f"No hay app instalada '{app_id}'."