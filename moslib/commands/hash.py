"""SHA-256 de una ruta del clone."""

from moslib.core.hostfs import resolver
from moslib.core.integridad import sha256_fichero


def execute(args):
    if not args:
        print("[hash] Uso: hash <ruta>")
        return
    try:
        path = resolver(args[0])
    except ValueError as exc:
        print(f"[hash] {exc}")
        return
    if not path.is_file():
        print(f"[hash] no existe: {args[0]}")
        return
    print(sha256_fichero(path))


def help():
    return "Uso: hash <ruta> - SHA-256 del fichero en el clone."


def sinopsis():
    return ["hash <ruta>"]