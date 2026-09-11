"""
moslib.core.entorno
Etiqueta corta del anfitrión para el prompt.
Ampliar: añadir una fila a ETIQUETAS o un detector en etiqueta().
"""

from __future__ import annotations

import sys
from pathlib import Path

# orden: primera que cumpla
ETIQUETAS = (
    ("wsl", "WSL"),
    ("win", "Windows nativo"),
    ("mac", "macOS"),
    ("nix", "Linux nativo"),
)


def es_wsl() -> bool:
    if Path("/mnt/c/Windows").is_dir():
        return True
    proc = Path("/proc/version")
    if proc.is_file():
        try:
            return "microsoft" in proc.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            return False
    return False


def etiqueta() -> str:
    if es_wsl():
        return "wsl"
    plat = sys.platform
    if plat.startswith("win"):
        return "win"
    if plat == "darwin":
        return "mac"
    if plat.startswith("linux"):
        return "nix"
    return plat[:3]


def descripcion(tag: str | None = None) -> str:
    tag = tag or etiqueta()
    for clave, texto in ETIQUETAS:
        if clave == tag:
            return texto
    return tag