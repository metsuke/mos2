"""Sellos, manifiesto canónico, alineación local y clases de fallo."""

from pathlib import Path

from moslib.core.integridad import (
    alinear_local_con_repo,
    cargar_local,
    cargar_repo,
    clase_fallo,
    fallos,
    repo_path,
    sha256_bytes,
    sha256_fichero,
    sha256_texto,
)
from moslib.core.integridad_sello import (
    comprobar_sello,
    escribir_sello,
    normalizar_eol,
    sha256_canonico_bytes,
)


def test_normalizar_eol_crlf_y_cr():
    assert normalizar_eol(b"a\r\nb\rc\n") == b"a\nb\nc\n"


def test_mismo_hex_lf_crlf_cr():
    lf = b"hola\nmundo\n"
    crlf = b"hola\r\nmundo\r\n"
    cr = b"hola\rmundo\r"
    assert sha256_canonico_bytes(lf) == sha256_canonico_bytes(crlf)
    assert sha256_canonico_bytes(lf) == sha256_canonico_bytes(cr)
    assert sha256_bytes(crlf) == sha256_canonico_bytes(lf)
    assert sha256_texto("hola\r\nmundo\r\n") == sha256_texto("hola\nmundo\n")


def test_fichero_solo_eol_mismo_digest(tmp_path: Path):
    lf = tmp_path / "lf.txt"
    crlf = tmp_path / "crlf.txt"
    lf.write_bytes(b"x\ny\n")
    crlf.write_bytes(b"x\r\ny\r\n")
    assert sha256_fichero(lf) == sha256_fichero(crlf)


def test_cambio_no_eol_distinto(tmp_path: Path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"x\ny\n")
    b.write_bytes(b"x\nz\n")
    assert sha256_fichero(a) != sha256_fichero(b)


def test_sellos_si_hay_manifiesto():
    if not repo_path().is_file():
        return
    msg = comprobar_sello(repo_path())
    assert msg is None, msg


def test_repo_si_hay_entradas():
    if not cargar_repo():
        return
    graves = [
        p
        for p in fallos("repo")
        if clase_fallo(p) not in {"eol", "sello-eol", "desfase-local"}
        and not p.startswith("falta sello")
    ]
    assert graves == [], "\n".join(graves[:15])


def _parche_rutas(monkeypatch, root: Path):
    from moslib.core import integridad as mod

    repo = root / "docs" / "docgen" / "integridad.json"
    local = root / "mos" / "integridad.json"
    repo.parent.mkdir(parents=True, exist_ok=True)
    local.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(mod, "project_root", lambda: root)
    monkeypatch.setattr(mod, "repo_path", lambda: repo)
    monkeypatch.setattr(mod, "local_path", lambda: local)
    return repo, local


def test_alinear_local_viejo_copia_repo(monkeypatch, tmp_path: Path):
    from moslib.core.integridad import _escribir

    repo, local = _parche_rutas(monkeypatch, tmp_path)
    _escribir(repo, {"a.txt": "nuevo"})
    _escribir(local, {"a.txt": "viejo"})
    alinear_local_con_repo()
    assert cargar_local() == {"a.txt": "nuevo"}


def test_sello_crlf_no_es_contenido(monkeypatch, tmp_path: Path):
    from moslib.core.integridad import _escribir

    repo, local = _parche_rutas(monkeypatch, tmp_path)
    tracked = tmp_path / "ok.txt"
    tracked.write_bytes(b"ok\n")
    digest = sha256_fichero(tracked)
    _escribir(repo, {"ok.txt": digest})
    _escribir(local, {"ok.txt": digest})
    crudo = repo.read_bytes().replace(b"\n", b"\r\n")
    repo.write_bytes(crudo)
    assert comprobar_sello(repo) is None
    problemas = fallos("local")
    graves = [p for p in problemas if clase_fallo(p) in {"contenido", "falta"}]
    assert graves == [], "\n".join(graves)


def test_mutacion_real_es_contenido(monkeypatch, tmp_path: Path):
    from moslib.core.integridad import _escribir

    repo, local = _parche_rutas(monkeypatch, tmp_path)
    tracked = tmp_path / "x.py"
    tracked.write_bytes(b"ok\n")
    digest = sha256_fichero(tracked)
    _escribir(repo, {"x.py": digest})
    _escribir(local, {"x.py": digest})
    tracked.write_bytes(b"ko\n")
    problemas = fallos("local")
    assert any(p.startswith("contenido x.py") for p in problemas)