"""Comando iarouter. Execute, help y sinopsis."""

from moslib.core import ia_bridge, ia_router
from moslib.core.iarouter_cmd import (
    cmd_check,
    cmd_clave,
    cmd_modelos,
    cmd_publicar,
    proveedor_y_resto,
)
from moslib.core.iarouter_cmd_share import cmd_connect, cmd_share
from moslib.core.iarouter_print import ofrecer_destino, print_detect, print_puente


def execute(args):
    if not args:
        print(help())
        return
    cmd = args[0].lower()
    if cmd in ("detectar", "detect"):
        items = ia_router.detectar()
        print_detect(items, "Detección de proveedores")
        ofrecer_destino(items)
        return
    if cmd == "estado":
        st = ia_router.status()
        print(f"Proveedor: {st['provider']}")
        print(f"Activo: {st['enabled']}")
        print(f"Modelo: {st.get('modelo', 'auto')}")
        if st.get("motivo"):
            print(st["motivo"])
        print_detect(st["disponibles"])
        return
    if cmd in ("usar", "use"):
        if len(args) < 2:
            print("Uso: iarouter usar jan|gpt4all|grok|openrouter")
            return
        ok, msg = ia_router.set_provider(args[1])
        print(msg)
        return
    if cmd == "check":
        cmd_check(args)
        return
    if cmd == "share":
        cmd_share()
        return
    if cmd == "connect":
        cmd_connect()
        return
    if cmd == "publicar":
        cmd_publicar()
        return
    if cmd == "clave":
        if len(args) < 2 or args[1].lower() not in ("grok", "openrouter"):
            print("Uso: iarouter clave grok|openrouter [borrar]")
            return
        cmd_clave(args)
        return
    if cmd in ("modelos", "models"):
        cmd_modelos(args)
        return
    if cmd == "modelo":
        pid, resto = proveedor_y_resto(args, 1)
        if not resto:
            print(f"Modelo activo: {ia_router.modelo_activo(pid)}")
            return
        ok, msg = ia_router.set_modelo(resto[0], pid)
        print(msg)
        return
    if cmd == "preguntar":
        if len(args) < 2:
            print("Uso: iarouter preguntar <texto>")
            return
        ok, text = ia_router.complete(" ".join(args[1:]))
        print(text)
        return
    if cmd == "puente":
        sub = args[1].lower() if len(args) > 1 else ""
        if sub == "on":
            print(ia_bridge.arrancar()[1])
        elif sub == "off":
            print(ia_bridge.parar()[1])
        elif sub == "estado":
            print_puente()
        else:
            print("Uso: iarouter puente on|off|estado")
        return
    print(help())


def help():
    return (
        "Uso: iarouter detectar|estado|usar <prov>|check [ámbito] [twitter] [detalle]| "
        "share|connect|publicar|clave grok|openrouter [borrar]|modelos [prov]| "
        "modelo [prov] [id]|preguntar <texto>|puente on|off|estado"
    )


def sinopsis():
    return [
        "iarouter",
        "iarouter detectar",
        "iarouter estado",
        "iarouter usar jan|gpt4all|grok|openrouter",
        "iarouter check [all|share|jan|gpt4all|grok|openrouter] [twitter] [detalle]",
        "iarouter share",
        "iarouter connect",
        "iarouter publicar",
        "iarouter clave grok|openrouter [borrar]",
        "iarouter modelos [prov]",
        "iarouter modelo [prov] [id]",
        "iarouter preguntar <texto>",
        "iarouter puente on|off|estado",
    ]
