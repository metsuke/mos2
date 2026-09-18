"""Registrar hash tras escribir un documento docgen."""

from pathlib import Path

from moslib.core.docgen_index import get_project_root
from moslib.core.integridad import registrar


def registrar_destino(dest: Path) -> str:
    root = get_project_root().resolve()
    rel = dest.resolve().relative_to(root).as_posix()
    return registrar(rel)
