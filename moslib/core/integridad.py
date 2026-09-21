"""Manifiesto SHA-256 canonico. Repo + copia .mos."""

from __future__ import annotations

import hashlib
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


def _mapa():
    from moslib.core import integridad_map as modulo
    return modulo


def _escribir(path, mapa):
    return _mapa()._escribir(path, mapa)


def cargar_repo():
    return _mapa().cargar_repo()


def cargar_local():
    return _mapa().cargar_local()


def guardar_ambos(mapa: dict):
    return _mapa().guardar_ambos(mapa)


def copiar_repo_a_local():
    return _mapa().copiar_repo_a_local()


def alinear_local_con_repo():
    return _mapa().alinear_local_con_repo()


def asegurar_local():
    return alinear_local_con_repo()


def registrar(rel: str, digest: str | None = None) -> str:
    return _mapa().registrar(rel, digest)


def fallos(contra: str = "local") -> list:
    return _mapa().fallos(contra)
