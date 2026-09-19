"""Comando test de MetsuOS. Pytest + A11Y. Consulta: test 120."""

import subprocess
import sys
from pathlib import Path

from moslib.commands.a11y import execute as a11y_execute
from moslib.core.tope import informe


def execute(args):
    extra = [str(x) for x in (args or [])]
    if "120" in extra:
        print(informe())
        return
    project_root = Path(__file__).resolve().parent.parent.parent
    if "-s" not in extra and "--capture=no" not in extra:
        extra = ["-s"] + extra
    print("Ejecutando tests de MetsuOS...")
    print("-" * 50)
    result = subprocess.run(
        [sys.executable, "-m", "pytest"] + extra,
        cwd=str(project_root),
    )
    print()
    print("[test] Regenerando informe de accesibilidad...")
    a11y_execute([])
    if result.returncode == 0:
        print()
        print("Todos los tests pasaron correctamente.")
        return
    print()
    print("Algunos tests fallaron.")
    sys.exit(result.returncode)


def help():
    return (
        "Uso: test [args...] - Pytest (-s) e informe A11Y. "
        "test 120 - lista ficheros de moslib con más de 120 líneas (no falla)."
    )


def sinopsis():
    return ["test", "test [args...]", "test 120"]
