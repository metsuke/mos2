"""
moslib.core.cmd_loader
Cargador dinámico de comandos con soporte de espacio de usuario.

Reglas estrictas:
- Los comandos del sistema tienen prioridad absoluta.
- Los comandos de usuario SOLO se cargan si empiezan por 'user_'.
- El usuario NUNCA puede sobrescribir un comando del sistema.
"""

import os
import importlib.util
from pathlib import Path


class CommandManager:
    def __init__(
        self,
        system_commands_dir: str | Path,
        user_commands_dir: str | Path | None = None,
    ):
        self.system_commands_dir = Path(system_commands_dir)
        self.user_commands_dir = Path(user_commands_dir) if user_commands_dir else None

        self.cache = {}
        self.mtimes = {}

    def _load_module(self, cmd_name: str, file_path: Path):
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

    def get_command(self, cmd_name: str):
        # 1. Comandos del sistema (prioridad absoluta)
        system_file = self.system_commands_dir / f"{cmd_name}.py"
        if system_file.is_file():
            return self._load_module(cmd_name, system_file)

        # 2. Comandos de usuario (solo con prefijo user_)
        if self.user_commands_dir and cmd_name.startswith("user_"):
            user_file = self.user_commands_dir / f"{cmd_name}.py"
            if user_file.is_file():
                return self._load_module(cmd_name, user_file)

        return None