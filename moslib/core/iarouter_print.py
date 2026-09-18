"""Salida por pantalla de iarouter. No es un comando."""

from moslib.core import ia_bridge, ia_router


def print_detect(items: list, titulo: str | None = None):
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


def print_lista(items: list, titulo: str):
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
        if d.get("accion"):
            print(f"Acción: {d['accion']}")


def ofrecer_destino(items: list):
    pol = ia_router.load_policy()
    vistos = set()
    for d in items:
        url = d.get("url") or ""
        if not url or "127.0.0.1" in url:
            continue
        if url in vistos:
            continue
        if "chat/completions" not in url and "1337" not in url and "4891" not in url:
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


def print_puente():
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