"""Herramientas de fichero del puente mos2ai. Sandbox = cwd."""

from __future__ import annotations

import os


def resolver_ruta(ruta_relativa: str) -> str:
    base = os.path.abspath(os.getcwd())
    destino = os.path.abspath(os.path.join(base, ruta_relativa or "."))
    if not (destino == base or destino.startswith(base + os.sep)):
        raise ValueError(f"Ruta fuera del sandbox: {ruta_relativa}")
    return destino


def listar_directorio(ruta_relativa: str = ".") -> str:
    try:
        full = resolver_ruta(ruta_relativa)
        entradas = os.listdir(full)
        if not entradas:
            return f"(vacío) {ruta_relativa}"
        lineas = []
        for nombre in sorted(entradas):
            ruta = os.path.join(full, nombre)
            lineas.append(nombre + ("/" if os.path.isdir(ruta) else ""))
        return "\n".join(lineas)
    except Exception as exc:
        return f"Error al listar {ruta_relativa}: {exc}"


def leer_fichero(ruta_relativa: str) -> str:
    try:
        with open(resolver_ruta(ruta_relativa), encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        return f"Error al leer {ruta_relativa}: {exc}"


def escribir_fichero(ruta_relativa: str, contenido: str, append: bool = False) -> str:
    try:
        full = resolver_ruta(ruta_relativa)
        padre = os.path.dirname(full)
        if padre:
            os.makedirs(padre, exist_ok=True)
        with open(full, "a" if append else "w", encoding="utf-8") as f:
            f.write(contenido if contenido is not None else "")
        accion = "añadido" if append else "escrito"
        return f"OK: {accion} en {ruta_relativa} ({len(contenido or '')} chars)"
    except Exception as exc:
        return f"Error al escribir {ruta_relativa}: {exc}"


def crear_fichero(ruta_relativa: str, contenido: str = "") -> str:
    return escribir_fichero(ruta_relativa, contenido, append=False)


def crear_directorio(ruta_relativa: str) -> str:
    try:
        os.makedirs(resolver_ruta(ruta_relativa), exist_ok=True)
        return f"OK: directorio listo: {ruta_relativa}"
    except Exception as exc:
        return f"Error al crear directorio {ruta_relativa}: {exc}"


HERRAMIENTAS = [
    listar_directorio,
    leer_fichero,
    escribir_fichero,
    crear_fichero,
    crear_directorio,
]
DISPATCH = {fn.__name__: fn for fn in HERRAMIENTAS}
