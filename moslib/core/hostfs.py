"""Rutas y procesos de anfitrión anclados a la raíz del clone."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def resolver(rel: str) -> Path:
    raw = (rel or "").strip()
    if not raw or raw in (".", "./"):
        return project_root()
    root = project_root().resolve()
    cand = Path(raw)
    destino = cand.resolve() if cand.is_absolute() else (root / raw).resolve()
    try:
        destino.relative_to(root)
    except ValueError:
        raise ValueError(f"ruta fuera del clone: {rel}")
    return destino


def run_host(argv: list[str]) -> int:
    if not argv:
        raise ValueError("falta el programa")
    prog = argv[0]
    binario = shutil.which(prog)
    if binario is None:
        raise FileNotFoundError(f"no está en el PATH del anfitrión: {prog}")
    done = subprocess.run([binario, *argv[1:]], cwd=str(project_root()))
    return int(done.returncode)