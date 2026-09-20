"""update: main limpio, o update dev para probar una rama."""

import os
import sys
from pathlib import Path

from moslib.core.dev_git import checkout_rama, ramas_remotas, sucio
from moslib.core.update_git import prune_old_backups, run, sync_tags_with_origin


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
        print(copiar_repo_a_local())
    except Exception as exc:
        print(f"[update] integridad local: {exc}")


def _a_main(cwd: Path):
    if sucio(cwd):
        print("[update] Hay cambios locales. Usa dev publicar o limpia el árbol.")
        sys.exit(1)
    print("[update] origin/main...")
    run(["git", "fetch", "origin"], cwd)
    run(["git", "checkout", "main"], cwd, check=False)
    sync_tags_with_origin(cwd)
    run(["git", "reset", "--hard", "origin/main"], cwd)
    prune_old_backups(cwd, keep=10)
    _integridad()
    print("[update] Completado. Árbol = origin/main.")
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
    if sucio(cwd):
        print("[update] Árbol sucio. Publica o limpia antes.")
        return
    checkout_rama(cwd, rama)
    _integridad()
    print(f"[update] Estás en {rama}. Relanza MOSh.")
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
    return "Uso: update | update dev | update reiniciar"


def sinopsis():
    return ["update", "update dev", "update reiniciar"]
