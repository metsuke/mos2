"""
iarouter: estado, detección, elegir proveedor, preguntar.
Enviar texto solo con 'preguntar' (acción explícita).
"""

from moslib.core import ia_router


def _print_detect(items: list, titulo: str | None = None):
    if titulo:
        print(titulo)
        print()
    print("Proveedor    Tipo     ¿OK?")
    print("------------ -------- ----")
    for d in items:
        marca = "SI" if d.get("disponible") else "NO"
        print(f"{d.get('id', '-'):12} {d.get('tipo', '-'):8} {marca}")
    print()
    print("Detalle")
    print("-------")
    for d in items:
        nombre = d.get("id", "-")
        tipo = d.get("tipo", "-")
        estado = "disponible" if d.get("disponible") else "no disponible"
        motivo = d.get("motivo") or "sin detalle"
        print()
        print(f"{nombre} ({tipo}) está {estado}. {motivo}")


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("status",):
        st = ia_router.status()
        print("Enrutador de IA")
        print()
        print(f"Proveedor activo: {st['provider']}")
        print(f"Enabled: {st['enabled']}")
        if st.get("motivo"):
            print(f"Motivo de política: {st['motivo']}")
        print()
        _print_detect(st.get("disponibles") or ia_router.detectar())
        return

    if args[0] in ("detectar", "detect"):
        _print_detect(ia_router.detectar(), "Detección de proveedores")
        return

    if args[0] in ("usar", "use") and len(args) >= 2:
        ok, msg = ia_router.set_provider(args[1])
        print(msg)
        return

    if args[0] in ("preguntar", "ask", "q") and len(args) >= 2:
        prompt = " ".join(args[1:])
        ok, text = ia_router.complete(prompt)
        print()
        print("Respuesta")
        print()
        print(text)
        print()
        return

    print("Uso:")
    print("  iarouter")
    print("  iarouter status")
    print("  iarouter detectar")
    print("  iarouter usar jan|gpt4all|grok|openrouter")
    print("  iarouter preguntar TEXTO")


def help():
    return (
        "Uso: iarouter [status|detectar|usar <proveedor>|preguntar <texto>] - "
        "Elige modelo (detección automática) y envía una petición explícita. "
        "Off hasta 'usar'. Claves: XAI_API_KEY, OPENROUTER_API_KEY."
    )