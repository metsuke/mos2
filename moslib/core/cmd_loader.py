"""
moslib.core.cmd_loader
Cargador dinámico de comandos: sistema, usuario y apps instaladas.
Validación de seguridad obligatoria.
"""

import os
import importlib.util
from pathlib import Path

from moslib.core.security import validate_command_file


class CommandManager:
    def __init__(
        self,
        system_commands_dir: str | Path,
        user_commands_dir: str | Path | None = None,
        apps_root: str | Path | None = None,
        enforce_security: bool = True,
    ):
        self.system_commands_dir = Path(system_commands_dir)
        self.user_commands_dir = Path(user_commands_dir) if user_commands_dir else None
        self.apps_root = Path(apps_root) if apps_root else None
        self.enforce_security = enforce_security

        self.cache = {}
        self.mtimes = {}

    def _load_module(self, cmd_name: str, file_path: Path):
        if self.enforce_security:
            ok, errors = validate_command_file(file_path)
            if not ok:
                print(f"[SEGURIDAD] Comando '{cmd_name}' rechazado:")
                for err in errors:
                    print(f"  - {err}")
                return None

        current_mtime = os.path.getmtime(file_path)

        if cmd_name in self.cache and self.mtimes.get(cmd_name) == current_mtime:
            return self.cache[cmd_name]

        spec = importlib.util.spec_from_file_location(cmd_name, str(file_path))
        if spec is None or spec.loader is None:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.cache[cmd_name] = module
        self.mtimes[cmd_name] = current_mtime
        return module

    def _system_names(self) -> set[str]:
        if not self.system_commands_dir.is_dir():
            return set()
        return {
            p.stem
            for p in self.system_commands_dir.glob("*.py")
            if p.stem != "__init__"
        }

    def _app_command_file(self, cmd_name: str) -> Path | None:
        if not self.apps_root or not self.apps_root.is_dir():
            return None
        if cmd_name in self._system_names():
            return None
        for child in sorted(self.apps_root.iterdir()):
            if not child.is_dir():
                continue
            candidate = child / "commands" / f"{cmd_name}.py"
            if candidate.is_file():
                return candidate
        return None

    def get_command(self, cmd_name: str):
        system_file = self.system_commands_dir / f"{cmd_name}.py"
        if system_file.is_file():
            return self._load_module(cmd_name, system_file)

        if self.user_commands_dir:
            if cmd_name.startswith("user_"):
                user_file = self.user_commands_dir / f"{cmd_name}.py"
                if user_file.is_file():
                    return self._load_module(cmd_name, user_file)
            else:
                user_file = self.user_commands_dir / f"user_{cmd_name}.py"
                if user_file.is_file():
                    return self._load_module(f"user_{cmd_name}", user_file)

        app_file = self._app_command_file(cmd_name)
        if app_file is not None:
            return self._load_module(cmd_name, app_file)

        return None