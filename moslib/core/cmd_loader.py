"""
moslib.core.cmd_loader
Cargador de comandos: sistema > app sistema > app usuario > user_.
Al cargar un comando de app inyecta el minimoslib de ESA app.
"""

import os
import sys
import importlib.util
from pathlib import Path

from moslib.core.security import validate_command_file


def invocation_names(app_id: str, stem: str) -> set[str]:
    names = {stem}
    prefix = f"app_{app_id}_"
    if stem.startswith(prefix):
        rest = stem[len(prefix) :]
        if rest:
            names.add(f"{app_id}_{rest}")
            names.add(rest)
    return names


class CommandManager:
    def __init__(
        self,
        system_commands_dir: str | Path,
        user_commands_dir: str | Path | None = None,
        apps_root: str | Path | None = None,
        system_apps_root: str | Path | None = None,
        enforce_security: bool = True,
    ):
        self.system_commands_dir = Path(system_commands_dir)
        self.user_commands_dir = Path(user_commands_dir) if user_commands_dir else None
        self.apps_root = Path(apps_root) if apps_root else None
        self.system_apps_root = Path(system_apps_root) if system_apps_root else None
        self.enforce_security = enforce_security
        self.cache = {}
        self.mtimes = {}

    def _system_names(self) -> set[str]:
        if not self.system_commands_dir.is_dir():
            return set()
        return {
            p.stem
            for p in self.system_commands_dir.glob("*.py")
            if p.stem != "__init__"
        }

    def _iter_apps(self, root: Path | None):
        if not root or not root.is_dir():
            return
        for child in sorted(root.iterdir()):
            if child.is_dir() and (child / "commands").is_dir():
                yield child

    def _find_in_apps(self, cmd_name: str, root: Path | None) -> Path | None:
        if cmd_name in self._system_names():
            return None
        for app_dir in self._iter_apps(root):
            aid = app_dir.name
            for py in (app_dir / "commands").glob("*.py"):
                if py.stem == "__init__":
                    continue
                if cmd_name in invocation_names(aid, py.stem):
                    return py
        return None

    def _load_minimoslib(self, app_dir: Path) -> None:
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

    def _load_module(self, cmd_name: str, file_path: Path, app_dir: Path | None = None):
        if self.enforce_security:
            ok, errors = validate_command_file(file_path, app_dir=app_dir)
            if not ok:
                print(f"[SEGURIDAD] Comando '{cmd_name}' rechazado:")
                for err in errors:
                    print(f"  - {err}")
                return None

        current_mtime = os.path.getmtime(file_path)
        cache_key = str(file_path)
        if cache_key in self.cache and self.mtimes.get(cache_key) == current_mtime:
            return self.cache[cache_key]

        prev = sys.modules.get("minimoslib")
        try:
            if app_dir is not None:
                self._load_minimoslib(app_dir)
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

        self.cache[cache_key] = module
        self.mtimes[cache_key] = current_mtime
        return module

    def get_command(self, cmd_name: str):
        system_file = self.system_commands_dir / f"{cmd_name}.py"
        if system_file.is_file():
            return self._load_module(cmd_name, system_file)

        app_sys = self._find_in_apps(cmd_name, self.system_apps_root)
        if app_sys is not None:
            return self._load_module(cmd_name, app_sys, app_dir=app_sys.parent.parent)

        app_usr = self._find_in_apps(cmd_name, self.apps_root)
        if app_usr is not None:
            return self._load_module(cmd_name, app_usr, app_dir=app_usr.parent.parent)

        if self.user_commands_dir:
            if cmd_name.startswith("user_"):
                user_file = self.user_commands_dir / f"{cmd_name}.py"
                if user_file.is_file():
                    return self._load_module(cmd_name, user_file)
            else:
                user_file = self.user_commands_dir / f"user_{cmd_name}.py"
                if user_file.is_file():
                    return self._load_module(f"user_{cmd_name}", user_file)

        return None