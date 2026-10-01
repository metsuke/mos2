"""update: si hay sucio, backup local y luego el remoto a la fuerza."""

import os
import sys
from pathlib import Path

from moslib.core.dev_git import ramas_remotas, sucio
from moslib.core.update_git import (
    create_backup_branch,
    prune_old_backups,
    run,
    sync_tags_with_origin,
)

BACKUPS = 10


def _root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _avisar():
    print()
    print("[update] El código nuevo no entra en esta sesión.")
    print("[update] exit y vuelve a lanzar mos2, o: update reiniciar")


def _reiniciar(cwd: Path):
    entrada = cwd / "rootfs" / "bin" / "mos.py"
    print("[update] Relanzando MOSh...")
    os.execv(sys.executable, [sys.executable, str(entrada)])


def _integridad():
    try:
        from moslib.core.integridad import copiar_repo_a_local

        dest = copiar_repo_a_local()
        print(f"[update] integridad local ← repo  {dest}")
    except Exception as exc:
        print(f"[update] integridad local: {exc}")


def _resguardar(cwd: Path) -> None:
    if not sucio(cwd):
        return
    print("[update] Árbol sucio. Backup local obligatorio.")
    create_backup_branch(cwd)
    prune_old_backups(cwd, keep=BACKUPS)


def _forzar(cwd: Path, rama: str) -> None:
    run(["git", "fetch", "origin"], cwd)
    run(["git", "checkout", "-B", rama, f"origin/{rama}"], cwd)
    run(["git", "reset", "--hard", f"origin/{rama}"], cwd)
    prune_old_backups(cwd, keep=BACKUPS)


def _a_main(cwd: Path):
    _resguardar(cwd)
    print("[update] origin/main...")
    sync_tags_with_origin(cwd)
    _forzar(cwd, "main")
    _integridad()
    print("[update] Completado. Árbol = origin/main. Backups locales: 10.")
    _avisar()


def _dev(cwd: Path):
    ramas = ramas_remotas(cwd)
    if not ramas:
        print("[update] No hay ramas remotas aparte de main.")
        return
    print("[update] Ramas de desarrollo:")
    for i, name in enumerate(ramas, 1):
        print(f"  {i}. {name}")
    try:
        raw = input("[update] Número (vacío cancela): ").strip()
    except EOFError:
        return
    if not raw:
        return
    if not raw.isdigit() or not (1 <= int(raw) <= len(ramas)):
        print("[update] Número no válido.")
        return
    rama = ramas[int(raw) - 1]
    _resguardar(cwd)
    _forzar(cwd, rama)
    _integridad()
    print(f"[update] Árbol = origin/{rama}. Relanza MOSh.")
    _avisar()


def execute(args):
    args = list(args or [])
    cwd = _root()
    if args == ["reiniciar"]:
        _reiniciar(cwd)
        return
    if args[:1] == ["dev"]:
        _dev(cwd)
        return
    _a_main(cwd)
    if "reiniciar" in args:
        _reiniciar(cwd)


def help():
    return (
        "Uso: update | update dev | update reiniciar. "
        "Si hay cambios locales, rama backup/ y luego reset al remoto. "
        "Se guardan 10 backups."
    )


def sinopsis():
    return ["update", "update dev", "update reiniciar"]
