"""Etiqueta del anfitrión y política de locale de arranque."""

from __future__ import annotations

import locale
import os
import sys
from pathlib import Path

from moslib.core.entorno_msg import URL_DUDH
from moslib.core.entorno_msg import mensaje_locale_bloqueado as _mensaje

ETIQUETAS = (
    ("wsl", "WSL"),
    ("win", "Windows nativo"),
    ("mac", "macOS"),
    ("nix", "Linux nativo"),
)
LOCALES_PERMITIDOS = ("es_ES",)


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


def _normaliza(valor: str) -> str:
    pieza = valor.strip().split(".")[0].split("@")[0]
    return pieza.replace("-", "_")


def locales_detectados() -> list[str]:
    crudos = []
    for clave in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        valor = os.environ.get(clave)
        if valor:
            crudos.append(valor)
    for fn in (locale.getlocale, locale.getdefaultlocale):
        try:
            par = fn()
        except Exception:
            par = None
        if par and par[0]:
            crudos.append(par[0])
    out = []
    for item in crudos:
        for parte in item.replace(":", ";").split(";"):
            norma = _normaliza(parte)
            if norma:
                out.append(norma)
    return out


def locale_permitido() -> bool:
    detectados = [x.lower() for x in locales_detectados()]
    for permitido in LOCALES_PERMITIDOS:
        clave = permitido.lower()
        if clave in detectados or any(x.startswith(clave + "_") for x in detectados):
            return True
    return False


def pide_simular_bloqueo(argv=None) -> bool:
    if os.environ.get("MOS2_SIMULAR_BLOQUEO_LOCALE", "").strip().lower() in (
        "1", "true", "si", "sí",
    ):
        return True
    return "--simular-bloqueo-locale" in list(argv or [])


def debe_bloquear_locale(argv=None) -> bool:
    return pide_simular_bloqueo(argv) or not locale_permitido()


def mensaje_locale_bloqueado(prueba: bool = False) -> str:
    vistos = ", ".join(locales_detectados()) or "(ninguno)"
    return _mensaje(vistos, prueba)
