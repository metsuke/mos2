"""Manifiesto SHA-256 canónico de ficheros tracked. Repo + copia .mos."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from moslib.core.integridad_sello import (
    comprobar_sello,
    escribir_sello,
    normalizar_eol,
    sello_path,
    sha256_canonico,
    sha256_canonico_bytes,
    sha256_fichero,
)
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
    return sha256_canonico_bytes(data)


def sha256_texto(texto: str) -> str:
    return sha256_canonico_bytes(texto.encode("utf-8"))


def sha256_crudo(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clase_fallo(linea: str) -> str:
    return linea.split(" ", 1)[0]


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
    return _leer(repo_path())


def cargar_local() -> dict:
    return _leer(local_path())


def guardar_ambos(mapa: dict) -> None:
    _escribir(repo_path(), mapa)
    _escribir(local_path(), mapa)


def copiar_repo_a_local() -> Path:
    return _escribir(local_path(), cargar_repo())


def alinear_local_con_repo() -> Path:
    dest = local_path()
    repo = repo_path()
    if not repo.is_file():
        return dest
    repo_ok = comprobar_sello(repo) is None
    if not dest.is_file() or not sello_path(dest).is_file():
        print("[integridad] Sin copia local. Se toma la del repositorio.")
        return copiar_repo_a_local()
    if comprobar_sello(dest) is not None and repo_ok:
        print("[integridad] local alineado al repo (sello local inválido).")
        return copiar_repo_a_local()
    if repo_ok and cargar_local() != cargar_repo():
        print("[integridad] local alineado al repo (post-pull).")
        return copiar_repo_a_local()
    return dest


def asegurar_local() -> Path:
    return alinear_local_con_repo()


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
    alinear_local_con_repo()
    root = project_root()
    out = []
    repo_mapa = cargar_repo()
    local_mapa = cargar_local()
    if repo_mapa and local_mapa and repo_mapa != local_mapa:
        out.append("desfase-local")
    for path in (repo_path(), local_path()):
        msg = comprobar_sello(path)
        if not msg:
            continue
        crudo = sha256_crudo(path) if path.is_file() else ""
        if path.is_file() and crudo != sha256_fichero(path):
            out.append(f"sello-eol {path.name} {msg}")
        else:
            out.append(msg)
    mapa = local_mapa if contra == "local" else repo_mapa
    for rel, esperado in mapa.items():
        f = root / rel
        if not f.is_file():
            out.append(f"falta {rel}")
            continue
        real = sha256_fichero(f)
        if real == esperado:
            if sha256_crudo(f) != esperado:
                out.append(f"eol {rel}")
            continue
        out.append(f"contenido {rel} esperado={esperado} real={real}")
    return out