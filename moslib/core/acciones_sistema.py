"""Registro de acciones de sistema ejecutables e integradas con control de permisos y exclusión de repositorios."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, List, Tuple

# Comandos de sistema prohibidos/excluidos de ejecución automatizada por riesgo en repositorios
COMANDOS_REPOSITORIO_EXCLUIDOS = {
    "git",
    "synccheck",
    "update",
    "test",
    "apps",
}


def listar_comandos_sistema() -> List[str]:
    """Lista todos los comandos oficiales disponibles en moslib.commands."""
    cmd_dir = Path(__file__).resolve().parent.parent / "commands"
    comandos = []
    for f in cmd_dir.glob("*.py"):
        if f.name.startswith("_"):
            continue
        nombre = f.stem
        if nombre not in COMANDOS_REPOSITORIO_EXCLUIDOS:
            comandos.append(nombre)
    return sorted(comandos)


def recomendar_ejecucion_manual(nombre: str) -> str:
    """Devuelve la recomendación para comandos de repositorio excluidos."""
    return (
        f"[SISTEMA DE SEGURIDAD] El comando '{nombre}' interactúa con repositorios "
        f"o control de cambios y está excluido de la ejecución automática por IA.\n"
        f"Recomendación: Ejecútalo manualmente desde MOSh escribiendo '{nombre}'."
    )


def ejecutar_accion_sistema(nombre: str, args: List[str]) -> Tuple[bool, str]:
    """Ejecuta un comando de sistema si es seguro, o advierte si es de repositorio."""
    if nombre in COMANDOS_REPOSITORIO_EXCLUIDOS:
        return False, recomendar_ejecucion_manual(nombre)
    
    try:
        mod = importlib.import_module(f"moslib.commands.{nombre}")
        if not hasattr(mod, "execute"):
            return False, f"El comando '{nombre}' no tiene función execute()."
        
        # Ejecutamos capturando salida o directamente
        ret = mod.execute(args)
        if ret is None or ret == 0:
            return True, f"Comando '{nombre}' ejecutado con éxito."
        else:
            return False, f"Comando '{nombre}' retornó código de error {ret}."
    except Exception as exc:
        return False, f"Error al ejecutar '{nombre}': {exc}"
