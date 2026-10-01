"""mos2ai: google, si cuota grok, si cuota openai."""

from moslib.core.ia_cascade import complete


def execute(args):
    if not args or args[0] in ("-h", "--help", "help"):
        print(help())
        return 0
    ok, texto, prov = complete(" ".join(args))
    if ok:
        print(f"[{prov}] {texto}")
        return 0
    print(texto)
    return 1


def help():
    return (
        "Uso: mos2ai <texto> — prueba Google (Gemini). "
        "Si la cuota o el rate limit fallan, Grok. Si tambien, OpenAI. "
        "Claves: GEMINI_API_KEY, XAI_API_KEY, OPENAI_API_KEY "
        "(o iarouter clave google|grok|openai)."
    )


def sinopsis():
    return ["mos2ai <texto>"]
