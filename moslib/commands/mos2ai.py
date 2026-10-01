"""mos2ai: comando de sistema. Cascada de cuota, no preferencia de usuario."""

from moslib.core.ia_cascade import ORDEN, complete, vetados


def execute(args):
    if not args or args[0] in ("-h", "--help", "help"):
        print(help())
        return 0
    if args[0] == "vetados":
        for pid in ORDEN:
            fuera = sorted(vetados(pid))
            print(f"{pid}: {', '.join(fuera) if fuera else '(ninguno)'}")
        return 0
    ok, texto, prov = complete(" ".join(args))
    if ok:
        print(f"[{prov}] {texto}")
        return 0
    print(texto)
    return 1


def help():
    return (
        "Uso: mos2ai <texto> | mos2ai vetados\n"
        "Comando de sistema. No es una app de usuario.\n"
        "Cascada al agotar cuota de Google: Grok, OpenAI, OpenRouter, "
        "Jan en la red local, GPT4All al final (sin GPU).\n"
        "Si el modelo indicado no existe, se quita de la lista y no se selecciona.\n"
        "Claves: GEMINI_API_KEY, XAI_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY."
    )


def sinopsis():
    return ["mos2ai <texto>", "mos2ai vetados"]
