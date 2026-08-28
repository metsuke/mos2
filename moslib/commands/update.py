"""
Comando update de MetsuOS.
Fuerza la actualización del repositorio local desde origin/main.
Si hay cambios pendientes, crea una rama de backup con fecha y hora.
Mantiene como máximo 10 ramas de backup locales.
Alinea los tags locales con los de origin (alta y baja).
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
    return Path(__file__).resolve().parent.parent.parent


def _has_pending_changes(cwd: Path) -> bool:
    result = _run(["git", "status", "--porcelain"], cwd, check=False)
    return bool(result.stdout.strip())


def _create_backup_branch(cwd: Path) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"backup/{timestamp}"

    print(f"[update] Creando rama de backup: {branch_name}")
    _run(["git", "checkout", "-b", branch_name], cwd)

    if _has_pending_changes(cwd):
        _run(["git", "add", "-A"], cwd)
        _run(
            ["git", "commit", "-m", f"Backup automático antes de update ({timestamp})"],
            cwd,
            check=False,
        )

    return branch_name


def _prune_old_backups(cwd: Path, keep: int = 10):
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
    branches = sorted(branches)
    if len(branches) <= keep:
        return
    to_delete = branches[:-keep]
    for branch in to_delete:
        print(f"[update] Eliminando rama de backup antigua: {branch}")
        _run(["git", "branch", "-D", branch], cwd, check=False)


def _sync_tags_with_origin(cwd: Path):
    """Deja los tags locales iguales a los de origin (Git prune-tags)."""
    print("[update] Sincronizando tags con origin...")
    _run(
        ["git", "fetch", "origin", "--tags", "--prune", "--prune-tags"],
        cwd,
    )


def execute(args):
    cwd = _get_project_root()

    print("[update] Iniciando actualización forzada desde origin/main...")
    print(f"[update] Directorio: {cwd}")
    print()

    result = _run(["git", "rev-parse", "--is-inside-work-tree"], cwd, check=False)
    if result.returncode != 0:
        print("Error: no se está dentro de un repositorio git.")
        sys.exit(1)

    if _has_pending_changes(cwd):
        print("[update] Se han detectado cambios locales pendientes.")
        backup_branch = _create_backup_branch(cwd)
        print(f"[update] Cambios guardados en la rama: {backup_branch}")
        _run(["git", "checkout", "main"], cwd, check=False)
    else:
        print("[update] No hay cambios locales pendientes.")
        _run(["git", "checkout", "main"], cwd, check=False)

    print("[update] Descargando cambios de origin...")
    _run(["git", "fetch", "origin"], cwd)

    _sync_tags_with_origin(cwd)

    print("[update] Forzando sincronización con origin/main...")
    _run(["git", "reset", "--hard", "origin/main"], cwd)

    print("[update] Limpiando ramas de backup antiguas (máx. 10)...")
    _prune_old_backups(cwd, keep=10)

    print()
    print("[update] Actualización completada.")
    print("[update] El árbol main y los tags locales coinciden con origin.")


def help():
    return (
        "Uso: update - Fuerza la actualización desde origin/main. "
        "Si hay cambios locales, los guarda en una rama backup/YYYYMMDD_HHMMSS "
        "y mantiene como máximo 10 ramas de backup. "
        "Sincroniza tags con origin (añade los nuevos y quita los que el remoto ya no tiene)."
    )