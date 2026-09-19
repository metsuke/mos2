"""Validar e instalar / quitar apps."""

from __future__ import annotations

import shutil
from pathlib import Path

from moslib.core.security import validate_command_file


def _validate_source(src: Path) -> tuple[dict | None, list[str]]:
    from moslib.core.apps import _read_meta, _system_command_names

    errors = []
    meta = _read_meta(src)
    if meta is None:
        return None, ["Falta app.json válido."]
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
    return meta, errors


def _copy_install(src: Path, meta: dict) -> tuple[bool, str]:
    from moslib.core.apps import _dest_root

    dest = _dest_root(meta["ambito"]) / meta["id"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return True, f"App '{meta['id']}' instalada en ámbito {meta['ambito']}."


def install_from_path(src: str | Path) -> tuple[bool, str]:
    from moslib.core.apps import resolve_source

    path = resolve_source(src)
    if not path.is_dir():
        return False, f"No es un directorio: {path}"
    meta, errors = _validate_source(path)
    if errors:
        return False, "No se acepta la app:\n  - " + "\n  - ".join(errors)
    return _copy_install(path, meta)


def remove_app(app_id: str) -> tuple[bool, str]:
    from moslib.core.apps import _system_root, _user_root

    for root in (_system_root(), _user_root()):
        dest = root / app_id
        if dest.is_dir():
            shutil.rmtree(dest)
            return True, f"App '{app_id}' eliminada de {root}."
    return False, f"No hay app instalada '{app_id}'."
