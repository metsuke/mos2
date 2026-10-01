"""mos2ai dentro de MOS. Misma puerta que el py de la raiz."""

from moslib.core.mos2ai_bucle import main


def execute(args):
    if args and args[0] in ("-h", "--help", "help"):
        print(help())
        return 0
    main()
    return 0


def help():
    return (
        "Uso: mos2ai\n"
        "Comando de sistema. Arranca el puente de ingesta de moslib.core.\n"
        "Lista modelos, quita los que ya no existen y rota si hay cuota.\n"
        "Puede listar, leer, crear ficheros y crear directorios en el cwd.\n"
        "El py de la raiz, mos2AI.py, llama a la misma funcion."
    )


def sinopsis():
    return ["mos2ai"]
