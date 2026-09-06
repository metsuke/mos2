"""
iarouter: estado, detección, elegir proveedor, preguntar.
Enviar texto solo con 'preguntar' (acción explícita).
"""

from moslib.core import ia_router


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("status",):
        st = ia_router.status()
        print(f"proveedor: {st['provider']}")
        print(f"enabled: {st['enabled']}")
        if st.get("motivo"):
            print(f"motivo: {st['motivo']}")
        print("disponibles:")
        for d in st.get("disponibles") or ia_router.detectar():
            marca = "si" if d["disponible"] else "no"
            print(f"  {d['id']}  ({d['tipo']})  {marca}  {d['motivo']}")
        return

    if args[0] in ("detectar", "detect"):
        print("Proveedores detectados:")
        for d in ia_router.detectar():
            marca = "si" if d["disponible"] else "no"
            print(f"  {d['id']}  ({d['tipo']})  {marca}  {d['motivo']}")
        return

    if args[0] in ("usar", "use") and len(args) >= 2:
        ok, msg = ia_router.set_provider(args[1])
        print(msg)
        return

    if args[0] in ("preguntar", "ask", "q") and len(args) >= 2:
        prompt = " ".join(args[1:])
        ok, text = ia_router.complete(prompt)
        if ok:
            print(text)
        else:
            print(text)
        return

    print("Uso: iarouter [status|detectar|usar <jan|gpt4all|grok|openrouter>|preguntar <texto>]")


def help():
    return (
        "Uso: iarouter [status|detectar|usar <proveedor>|preguntar <texto>] - "
        "Elige modelo (detección automática) y envía una petición explícita. "
        "Off hasta 'usar'. Claves: XAI_API_KEY, OPENROUTER_API_KEY."
    )