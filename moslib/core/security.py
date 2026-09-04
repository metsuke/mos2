"""
moslib.core.security
Validación de imports de comandos (sistema, usuario y apps).

Permitido siempre: stdlib y moslib.
Permitido en comando de app: minimoslib.* si el módulo existe
en <app_dir>/minimoslib/.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import List, Set, Tuple


STDLIB_MODULES: Set[str] = set(sys.stdlib_module_names)
ALLOWED_PREFIXES = ("moslib",)


def _minimoslib_file(app_dir: Path, module: str) -> Path | None:
    if not module or module.split(".")[0] != "minimoslib":
        return None
    parts = module.split(".")[1:]
    base = Path(app_dir) / "minimoslib"
    if not parts:
        init = base / "__init__.py"
        return init if init.is_file() else None
    file_py = base.joinpath(*parts).with_suffix(".py")
    pkg_init = base.joinpath(*parts) / "__init__.py"
    if file_py.is_file():
        return file_py
    if pkg_init.is_file():
        return pkg_init
    return None


def _is_allowed_module(name: str, app_dir: Path | None = None) -> bool:
    if not name:
        return False
    top = name.split(".")[0]
    if top in STDLIB_MODULES:
        return True
    for prefix in ALLOWED_PREFIXES:
        if name == prefix or name.startswith(prefix + "."):
            return True
    if top == "minimoslib":
        if app_dir is None:
            return False
        if name == "minimoslib":
            return (Path(app_dir) / "minimoslib" / "__init__.py").is_file()
        return _minimoslib_file(app_dir, name) is not None
    return False


def analyze_imports(source: str, app_dir: Path | None = None) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, [f"Error de sintaxis: {e}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _is_allowed_module(alias.name, app_dir):
                    errors.append(f"Import prohibido: import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level > 0:
                errors.append(
                    f"Import relativo no permitido: from {'.' * node.level}{module}"
                )
            elif not _is_allowed_module(module, app_dir):
                errors.append(f"Import prohibido: from {module} import ...")

    return len(errors) == 0, errors


def validate_command_file(
    file_path: str | Path,
    app_dir: str | Path | None = None,
) -> Tuple[bool, List[str]]:
    path = Path(file_path)
    if not path.is_file():
        return False, [f"El archivo no existe: {path}"]
    if path.suffix != ".py":
        return False, [f"No es un archivo Python: {path}"]
    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"No se pudo leer el archivo: {e}"]
    ad = Path(app_dir) if app_dir is not None else None
    return analyze_imports(source, app_dir=ad)


def validate_command_source(
    source: str,
    name: str = "<string>",
    app_dir: str | Path | None = None,
) -> Tuple[bool, List[str]]:
    ad = Path(app_dir) if app_dir is not None else None
    return analyze_imports(source, app_dir=ad)