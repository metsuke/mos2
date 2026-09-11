"""
iarouter: estado, detección, check, proveedor, modelos, claves, share, publicar, puente, preguntar.
"""

import getpass

from moslib.core import ia_bridge, ia_check, ia_keys, ia_router, ia_share


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
        if d.get("url"):
            print(f"URL: {d['url']}")


def _print_lista(items: list, titulo: str):
    print(titulo)
    print()
    print("Comprobación                              ¿OK?")
    print("----------------------------------------- ----")
    for d in items:
        marca = "SI" if d.get("ok") or d.get("disponible") else "NO"
        print(f"{str(d.get('id', '-'))[:41]:41} {marca}")
    print()
    print("Detalle")
    print("-------")
    for d in items:
        estado = "correcto" if d.get("ok") or d.get("disponible") else "no correcto"
        print()
        print(f"{d.get('id')}: {estado}. {d.get('motivo', '')}")
        if d.get("url"):
            print(f"URL: {d['url']}")


def _ofrecer_destino(items: list):
    pol = ia_router.load_policy()
    vistos = set()
    for d in items:
        url = d.get("url") or ""
        if not url or "127.0.0.1" in url:
            continue
        if url in vistos:
            continue
        vistos.add(url)
        pid = "gpt4all" if "4891" in url else "jan"
        actual = pol.get("jan_url") if pid == "jan" else pol.get("gpt4all_url")
        if actual and url.rstrip("/") in (actual or ""):
            continue
        print()
        print(f"Se ha encontrado un destino en {url}")
        print("¿Guardar esta URL en la política de este usuario? [s/N]")
        try:
            resp = input("> ").strip().lower()
        except EOFError:
            return
        if resp in ("s", "si", "sí", "y", "yes"):
            ok, msg = ia_router.set_destino(pid, url)
            print(msg)
        else:
            print("No se ha guardado.")


def _print_puente():
    st = ia_bridge.estado()
    print("Puente MetsuOS")
    print()
    print(f"Activo: {st['activo']}")
    print(f"Puerto: {st['puerto']}")
    print(f"Destino: {st['destino']}")
    print()
    print("Detalle")
    print("-------")
    print()
    if st["activo"]:
        for url in st["urls"]:
            print(f"URL para otro MetsuOS: {url}")
    else:
        print("Parado. iarouter puente on para abrirlo en la LAN.")


def _proveedor_y_resto(args, inicio: int):
    if len(args) <= inicio:
        return None, []
    if args[inicio].lower() in ia_router.PROVIDERS:
        return args[inicio].lower(), args[inicio + 1 :]
    return None, args[inicio:]


def _pedir_clave(pid: str) -> None:
    print(f"Clave para {pid} (no se muestra al escribir). Vacío cancela.")
    try:
        raw = getpass.getpass("clave: ")
    except Exception:
        print("No se pudo leer la clave en este terminal.")
        return
    if not raw.strip():
        print("Cancelado.")
        return
    ok, msg = ia_keys.save_key(pid, raw)
    print(msg)


def execute(args):
    args = list(args or [])
    ia_keys.ingest_env()

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
        items = st.get("disponibles") or ia_router.detectar()
        _print_detect(items)
        _ofrecer_destino(items)
        return

    if args[0] in ("detectar", "detect"):
        items = ia_router.detectar()
        _print_detect(items, "Detección de proveedores")
        _ofrecer_destino(items)
        return

    if args[0] == "check":
        detalle = len(args) >= 2 and args[1] in ("detalle", "-v", "verbose")
        items = ia_check.check(detalle=detalle)
        _print_lista(items, "Check de compartición")
        _ofrecer_destino(items)
        return

    if args[0] == "share":
        _print_lista(ia_share.diagnostico(), "Share LAN")
        return

    if args[0] == "publicar":
        _print_lista(ia_share.publicar(), "Publicar (autorización explícita)")
        return

    if args[0] == "puente":
        sub = args[1] if len(args) >= 2 else "status"
        if sub in ("on", "start", "arrancar"):
            ok, msg = ia_bridge.arrancar()
            print(msg)
            return
        if sub in ("off", "stop", "parar"):
            ok, msg = ia_bridge.parar()
            print(msg)
            return
        _print_puente()
        return

    if args[0] in ("usar", "use") and len(args) >= 2:
        pid = args[1].lower()
        if pid in ("grok", "openrouter") and not ia_keys.has_any_key(pid):
            _pedir_clave(pid)
        ok, msg = ia_router.set_provider(args[1])
        print(msg)
        return

    if args[0] in ("clave", "key") and len(args) >= 2:
        pid = args[1].lower()
        if len(args) >= 3 and args[2] in ("borrar", "delete"):
            ok, msg = ia_keys.delete_key(pid)
            print(msg)
            return
        if ia_keys.has_stored_key(pid):
            print(f"Ya hay clave de {pid} en .mos. No se muestra.")
            print(f"Para sustituirla: iarouter clave {pid}")
            print(f"Para borrarla: iarouter clave {pid} borrar")
        _pedir_clave(pid)
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
    print("  iarouter check")
    print("  iarouter check detalle")
    print("  iarouter share")
    print("  iarouter publicar")
    print("  iarouter puente [on|off|status]")
    print("  iarouter usar jan|gpt4all|grok|openrouter")
    print("  iarouter clave <proveedor> [borrar]")
    print("  iarouter modelos [proveedor]")
    print("  iarouter modelo [proveedor] <id del modelo...>")
    print("  iarouter preguntar TEXTO")


def help():
    return (
        "Uso: iarouter [status|detectar|check|share|publicar|puente|usar|clave|modelos|modelo|preguntar] - "
        "Proveedor, LAN, puente, claves, modelos y petición explícita."
    )