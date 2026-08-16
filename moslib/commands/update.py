"""
Comando update de MetsuOS.
Fuerza la actualización del repositorio local desde origin/main.
Si hay cambios pendientes, crea una rama de backup con fecha y hora.
Mantiene como máximo 10 ramas de backup locales.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _run(cmd, cwd, check=True):
    """Ejecuta un comando git y devuelve el resultado."""
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        print(f"Error ejecutando: {' '.join(cmd)}")
        if result.stderr:
            print(result.stderr.strip())
        sys.exit(result.returncode)
    return result


def _get_project_root() -> Path:
    # moslib/commands/update.py → raíz del proyecto
    return Path(__file__).resolve().parent.parent.parent


def _has_pending_changes(cwd: Path) -> bool:
    """Detecta si hay cambios sin commitear o el working tree está sucio."""
    result = _run(["git", "status", "--porcelain"], cwd, check=False)
    return bool(result.stdout.strip())


def _create_backup_branch(cwd: Path) -> str:
    """Crea una rama de backup con timestamp y guarda los cambios pendientes."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"backup/{timestamp}"

    print(f"[update] Creando rama de backup: {branch_name}")

    # Crear la rama desde el estado actual
    _run(["git", "checkout", "-b", branch_name], cwd)

    # Si hay cambios sin commitear, los guardamos en la rama
    if _has_pending_changes(cwd):
        _run(["git", "add", "-A"], cwd)
        _run(
            ["git", "commit", "-m", f"Backup automático antes de update ({timestamp})"],
            cwd,
            check=False,  # por si no hay nada que commitear realmente
        )

    return branch_name


def _prune_old_backups(cwd: Path, keep: int = 10):
    """Elimina las ramas backup/ más antiguas, dejando solo las 'keep' más recientes."""
    result = _run(
        ["git", "branch", "--list", "backup/*"],
        cwd,
        check=False,
    )
    branches = [
        line.strip().lstrip("* ").strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    # Ordenar por nombre (el timestamp hace que el orden alfabético sea cronológico)
    branches = sorted(branches)

    if len(branches) <= keep:
        return

    to_delete = branches[:-keep]  # las más antiguas
    for branch in to_delete:
        print(f"[update] Eliminando rama de backup antigua: {branch}")
        _run(["git", "branch", "-D", branch], cwd, check=False)


def execute(args):
    cwd = _get_project_root()

    print("[update] Iniciando actualización forzada desde origin/main...")
    print(f"[update] Directorio: {cwd}")
    print()

    # 1. Asegurarnos de que es un repositorio git
    result = _run(["git", "rev-parse", "--is-inside-work-tree"], cwd, check=False)
    if result.returncode != 0:
        print("Error: no se está dentro de un repositorio git.")
        sys.exit(1)

    # 2. Si hay cambios pendientes → crear rama de backup
    if _has_pending_changes(cwd):
        print("[update] Se han detectado cambios locales pendientes.")
        backup_branch = _create_backup_branch(cwd)
        print(f"[update] Cambios guardados en la rama: {backup_branch}")
        # Volver a main (o a la rama que estuviera, pero forzamos main después)
        _run(["git", "checkout", "main"], cwd, check=False)
    else:
        print("[update] No hay cambios locales pendientes.")
        # Asegurarnos de estar en main
        _run(["git", "checkout", "main"], cwd, check=False)

    # 3. Obtener lo último de origin
    print("[update] Descargando cambios de origin...")
    _run(["git", "fetch", "origin"], cwd)

    # 4. Forzar sincronización absoluta con origin/main
    print("[update] Forzando sincronización con origin/main...")
    _run(["git", "reset", "--hard", "origin/main"], cwd)

    # 5. Limpiar ramas de backup antiguas (máximo 10)
    print("[update] Limpiando ramas de backup antiguas (máx. 10)...")
    _prune_old_backups(cwd, keep=10)

    print()
    print("[update] Actualización completada.")
    print("[update] El repositorio local está ahora exactamente igual que origin/main.")


def help():
    return (
        "Uso: update - Fuerza la actualización desde origin/main. "
        "Si hay cambios locales, los guarda en una rama backup/YYYYMMDD_HHMMSS "
        "y mantiene como máximo 10 ramas de backup."
    )