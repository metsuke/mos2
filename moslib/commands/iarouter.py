"""
iarouter: estado, detección, proveedor, modelos, preguntar.
Enviar texto solo con 'preguntar'.
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


def _proveedor_y_resto(args, inicio: int):
    if len(args) <= inicio:
        return None, []
    if args[inicio].lower() in ia_router.PROVIDERS:
        return args[inicio].lower(), args[inicio + 1 :]
    return None, args[inicio:]


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("status",):
        st = ia_router.status()
        print("Enrutador de IA")
        print()
        print(f"Proveedor activo: {st['provider']}")
        print(f"Enabled: {st['enabled']}")
        print(f"Modelo: {st.get('modelo', 'auto')}")
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

    if args[0] in ("modelos", "models"):
        proveedor = args[1] if len(args) >= 2 else None
        if proveedor and proveedor.lower() not in ia_router.PROVIDERS:
            print(f"Proveedor desconocido: {proveedor}")
            return
        ok, info, ids = ia_router.listar_modelos(proveedor)
        if not ok:
            print(info)
            return
        activo = ia_router.modelo_activo(info)
        print(f"Proveedor: {info}")
        print(f"Modelo activo: {activo}")
        print()
        print("Id")
        print("--")
        for mid in ids:
            marca = " (activo)" if mid == activo else ""
            print(f"{mid}{marca}")
        print()
        for mid in ids:
            extra = " Este es el modelo activo." if mid == activo else ""
            print(f"{mid}.{extra}")
        return

    if args[0] in ("modelo", "model"):
        proveedor, resto = _proveedor_y_resto(args, 1)
        if not resto:
            print("Uso: iarouter modelo [proveedor] <id del modelo...>")
            return
        mid = " ".join(resto)
        ok, msg = ia_router.set_modelo(mid, proveedor)
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
    print("  iarouter modelos [proveedor]")
    print("  iarouter modelo [proveedor] <id del modelo...>")
    print("  iarouter preguntar TEXTO")


def help():
    return (
        "Uso: iarouter [status|detectar|usar|modelos|modelo|preguntar] - "
        "Proveedor, lista de modelos, modelo activo y petición explícita."
    )