"""Lectura, sello y fallos del manifiesto de integridad."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.integridad_sello import comprobar_sello, escribir_sello, normalizar_eol, sello_path
from moslib.core import integridad as nucleo


def _leer(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(normalizar_eol(path.read_bytes()).decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _escribir(path: Path, mapa: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordenado = {k: mapa[k] for k in sorted(mapa)}
    path.write_text(
        json.dumps(ordenado, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    escribir_sello(path)
    return path


def cargar_repo() -> dict:
    return _leer(nucleo.repo_path())


def cargar_local() -> dict:
    return _leer(nucleo.local_path())


def guardar_ambos(mapa: dict) -> None:
    _escribir(nucleo.repo_path(), mapa)
    _escribir(nucleo.local_path(), mapa)


def copiar_repo_a_local() -> Path:
    return _escribir(nucleo.local_path(), cargar_repo())


def alinear_local_con_repo() -> Path:
    dest = nucleo.local_path()
    repo = nucleo.repo_path()
    if not repo.is_file():
        return dest
    repo_ok = comprobar_sello(repo) is None
    if not dest.is_file() or not sello_path(dest).is_file():
        print("[integridad] Sin copia local. Se toma la del repositorio.")
        return copiar_repo_a_local()
    if comprobar_sello(dest) is not None and repo_ok:
        print("[integridad] local alineado al repo (sello local invalido).")
        return copiar_repo_a_local()
    if repo_ok and cargar_local() != cargar_repo():
        print("[integridad] local alineado al repo (post-pull).")
        return copiar_repo_a_local()
    return dest


def registrar(rel: str, digest: str | None = None) -> str:
    root = nucleo.project_root()
    path = (root / rel).resolve()
    path.relative_to(root.resolve())
    hexaje = digest or nucleo.sha256_fichero(path)
    clave = rel.replace("\\", "/")
    for destino in (nucleo.repo_path(), nucleo.local_path()):
        mapa = _leer(destino)
        mapa[clave] = hexaje
        _escribir(destino, mapa)
    return hexaje


def fallos(contra: str = "local") -> list:
    alinear_local_con_repo()
    root = nucleo.project_root()
    out = []
    repo_mapa = cargar_repo()
    local_mapa = cargar_local()
    if repo_mapa and local_mapa and repo_mapa != local_mapa:
        out.append("desfase-local")
    for path in (nucleo.repo_path(), nucleo.local_path()):
        msg = comprobar_sello(path)
        if not msg:
            continue
        crudo = nucleo.sha256_crudo(path) if path.is_file() else ""
        if path.is_file() and crudo != nucleo.sha256_fichero(path):
            out.append(f"sello-eol {path.name} {msg}")
        else:
            out.append(msg)
    mapa = local_mapa if contra == "local" else repo_mapa
    for rel, esperado in mapa.items():
        f = root / rel
        if not f.is_file():
            out.append(f"falta {rel}")
            continue
        real = nucleo.sha256_fichero(f)
        if real == esperado:
            if nucleo.sha256_crudo(f) != esperado:
                out.append(f"eol {rel}")
            continue
        out.append(f"contenido {rel} esperado={esperado} real={real}")
    return out
