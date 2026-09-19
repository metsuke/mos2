"""Carga de módulos de comando (cache + minimoslib)."""

from __future__ import annotations

import os
import sys
import importlib.util
from pathlib import Path

from moslib.core.security import validate_command_file


def load_minimoslib(app_dir: Path) -> None:
    init = app_dir / "minimoslib" / "__init__.py"
    if not init.is_file():
        return
    spec = importlib.util.spec_from_file_location(
        "minimoslib",
        init,
        submodule_search_locations=[str(app_dir / "minimoslib")],
    )
    if spec is None or spec.loader is None:
        return
    mod = importlib.util.module_from_spec(spec)
    sys.modules["minimoslib"] = mod
    spec.loader.exec_module(mod)


def load_module(mgr, cmd_name: str, file_path: Path, app_dir: Path | None = None):
    if mgr.enforce_security:
        ok, errors = validate_command_file(file_path, app_dir=app_dir)
        if not ok:
            print(f"[SEGURIDAD] Comando '{cmd_name}' rechazado:")
            for err in errors:
                print(f"  - {err}")
            return None
    current_mtime = os.path.getmtime(file_path)
    cache_key = str(file_path)
    if cache_key in mgr.cache and mgr.mtimes.get(cache_key) == current_mtime:
        return mgr.cache[cache_key]
    prev = sys.modules.get("minimoslib")
    try:
        if app_dir is not None:
            load_minimoslib(app_dir)
        spec = importlib.util.spec_from_file_location(cmd_name, str(file_path))
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if prev is not None:
            sys.modules["minimoslib"] = prev
        elif "minimoslib" in sys.modules and app_dir is not None:
            del sys.modules["minimoslib"]
    mgr.cache[cache_key] = module
    mgr.mtimes[cache_key] = current_mtime
    return module
