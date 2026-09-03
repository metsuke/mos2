from pathlib import Path

from moslib.core import apps as apps_core


def _write_app(root: Path, app_id: str, cmd_name: str, body: str) -> Path:
    app = root / app_id
    (app / "commands").mkdir(parents=True)
    (app / "app.json").write_text(
        (
            '{"id": "%s", "nombre": "T", "version": "0.0.1", '
            '"comandos": ["%s"], "acceso": "local-owner"}'
        )
        % (app_id, cmd_name),
        encoding="utf-8",
    )
    (app / "commands" / f"{cmd_name}.py").write_text(body, encoding="utf-8")
    return app


LEGAL = """
def execute(args):
    print("ok")

def help():
    return "Uso: app_fx_hola - prueba"
"""

ILLEGAL = """
import jander

def execute(args):
    print("no")

def help():
    return "x"
"""


def test_install_legal_list_remove(tmp_path, monkeypatch):
    monkeypatch.setattr(apps_core, "_apps_root", lambda: tmp_path / "installed")
    src = _write_app(tmp_path, "fx", "app_fx_hola", LEGAL)
    ok, msg = apps_core.install_from_path(src)
    assert ok, msg
    ids = [m["id"] for m in apps_core.list_apps()]
    assert "fx" in ids
    ok, _ = apps_core.remove_app("fx")
    assert ok
    assert apps_core.list_apps() == []


def test_reject_illegal_import(tmp_path, monkeypatch):
    monkeypatch.setattr(apps_core, "_apps_root", lambda: tmp_path / "installed")
    src = _write_app(tmp_path, "bad", "app_bad_x", ILLEGAL)
    ok, msg = apps_core.install_from_path(src)
    assert not ok
    assert "No se acepta" in msg


def test_reject_system_name_clash(tmp_path, monkeypatch):
    monkeypatch.setattr(apps_core, "_apps_root", lambda: tmp_path / "installed")
    src = _write_app(tmp_path, "clash", "help", LEGAL)
    ok, msg = apps_core.install_from_path(src)
    assert not ok
    assert "pisa" in msg