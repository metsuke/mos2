"""Validación del contrato de comandos del sistema."""

import importlib.util
from pathlib import Path

from moslib.core.user import get_project_root


COMMANDS_DIR = get_project_root() / "moslib" / "commands"


def _iter_system_command_files():
    assert COMMANDS_DIR.is_dir(), f"No existe {COMMANDS_DIR}"
    for path in sorted(COMMANDS_DIR.glob("*.py")):
        if path.name.startswith("__"):
            continue
        yield path


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_system_commands_have_execute_and_help():
    files = list(_iter_system_command_files())
    assert files, "No se encontraron comandos del sistema"

    for path in files:
        module = _load_module(path)
        assert hasattr(module, "execute"), f"{path.name} no define execute"
        assert callable(module.execute), f"{path.name}: execute no es callable"
        assert hasattr(module, "help"), f"{path.name} no define help"
        assert callable(module.help), f"{path.name}: help no es callable"


def test_all_system_command_help_returns_str():
    for path in _iter_system_command_files():
        module = _load_module(path)
        result = module.help()
        assert isinstance(result, str), f"{path.name}: help() debe devolver str"
        assert result.strip(), f"{path.name}: help() no debe devolver cadena vacía"