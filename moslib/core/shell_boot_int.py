"""Integridad de arranque. No bloquea por avisos de eol."""

from __future__ import annotations

import os
import sys

from moslib.core.integridad import (
    alinear_local_con_repo,
    cargar_local,
    clase_fallo,
    copiar_repo_a_local,
    fallos,
    repo_path,
)

_AVISOS = {"eol", "sello-eol", "desfase-local"}
_GRAVE = {"contenido", "falta"}


def _pide_recargar() -> bool:
    env = os.environ.get("MOS_INTEGRIDAD", "").strip()
    return env == "recargar" or "--integridad-recargar" in sys.argv


def comprobar_integridad() -> bool:
    if not repo_path().is_file() and not cargar_local():
        print("[integridad] sin manifiesto; integridad sembrar")
        return True
    if _pide_recargar() and repo_path().is_file():
        copiar_repo_a_local()
        print("[integridad] local cargado desde repo")
    elif repo_path().is_file():
        alinear_local_con_repo()
    problemas = fallos("local")
    avisos = []
    graves = []
    for linea in problemas:
        clase = clase_fallo(linea)
        if clase in _AVISOS:
            avisos.append(linea)
        elif clase in _GRAVE or linea.startswith("sello roto"):
            graves.append(linea)
        elif linea.startswith("falta sello") or linea.startswith("falta manifiesto"):
            graves.append(linea)
    for linea in avisos[:30]:
        print("[integridad] aviso " + linea)
    if not graves:
        print("[integridad] OK")
        return True
    print("[integridad] FALLO. El sistema no arranca.")
    for linea in graves[:30]:
        print("  " + linea)
    print("[integridad] write en multi, o: integridad aceptar / recargar")
    print("[integridad] emergencia: MOS_INTEGRIDAD=recargar")
    return False
