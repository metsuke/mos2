"""Integridad de arranque. API real de integridad.py."""

from __future__ import annotations

import os
import sys

from moslib.core.integridad import (
    cargar_local,
    copiar_repo_a_local,
    fallos,
    repo_path,
)


def _pide_recargar() -> bool:
    env = os.environ.get("MOS_INTEGRIDAD", "").strip()
    return env == "recargar" or "--integridad-recargar" in sys.argv


def _es_aviso(linea: str) -> bool:
    baja = linea.lower()
    return "eol" in baja or "desfase" in baja


def comprobar_integridad() -> bool:
    try:
        from moslib.core.integridad import asegurar_local
        asegurar_local()
    except ImportError:
        pass
    if not repo_path().is_file() and not cargar_local():
        print("[integridad] sin manifiesto; integridad sembrar")
        return True
    if _pide_recargar() and repo_path().is_file():
        copiar_repo_a_local()
        print("[integridad] local cargado desde repo")
    problemas = fallos("local")
    avisos = [p for p in problemas if _es_aviso(p)]
    graves = [p for p in problemas if p not in avisos]
    for linea in avisos[:30]:
        print("[integridad] aviso " + linea)
    if not graves:
        print("[integridad] OK")
        return True
    print("[integridad] FALLO. El sistema no arranca.")
    for linea in graves[:30]:
        print("  " + linea)
    print("[integridad] write.sh o MOS_INTEGRIDAD=recargar")
    return False
