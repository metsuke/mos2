"""write: solo en multi. Payload = hash + Base64 + punto."""

from moslib.core.write_b64 import aplicar


def execute(args, payload=None):
    if payload is None:
        print("[write] Solo se usa dentro de multi.")
        return
    if not args:
        print("[write] Uso: write <ruta>")
        return
    ok, msg = aplicar(args[0], list(payload))
    print(msg)
    if not ok:
        return


def help():
    return (
        "Uso: write <ruta>  (solo multi). "
        "Línea 1: sha256. Luego Base64. Cierra con ."
    )


def sinopsis():
    return ["write <ruta>", "w <ruta>"]