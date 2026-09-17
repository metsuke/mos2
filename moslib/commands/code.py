"""Abre un fichero del clone con el editor del anfitrión (code/cursor)."""

from moslib.core.hostfs import resolver, run_host


def execute(args):
    if not args:
        print("[code] Uso: code <ruta-desde-la-raiz-del-clone>")
        return
    dest = resolver(args[0])
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        dest.touch()
    try:
        codigo = run_host(["code", str(dest)])
    except FileNotFoundError:
        codigo = run_host(["cursor", str(dest)])
    if codigo != 0:
        print(f"[code] el editor salió con código {codigo}")


def help():
    return (
        "Uso: code <ruta> - Abre el fichero con VS Code o Cursor. "
        "Ruta relativa a la raíz del clone."
    )


def sinopsis():
    return ["code <ruta>"]