"""Comando mos2ai. Al rotar no espera al humano."""

from moslib.core.mos2ai_bucle import anotar, cargar, rotar, ultimo_encargo
from moslib.core.mos2ai_cliente import bucle, tras_herramienta


def execute(args):
    if not args:
        print(help())
        return
    cmd = args[0].lower()
    if cmd == "estado":
        inv = cargar("investigacion")
        acc = cargar("acciones")
        print(f"Investigacion: {len(inv)} trozos")
        print(f"Acciones: {len(acc)} trozos")
        print(f"Ultimo encargo: {ultimo_encargo() or '-'}")
        return
    if cmd == "investigacion":
        texto = " ".join(args[1:]).strip()
        if not texto:
            print("Uso: mos2ai investigacion <texto>")
            return
        anotar("investigacion", "system", texto)
        print("Investigacion guardada.")
        return
    if cmd == "encargo":
        texto = " ".join(args[1:]).strip()
        if not texto:
            print("Uso: mos2ai encargo <texto>")
            return
        anotar("acciones", "user", texto)
        print("Encargo guardado. Al rotar se continua con este texto.")
        return
    if cmd == "rotar":
        if len(args) < 2:
            print("Uso: mos2ai rotar <modelo> [resultado pendiente]")
            return
        modelo = args[1]
        pendiente = " ".join(args[2:])
        print(rotar(modelo, pendiente, lambda _msgs: "relevo anotado; el cliente debe completar"))
        return
    if cmd == "seguir":
        if not ultimo_encargo():
            print("No hay encargo. Nada que continuar.")
            return
        print("Sigo. Si hay cuota, no se abre el prompt humano.")
        bucle(args[1] if len(args) > 1 else "auto", _completar_falso, _ejecutar_falso)
        return
    if cmd == "herramienta":
        if len(args) < 3:
            print("Uso: mos2ai herramienta <nombre> <resultado>")
            return
        modelo = tras_herramienta("auto", args[1], " ".join(args[2:]), _completar_falso, _ejecutar_falso)
        print(f"Modelo tras herramienta: {modelo}")
        return
    print(help())


def _completar_falso(modelo, mensajes):
    return False, "cuota"


def _ejecutar_falso(nombre, args):
    return ""


_completar_falso.siguiente = lambda _modelo: "siguiente"


def help():
    return (
        "Uso: mos2ai estado|investigacion <texto>|encargo <texto>|"
        "rotar <modelo> [resultado]|seguir [modelo]|herramienta <nombre> <resultado>"
    )


def sinopsis():
    return [
        "mos2ai",
        "mos2ai estado",
        "mos2ai investigacion <texto>",
        "mos2ai encargo <texto>",
        "mos2ai rotar <modelo> [resultado]",
        "mos2ai seguir [modelo]",
        "mos2ai herramienta <nombre> <resultado>",
    ]