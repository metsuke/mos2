"""
moslib.core.security
Validación de seguridad de comandos (sistema y usuario).

Regla estricta:
- Solo se permiten imports de la biblioteca estándar de Python
  y de moslib (y sus submódulos).
- Cualquier otro import está prohibido.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import List, Set, Tuple


# Módulos de la biblioteca estándar (Python 3.10+)
STDLIB_MODULES: Set[str] = set(sys.stdlib_module_names)

# Prefijos permitidos además de la stdlib
ALLOWED_PREFIXES = (
    "moslib",
)


def _is_allowed_module(name: str) -> bool:
    """
    Comprueba si un nombre de módulo está permitido.
    Ejemplos permitidos: os, pathlib, moslib, moslib.core.user
    """
    if not name:
        return False

    top_level = name.split(".")[0]

    if top_level in STDLIB_MODULES:
        return True

    for prefix in ALLOWED_PREFIXES:
        if name == prefix or name.startswith(prefix + "."):
            return True

    return False


def analyze_imports(source: str) -> Tuple[bool, List[str]]:
    """
    Analiza el código fuente y devuelve:
    - ok (bool)
    - lista de errores encontrados
    """
    errors: List[str] = []

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, [f"Error de sintaxis: {e}"]

    for node in ast.walk(tree):
        # import xxx
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _is_allowed_module(alias.name):
                    errors.append(f"Import prohibido: import {alias.name}")

        # from xxx import yyy
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level > 0:
                # Imports relativos (from .xxx import ...) → solo permitimos dentro de moslib
                # Por seguridad los rechazamos en comandos de usuario
                errors.append(f"Import relativo no permitido: from {'.' * node.level}{module}")
            else:
                if not _is_allowed_module(module):
                    errors.append(f"Import prohibido: from {module} import ...")

    return len(errors) == 0, errors


def validate_command_file(file_path: str | Path) -> Tuple[bool, List[str]]:
    """
    Valida un archivo de comando (.py).
    Devuelve (ok, lista_de_errores).
    """
    path = Path(file_path)

    if not path.is_file():
        return False, [f"El archivo no existe: {path}"]

    if path.suffix != ".py":
        return False, [f"No es un archivo Python: {path}"]

    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"No se pudo leer el archivo: {e}"]

    return analyze_imports(source)


def validate_command_source(source: str, name: str = "<string>") -> Tuple[bool, List[str]]:
    """Versión que valida código en memoria (útil para tests)."""
    return analyze_imports(source)