"""
Comando update de MetsuOS.
Fuerza la actualización del repositorio local desde origin/main.
Los módulos ya cargados en esta sesión no cambian hasta relanzar MOSh.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _run(cmd, cwd, check=True):
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
    result = _run(["git", "branch", "--list", "backup/*"], cwd, check=False)
    branches = [
        line.strip().lstrip("* ").strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]
    branches = sorted(branches)
    if len(branches) <= keep:
        return
    for branch in branches[:-keep]:
        print(f"[update] Eliminando rama de backup antigua: {branch}")
        _run(["git", "branch", "-D", branch], cwd, check=False)


def _sync_tags_with_origin(cwd: Path):
    print("[update] Sincronizando tags con origin...")
    _run(
        ["git", "fetch", "origin", "--tags", "--prune", "--prune-tags"],
        cwd,
    )


def _avisar_reinicio():
    print()
    print("[update] El código nuevo no entra en esta sesión.")
    print("[update] Escribe exit y vuelve a lanzar mos2, o: update reiniciar")


def _reiniciar(cwd: Path):
    entrada = cwd / "rootfs" / "bin" / "mos.py"
    print("[update] Relanzando MOSh...")
    os.execv(sys.executable, [sys.executable, str(entrada)])


def execute(args):
    args = list(args or [])
    solo_reiniciar = args == ["reiniciar"]
    cwd = _get_project_root()

    if not solo_reiniciar:
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
        _avisar_reinicio()

    if "reiniciar" in args:
        _reiniciar(cwd)


def help():
    return (
        "Uso: update [reiniciar] - Trae origin/main. "
        "Los módulos de esta sesión no cambian hasta relanzar MOSh. "
        "update reiniciar relanza el proceso tras el pull "
        "(o solo relanza si no hay pull pendiente)."
    )