"""
moslib.core.cmd_loader
Cargador dinámico de comandos con soporte de espacio de usuario
y validación de seguridad obligatoria.
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
        enforce_security: bool = True,
    ):
        self.system_commands_dir = Path(system_commands_dir)
        self.user_commands_dir = Path(user_commands_dir) if user_commands_dir else None
        self.enforce_security = enforce_security

        self.cache = {}
        self.mtimes = {}

    def _load_module(self, cmd_name: str, file_path: Path):
        """Carga o recarga un módulo desde disco (hot-reload) con validación de seguridad."""
        # Validación de seguridad obligatoria
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

    def get_command(self, cmd_name: str):
        # 1. Prioridad absoluta: comandos del sistema
        system_file = self.system_commands_dir / f"{cmd_name}.py"
        if system_file.is_file():
            return self._load_module(cmd_name, system_file)

        if not self.user_commands_dir:
            return None

        # 2. Nombre completo con prefijo user_
        if cmd_name.startswith("user_"):
            user_file = self.user_commands_dir / f"{cmd_name}.py"
            if user_file.is_file():
                return self._load_module(cmd_name, user_file)
            return None

        # 3. Nombre corto → buscar user_<nombre>
        user_file = self.user_commands_dir / f"user_{cmd_name}.py"
        if user_file.is_file():
            return self._load_module(f"user_{cmd_name}", user_file)

        return None