"""Permiso en lotes de 50 y vista humana antes/despues."""

from __future__ import annotations

import os

from moslib.core.mos2ai_tools import resolver_ruta

LOTE = 50
_restantes = 0
ESCRITURA = frozenset({"escribir_fichero", "crear_fichero", "crear_directorio"})


def _pedir_lote(nombre: str) -> bool:
    global _restantes
    if _restantes > 0:
        _restantes -= 1
        print(f"[permiso] lote vigente, quedan {_restantes}")
        return True
    print(f"[permiso] {nombre}: conceder otro lote de {LOTE}? [S/n]")
    resp = input().strip().lower()
    if resp in ("", "s", "si", "sí"):
        _restantes = LOTE - 1
        print(f"[permiso] lote de {LOTE} concedido")
        return True
    print("[permiso] denegado")
    return False


def _vista(ruta: str, nuevo: str, append: bool) -> None:
    print("=" * 60)
    print(f"FICHERO: {ruta}")
    try:
        full = resolver_ruta(ruta)
        existe = os.path.isfile(full)
        antes = open(full, encoding="utf-8").read() if existe else ""
    except Exception as exc:
        existe = False
        antes = f"(no legible: {exc})"
    print("ANTES:" if existe else "ANTES: (no existe)")
    print(antes if antes else "(vacio)")
    print("-" * 60)
    despues = (antes + nuevo) if append and existe else nuevo
    print("DESPUES (append):" if append else "DESPUES:")
    print(despues if despues else "(vacio)")
    print("=" * 60)


def aplicar(nombre: str, args: dict, fn) -> str:
    if not _pedir_lote(nombre):
        return "Acceso denegado por el usuario."
    if nombre in ("escribir_fichero", "crear_fichero"):
        _vista(
            str(args.get("ruta_relativa") or ""),
            str(args.get("contenido") or ""),
            bool(args.get("append")),
        )
    elif nombre == "crear_directorio":
        print(f"DIRECTORIO A CREAR: {args.get('ruta_relativa')}")
    if fn is None:
        return "Funcion no reconocida."
    return fn(**args)
