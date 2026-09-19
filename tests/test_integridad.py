"""Sellos y manifiesto. No bloquea si aún no hay semilla."""

from moslib.core.integridad import cargar_repo, fallos, repo_path
from moslib.core.integridad_sello import comprobar_sello


def test_sellos_si_hay_manifiesto():
    if not repo_path().is_file():
        return
    msg = comprobar_sello(repo_path())
    assert msg is None, msg


def test_repo_si_hay_entradas():
    if not cargar_repo():
        return
    problemas = [p for p in fallos("repo") if not p.startswith("falta sello")]
    assert problemas == [], "\n".join(problemas[:15])