"""Git del anfitrión, cwd = raíz del clone. No avanza main."""

from moslib.core.dev_git import rama_actual, raiz
from moslib.core.hostfs import run_host

_BLOQUEO = {"commit", "push", "merge", "rebase"}


def execute(args):
    args = list(args or [])
    if not args:
        print("[git] Uso: git <subcomando> [args...]")
        return
    if args[0] in _BLOQUEO and rama_actual(raiz()) == "main":
        print("[git] Prohibido sobre main. Usa una rama y dev publicar / consolidar.")
        return
    try:
        codigo = run_host(["git", *args])
    except FileNotFoundError as exc:
        print(f"[git] {exc}")
        return
    if codigo != 0:
        print(f"[git] salió con código {codigo}")


def help():
    return (
        "Uso: git <subcomando> [args...] - Ejecuta git en la raíz del clone. "
        "commit/push/merge/rebase en main están bloqueados."
    )


def sinopsis():
    return [
        "git status",
        "git add <ruta>",
        "git --no-pager diff",
        "git --no-pager diff --cached --stat",
        "git commit -m <mensaje>",
    ]
