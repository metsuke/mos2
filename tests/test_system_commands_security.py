"""
Tests de seguridad: todos los comandos del sistema deben pasar la validación de imports.
"""

from pathlib import Path
from moslib.core.security import validate_command_file

COMMANDS_DIR = Path(__file__).resolve().parent.parent / "moslib" / "commands"


def test_all_system_commands_pass_security():
    """Ningún comando del sistema puede tener imports prohibidos."""
    assert COMMANDS_DIR.is_dir(), f"No existe el directorio de comandos: {COMMANDS_dir}"

    py_files = list(COMMANDS_DIR.glob("*.py"))
    assert len(py_files) > 0, "No se encontraron comandos del sistema"

    errors_found = []
    for path in sorted(py_files):
        if path.name.startswith("__"):
            continue
        ok, errors = validate_command_file(path)
        if not ok:
            errors_found.append(f"{path.name}: {errors}")

    assert not errors_found, "Comandos del sistema con imports prohibidos:\n" + "\n".join(errors_found)


def test_each_system_command_has_execute_and_help():
    """Cada comando del sistema debe tener las funciones execute y help."""
    import importlib.util

    for path in sorted(COMMANDS_DIR.glob("*.py")):
        if path.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert hasattr(module, "execute"), f"{path.name} no tiene función execute()"
        assert callable(module.execute), f"{path.name}: execute no es callable"
        assert hasattr(module, "help"), f"{path.name} no tiene función help()"
        assert callable(module.help), f"{path.name}: help no es callable"