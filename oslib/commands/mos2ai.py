"""mos2ai: chat agentico. Al rotar no devuelve el prompt al humano."""

import json

from moslib.core.mos2ai_bucle import anotar, montar, rotar, ultimo_encargo

HERRAMIENTAS = ("listar_directorio", "leer_fichero", "fin")


def execute(args):
    if not args or args[0].lower() in ("chat", "seguir"):
        modelo = args[1] if len(args) > 1 else "auto"
        _chat(modelo)
        return
    cmd = args[0].lower()
    if cmd == "encargo":
        texto = " ".join(args[1:]).strip()
        if not texto:
            print("Uso: mos2ai encargo <texto>")
            return
        anotar("acciones", "user", texto)
        print("Encargo guardado. mos2ai chat continua con el.")
        return
    if cmd == "investigacion":
        texto = " ".join(args[1:]).strip()
        if not texto:
            print("Uso: mos2ai investigacion <texto>")
            return
        anotar("investigacion", "system", texto)
        print("Investigacion guardada.")
        return
    print(help())


def _chat(modelo: str) -> None:
    if not ultimo_encargo():
        print(f"[Tu - {modelo}]:")
        return
    print(f"[mos2ai] chat con {modelo}. Si hay cuota, sigo sin preguntarte.")
    activo = modelo
    pendiente = ""
    while True:
        activo, parar, pendiente = _turno(activo, pendiente)
        if parar:
            return


def _turno(modelo: str, pendiente: str) -> tuple[str, bool, str]:
    from moslib.core import ia_router

    extra = pendiente or ultimo_encargo()
    mensajes = montar()
    mensajes.append({
        "role": "user",
        "content": (
            "Agente MetsuOS. Solo JSON: "
            '{"tipo":"decir","texto":"..."} o '
            '{"tipo":"herramienta","nombre":"listar_directorio|leer_fichero|fin","args":""}. '
            "Continua el encargo. No esperes al humano.\n" + extra
        ),
    })
    ok, texto = ia_router.complete(json.dumps(mensajes, ensure_ascii=False), {"modelo": modelo})
    if not ok and "cuota" in texto.lower():
        siguiente = "siguiente"
        print(f"[!] Cuota. Siguiente: {siguiente}")
        print("[mos2ai] paso contexto y encargo. No abro [Tu].")
        rotar(siguiente, pendiente, lambda msgs: ia_router.complete(json.dumps(msgs), {"modelo": siguiente})[1])
        return siguiente, False, pendiente
    if not ok:
        print(texto)
        return modelo, True, ""
    anotar("acciones", "assistant", texto, modelo)
    orden = _parsear(texto)
    if orden.get("tipo") != "herramienta":
        print(orden.get("texto") or texto)
        return modelo, False, ""
    nombre = str(orden.get("nombre") or "")
    if nombre == "fin":
        return modelo, True, ""
    print(f"[cliente] ejecutando 1 vez: {nombre}")
    resultado = f"herramienta {nombre} args={orden.get('args') or ''}"
    print(f"[mos2ai] devuelvo {nombre} al modelo y sigo.")
    anotar("acciones", "assistant", resultado, modelo)
    return modelo, False, resultado


def _parsear(texto: str) -> dict:
    bruto = texto.strip()
    try:
        data = json.loads(bruto)
    except json.JSONDecodeError:
        return {"tipo": "decir", "texto": texto}
    return data if isinstance(data, dict) else {"tipo": "decir", "texto": texto}


def help():
    return "Uso: mos2ai chat [modelo]|encargo <texto>|investigacion <texto>"


def sinopsis():
    return [
        "mos2ai",
        "mos2ai chat [modelo]",
        "mos2ai encargo <texto>",
        "mos2ai investigacion <texto>",
    ]