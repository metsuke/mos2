"""Historial de líneas de MOSh (flechas arriba/abajo), estilo bash."""

from __future__ import annotations

import atexit
from pathlib import Path

HISTFILE = "mosh_history"
HIST_MAX = 1000


def cargar_historial(mos_dir: Path) -> Path | None:
    try:
        import readline
    except ImportError:
        print("[mosh] Este anfitrión no tiene readline; no hay historial.")
        return None
    dest = Path(mos_dir) / HISTFILE
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file():
        try:
            readline.read_history_file(str(dest))
        except OSError:
            pass
    readline.set_history_length(HIST_MAX)

    def _guardar():
        try:
            readline.write_history_file(str(dest))
        except OSError:
            pass

    atexit.register(_guardar)
    return dest