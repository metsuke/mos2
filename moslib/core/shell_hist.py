"""Historial de MOSh (readline). Tope de entradas y de tamaño."""

from __future__ import annotations

import atexit
from pathlib import Path

MAX_ENTRADAS = 1000
MAX_BYTES = 256 * 1024


def _ruta(mos_dir: Path) -> Path:
    mos_dir.mkdir(parents=True, exist_ok=True)
    return mos_dir / "historial"


def recortar(path: Path) -> None:
    if not path.is_file():
        return
    raw = path.read_bytes()
    if len(raw) <= MAX_BYTES:
        return
    texto = raw.decode("utf-8", errors="replace")
    lineas = texto.splitlines()
    while lineas and len(("\n".join(lineas) + "\n").encode("utf-8")) > MAX_BYTES:
        lineas = lineas[1:]
    if len(lineas) > MAX_ENTRADAS:
        lineas = lineas[-MAX_ENTRADAS:]
    path.write_text("\n".join(lineas) + ("\n" if lineas else ""), encoding="utf-8")


def cargar_historial(mos_dir: Path) -> Path | None:
    try:
        import readline
    except ImportError:
        return None
    path = _ruta(mos_dir)
    recortar(path)
    try:
        if path.is_file():
            readline.read_history_file(str(path))
    except OSError:
        pass
    readline.set_history_length(MAX_ENTRADAS)

    def _guardar() -> None:
        try:
            readline.write_history_file(str(path))
            recortar(path)
        except OSError:
            pass

    atexit.register(_guardar)
    return path