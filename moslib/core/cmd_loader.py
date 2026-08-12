"""
moslib.core.cmd_loader
Cargador dinámico de comandos con soporte de espacio de usuario.

Reglas:
- Los comandos del sistema tienen prioridad absoluta.
- Los archivos de usuario DEBEN llamarse user_*.py
- Un comando de usuario se puede invocar de dos formas:
    1. Con el prefijo completo:   user_hola
    2. Sin el prefijo (hola) SOLO si no existe un comando del sistema con ese nombre.
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
        """Carga o recarga un módulo desde disco (hot-reload)."""
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
        # -------------------------------------------------
        # 1. Prioridad absoluta: comandos del sistema
        # -------------------------------------------------
        system_file = self.system_commands_dir / f"{cmd_name}.py"
        if system_file.is_file():
            return self._load_module(cmd_name, system_file)

        if not self.user_commands_dir:
            return None

        # -------------------------------------------------
        # 2. El usuario escribió el nombre completo con prefijo
        #    Ejemplo: user_hola  →  busca user_hola.py
        # -------------------------------------------------
        if cmd_name.startswith("user_"):
            user_file = self.user_commands_dir / f"{cmd_name}.py"
            if user_file.is_file():
                return self._load_module(cmd_name, user_file)
            return None

        # -------------------------------------------------
        # 3. El usuario escribió el nombre corto (sin prefijo)
        #    Solo se permite si NO existe un comando del sistema
        #    con ese nombre (ya lo comprobamos arriba).
        #    Ejemplo: hola  →  busca user_hola.py
        # -------------------------------------------------
        user_file = self.user_commands_dir / f"user_{cmd_name}.py"
        if user_file.is_file():
            return self._load_module(f"user_{cmd_name}", user_file)

        return None