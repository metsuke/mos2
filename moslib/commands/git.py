"""Git del anfitrión, cwd = raíz del clone."""

from moslib.core.hostfs import run_host


def execute(args):
    args = list(args or [])
    if not args:
        print("[git] Uso: git <subcomando> [args...]")
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
        "Uso: git <subcomando> [args...] - Ejecuta git en la raíz del clone."
    )


def sinopsis():
    return [
        "git status",
        "git add <ruta>",
        "git --no-pager diff",
        "git --no-pager diff --cached --stat",
        "git commit -m <mensaje>",
    ]