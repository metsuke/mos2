"""Crea un fichero vacío en la raíz del clone."""

from moslib.core.hostfs import resolver


def execute(args):
    if not args:
        print("[touch] Uso: touch <ruta-desde-la-raiz-del-clone>")
        return
    dest = resolver(args[0])
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.touch()
    print(f"[touch] {dest}")


def help():
    return "Uso: touch <ruta> - Crea el fichero vacío relativo a la raíz del clone."


def sinopsis():
    return ["touch <ruta>"]