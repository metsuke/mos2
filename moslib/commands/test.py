"""
Comando test de MetsuOS.
Ejecuta la batería de tests unitarios y de seguridad.
Si la batería incluye (o puede incluir) tests a11y, regenera el informe A11Y.
"""

import subprocess
import sys
from pathlib import Path

from moslib.commands.a11y import execute as a11y_execute


def execute(args):
    project_root = Path(__file__).resolve().parent.parent.parent
    print("Ejecutando tests de MetsuOS...")
    print("-" * 50)

    result = subprocess.run(
        [sys.executable, "-m", "pytest"] + args,
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
        print("Revisa la salida de pytest o ejecuta: poetry run pytest")
        sys.exit(result.returncode)


def help():
    return (
        "Uso: test [args...] - Ejecuta la batería de tests unitarios y de seguridad (pytest). "
        "Regenera también docs/a11y/informe.md e informe.json."
    )