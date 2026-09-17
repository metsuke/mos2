"""
Comando test de MetsuOS.
Batería pytest + informe A11Y. -s para ver [tope] y el resto de prints.
"""

import subprocess
import sys
from pathlib import Path

from moslib.commands.a11y import execute as a11y_execute


def execute(args):
    project_root = Path(__file__).resolve().parent.parent.parent
    extra = list(args or [])
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
    else:
        print()
        print("Algunos tests fallaron.")
        sys.exit(result.returncode)


def help():
    return (
        "Uso: test [args...] - Pytest (-s) y regenera informe A11Y."
    )


def sinopsis():
    return ["test", "test [args...]"]