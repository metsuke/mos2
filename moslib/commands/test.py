"""
Comando test de MetsuOS.
Ejecuta la batería de tests unitarios y de seguridad.
"""

import subprocess
import sys
from pathlib import Path


def execute(args):
    project_root = Path(__file__).resolve().parent.parent.parent
    print("Ejecutando tests de MetsuOS...")
    print("-" * 50)

    result = subprocess.run(
        [sys.executable, "-m", "pytest"] + args,
        cwd=str(project_root),
    )

    if result.returncode == 0:
        print("\n✅ Todos los tests pasaron correctamente.")
    else:
        print("\n❌ Algunos tests fallaron.")
        sys.exit(result.returncode)


def help():
    return "Uso: test [args...] - Ejecuta la batería de tests unitarios y de seguridad (pytest)."