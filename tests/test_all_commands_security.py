"""
Validación de seguridad de TODOS los comandos existentes.
Si cualquier comando (sistema o usuario actual) viola la política de imports,
el test falla y el sistema no debe arrancar.
"""

from pathlib import Path
from moslib.core.security import validate_command_file
from moslib.core.user import get_username, get_user_mos_dir, get_project_root


def _collect_command_files():
    files = []

    # Comandos del sistema
    system_dir = get_project_root() / "moslib" / "commands"
    if system_dir.is_dir():
        for path in sorted(system_dir.glob("*.py")):
            if not path.name.startswith("__"):
                files.append(("system", path))

    # Comandos del usuario actual
    user_dir = get_user_mos_dir(get_username()) / "commands"
    if user_dir.is_dir():
        for path in sorted(user_dir.glob("*.py")):
            if not path.name.startswith("__"):
                files.append(("user", path))

    return files


def test_all_existing_commands_pass_security():
    files = _collect_command_files()
    assert files, "No se encontraron comandos para validar"

    errors_found = []
    for origin, path in files:
        ok, errors = validate_command_file(path)
        if not ok:
            errors_found.append(f"[{origin}] {path}: {errors}")

    assert not errors_found, (
        "Se encontraron comandos con imports prohibidos:\n" + "\n".join(errors_found)
    )


def test_all_system_commands_have_execute_and_help():
    """Los comandos del sistema deben exponer execute() y help()."""
    import importlib.util

    system_dir = get_project_root() / "moslib" / "commands"
    for path in sorted(system_dir.glob("*.py")):
        if path.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert hasattr(module, "execute") and callable(module.execute), (
            f"{path.name} no tiene execute() callable"
        )
        assert hasattr(module, "help") and callable(module.help), (
            f"{path.name} no tiene help() callable"
        )