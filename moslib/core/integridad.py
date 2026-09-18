"""Manifiesto SHA-256 de ficheros tracked. Repo + copia .mos."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from moslib.core.integridad_sello import comprobar_sello, escribir_sello
from moslib.core.user import ensure_user_space, get_username, get_user_mos_dir

MANIFIESTO_REL = Path("docs/docgen/integridad.json")


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def repo_path() -> Path:
    return project_root() / MANIFIESTO_REL


def local_path() -> Path:
    ensure_user_space(get_username())
    return get_user_mos_dir(get_username()) / "integridad.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_texto(texto: str) -> str:
    return sha256_bytes(texto.encode("utf-8"))


def sha256_fichero(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _leer(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _escribir(path: Path, mapa: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordenado = {k: mapa[k] for k in sorted(mapa)}
    path.write_text(json.dumps(ordenado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    escribir_sello(path)
    return path


def cargar_repo() -> dict:
    return _leer(repo_path())


def cargar_local() -> dict:
    return _leer(local_path())


def guardar_ambos(mapa: dict) -> None:
    _escribir(repo_path(), mapa)
    _escribir(local_path(), mapa)


def copiar_repo_a_local() -> Path:
    mapa = cargar_repo()
    dest = _escribir(local_path(), mapa)
    return dest


def registrar(rel: str, digest: str | None = None) -> str:
    root = project_root()
    path = (root / rel).resolve()
    path.relative_to(root.resolve())
    hexaje = digest or sha256_fichero(path)
    clave = rel.replace("\\", "/")
    for destino in (repo_path(), local_path()):
        mapa = _leer(destino)
        mapa[clave] = hexaje
        _escribir(destino, mapa)
    return hexaje


def fallos(contra: str = "local") -> list[str]:
    root = project_root()
    out = []
    for path in (repo_path(), local_path()):
        msg = comprobar_sello(path)
        if msg:
            out.append(msg)
    mapa = cargar_local() if contra == "local" else cargar_repo()
    for rel, esperado in mapa.items():
        path = root / rel
        if not path.is_file():
            out.append(f"falta {rel}")
            continue
        real = sha256_fichero(path)
        if real != esperado:
            out.append(f"{rel} esperado={esperado} real={real}")
    return out