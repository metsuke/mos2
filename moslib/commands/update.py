"""update: trae origin/main. Relanzar MOSh para cargar código nuevo."""

import os
import sys
from pathlib import Path

from moslib.core.update_git import (
    create_backup_branch,
    has_pending_changes,
    prune_old_backups,
    run,
    sync_tags_with_origin,
)


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _avisar_reinicio():
    print()
    print("[update] El código nuevo no entra en esta sesión.")
    print("[update] Escribe exit y vuelve a lanzar mos2, o: update reiniciar")


def _reiniciar(cwd: Path):
    entrada = cwd / "rootfs" / "bin" / "mos.py"
    print("[update] Relanzando MOSh...")
    os.execv(sys.executable, [sys.executable, str(entrada)])


def _sincronizar_integridad():
    try:
        from moslib.core.integridad import copiar_repo_a_local
        print(copiar_repo_a_local())
    except Exception as exc:
        print(f"[update] integridad local: {exc}")


def execute(args):
    args = list(args or [])
    solo_reiniciar = args == ["reiniciar"]
    cwd = _get_project_root()
    if not solo_reiniciar:
        print("[update] Iniciando actualización forzada desde origin/main...")
        print(f"[update] Directorio: {cwd}")
        print()
        result = run(["git", "rev-parse", "--is-inside-work-tree"], cwd, check=False)
        if result.returncode != 0:
            print("Error: no se está dentro de un repositorio git.")
            sys.exit(1)
        if has_pending_changes(cwd):
            print("[update] Se han detectado cambios locales pendientes.")
            backup_branch = create_backup_branch(cwd)
            print(f"[update] Cambios guardados en la rama: {backup_branch}")
            run(["git", "checkout", "main"], cwd, check=False)
        else:
            print("[update] No hay cambios locales pendientes.")
            run(["git", "checkout", "main"], cwd, check=False)
        print("[update] Descargando cambios de origin...")
        run(["git", "fetch", "origin"], cwd)
        sync_tags_with_origin(cwd)
        print("[update] Forzando sincronización con origin/main...")
        run(["git", "reset", "--hard", "origin/main"], cwd)
        print("[update] Limpiando ramas de backup antiguas (máx. 10)...")
        prune_old_backups(cwd, keep=10)
        _sincronizar_integridad()
        print()
        print("[update] Actualización completada.")
        print("[update] El árbol main y los tags locales coinciden con origin.")
        _avisar_reinicio()
    if "reiniciar" in args:
        _reiniciar(cwd)


def help():
    return (
        "Uso: update [reiniciar] - Trae origin/main. "
        "Los módulos de esta sesión no cambian hasta relanzar MOSh."
    )


def sinopsis():
    return ["update", "update reiniciar"]
