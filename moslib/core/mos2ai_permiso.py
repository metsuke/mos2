"""Permiso por comando: s una vez, S en tramos de 50 hasta 500."""

from __future__ import annotations

import os

from moslib.core.mos2ai_tools import resolver_ruta

PASO = 50
TOPE = 500
_restantes: dict[str, int] = {}
_tramo: dict[str, int] = {}


def _pedir(nombre: str) -> bool:
    quedan = _restantes.get(nombre, 0)
    if quedan > 0:
        _restantes[nombre] = quedan - 1
        print(f"[permiso] {nombre}: lote vigente, quedan {_restantes[nombre]}")
        return True
    siguiente = min(_tramo.get(nombre, 0) + PASO, TOPE)
    print(
        f"[permiso] {nombre}: s = solo esta vez; "
        f"S = lote de {siguiente} (tope {TOPE})"
    )
    resp = input().strip()
    if resp == "S":
        _tramo[nombre] = siguiente
        _restantes[nombre] = siguiente - 1
        print(f"[permiso] {nombre}: lote de {siguiente}")
        return True
    if resp == "s" or resp.lower() in ("si", "sí"):
        print(f"[permiso] {nombre}: solo esta vez")
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
    if not _pedir(nombre):
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
