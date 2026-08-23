"""Validación básica de estilo en módulos core."""

import ast
from pathlib import Path

from moslib.core.user import get_project_root


CORE_DIR = get_project_root() / "moslib" / "core"
REQUIRED_CORE_MODULES = (
    "shell.py",
    "cmd_loader.py",
    "user.py",
    "security.py",
)


def test_required_core_modules_exist():
    assert CORE_DIR.is_dir(), f"No existe {CORE_DIR}"
    for name in REQUIRED_CORE_MODULES:
        path = CORE_DIR / name
        assert path.is_file(), f"Falta módulo core obligatorio: {name}"


def test_core_modules_have_module_docstring():
    for name in REQUIRED_CORE_MODULES:
        path = CORE_DIR / name
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        docstring = ast.get_docstring(tree)
        assert docstring is not None and docstring.strip(), (
            f"{name} debe tener docstring de módulo"
        )