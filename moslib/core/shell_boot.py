"""Tests de arranque: barra, x/y, %, nombre, hasta 7 hilos."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HILOS = 7
RE_FIN = re.compile(r"(PASSED|FAILED|SKIPPED|ERROR)")
RE_NOMBRE = re.compile(r"(\S+::\S+)")


def _xdist() -> bool:
    try:
        import xdist  # noqa: F401

        return True
    except ImportError:
        return False


def _contar_tests() -> int:
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    texto = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+)\s+(?:tests collected|selected|items)", texto)
    if m:
        return int(m.group(1))
    return sum(1 for line in texto.splitlines() if "::" in line)


def _pinta(hecho: int, total: int, nombre: str) -> None:
    ancho = 28
    pct = int(100 * hecho / total) if total else 0
    n = int(ancho * hecho / total) if total else 0
    barra = "█" * n + "░" * (ancho - n)
    corto = nombre[-48:] if len(nombre) > 48 else nombre
    xy = f"{hecho}/{total}" if total else str(hecho)
    print(f"\r[tests] {barra} {xy} {pct:3d}% {corto:<48}", end="", flush=True)


def run_startup_tests() -> tuple[bool, str]:
    workers = _xdist()
    modo = f"{HILOS} hilos" if workers else "1 hilo (instala pytest-xdist para 7)"
    print(f"[MetsuOS] Tests de arranque ({modo})...")
    total = _contar_tests()
    cmd = [sys.executable, "-m", "pytest", "-v", "--tb=line", "-s"]
    if workers:
        cmd.extend(["-n", str(HILOS), "--dist", "load"])
    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    buf = []
    hecho = 0
    actual = "recogiendo…"
    _pinta(0, total, actual)
    assert proc.stdout is not None
    for raw in proc.stdout:
        buf.append(raw)
        line = raw.strip()
        nom = RE_NOMBRE.search(line)
        if nom:
            actual = nom.group(1)
            _pinta(hecho, total, actual)
        if RE_FIN.search(line) and "::" in line:
            hecho += 1
            _pinta(hecho, total, actual)
    codigo = proc.wait()
    print()
    texto = "".join(buf)
    for linea in texto.splitlines():
        if linea.startswith("[tope]"):
            print(linea)
    if codigo == 0:
        print("[MetsuOS] Tests de arranque: OK\n")
        return True, texto
    print("[MetsuOS] Error: fallo en los tests de arranque.")
    print(texto)
    print("El sistema no arrancará hasta que todos los tests pasen.")
    return False, texto