"""Subcomandos de iarouter: check, clave, modelos."""

from __future__ import annotations

import getpass

from moslib.core import ia_check, ia_keys, ia_router, ia_share
from moslib.core.iarouter_print import ofrecer_destino, print_lista


def parse_check_args(args: list) -> tuple[str, str | None, bool]:
    detalle = False
    scope = "all"
    extra = None
    tokens = [a.lower() for a in args[1:]]
    flags = {"detalle", "-v", "verbose", "--verbose"}
    clean = []
    for t in tokens:
        if t in flags:
            detalle = True
        else:
            clean.append(t)
    if not clean:
        return scope, extra, detalle
    if clean[0] in ia_check.SCOPES or clean[0] == "share":
        scope = clean[0]
        if len(clean) >= 2 and clean[1] in ("twitter", "x", "cliente"):
            extra = clean[1]
    elif clean[0] in ("twitter", "x"):
        scope = "grok"
        extra = "twitter"
    else:
        print(f"Ámbito desconocido: {clean[0]}")
        print("Usa: all|share|jan|gpt4all|grok|openrouter  [twitter]")
        scope = "all"
    return scope, extra, detalle


def pedir_clave(pid: str) -> None:
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


def proveedor_y_resto(args, inicio: int):
    if len(args) <= inicio:
        return None, []
    if args[inicio].lower() in ia_router.PROVIDERS:
        return args[inicio].lower(), args[inicio + 1 :]
    return None, args[inicio:]


def cmd_check(args: list) -> None:
    scope, extra, detalle = parse_check_args(args)
    titulo = "Check de iarouter"
    if scope != "all":
        titulo += f" [{scope}" + (f"/{extra}" if extra else "") + "]"
    if detalle:
        titulo += " (detalle)"
    items = ia_check.check(detalle=detalle, scope=scope, extra=extra)
    print_lista(items, titulo)
    if scope in ("all", "share", "jan", "gpt4all"):
        ofrecer_destino(items)


def cmd_share() -> None:
    print_lista(ia_share.diagnostico(), "Share LAN")


def cmd_publicar() -> None:
    print_lista(ia_share.publicar(), "Publicar (autorización explícita)")


def cmd_clave(args: list) -> None:
    pid = args[1].lower()
    if len(args) >= 3 and args[2] in ("borrar", "delete"):
        ok, msg = ia_keys.delete_key(pid)
        print(msg)
        return
    if ia_keys.has_stored_key(pid):
        print(f"Ya hay clave de {pid} en .mos. No se muestra.")
        print(f"Para sustituirla: iarouter clave {pid}")
        print(f"Para borrarla: iarouter clave {pid} borrar")
    pedir_clave(pid)


def cmd_modelos(args: list) -> None:
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