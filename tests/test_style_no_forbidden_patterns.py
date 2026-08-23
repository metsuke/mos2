"""Detección de patrones de código prohibidos en core y comandos."""

import ast
from pathlib import Path

from moslib.core.user import get_project_root


ROOT = get_project_root()
SCAN_DIRS = (
    ROOT / "moslib" / "core",
    ROOT / "moslib" / "commands",
)


FORBIDDEN_CALLS = {"eval", "exec"}


def _iter_python_files():
    for base in SCAN_DIRS:
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.py")):
            if path.name.startswith("__"):
                continue
            yield path


def _find_forbidden_calls(source: str) -> list[str]:
    tree = ast.parse(source)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = None
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name in FORBIDDEN_CALLS:
                found.append(name)
    return found


def test_no_eval_or_exec_in_core_and_commands():
    violations = []
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        found = _find_forbidden_calls(source)
        if found:
            violations.append(f"{path}: {sorted(set(found))}")

    assert not violations, (
        "Se encontraron llamadas prohibidas (eval/exec):\n" + "\n".join(violations)
    )