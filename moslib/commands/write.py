"""write: solo en multi. Payload = hash + codec + punto."""

from moslib.core.write_b64 import aplicar


def execute(args, payload=None):
    if payload is None:
        print("[write] Solo se usa dentro de multi.")
        return 1
    if not args:
        print("[write] Uso: write <ruta>")
        return 1
    ok, msg = aplicar(args[0], list(payload))
    print(msg)
    if not ok:
        return 1
    from moslib.commands import code as cmd_code
    cmd_code.execute([args[0]])
    return 0


def help():
    return (
        "Uso: write <ruta> (solo multi). "
        "Linea 1 sha256. Luego gz: a 80 cols. Cierra con ."
    )


def sinopsis():
    return ["write <ruta>", "w <ruta>"]
