from moslib.core.security import validate_command_source


LEGAL = """
from minimoslib.estado import load
import json
from moslib.core.user import get_username

def execute(args):
    print(load())

def help():
    return "Uso: x"
"""

BAD_LIB = """
import requests
def execute(args):
    pass
def help():
    return "x"
"""

BAD_APP = """
from apps.dev.commands import foo
def execute(args):
    pass
def help():
    return "x"
"""


def test_minimoslib_ok_if_file_exists(tmp_path):
    pkg = tmp_path / "minimoslib"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "estado.py").write_text("def load():\n    return 1\n", encoding="utf-8")
    ok, err = validate_command_source(LEGAL, app_dir=tmp_path)
    assert ok, err


def test_minimoslib_rejected_without_app_dir():
    ok, err = validate_command_source(LEGAL)
    assert not ok
    assert any("minimoslib" in e for e in err)


def test_requests_still_forbidden(tmp_path):
    (tmp_path / "minimoslib").mkdir()
    (tmp_path / "minimoslib" / "__init__.py").write_text("", encoding="utf-8")
    ok, _ = validate_command_source(BAD_LIB, app_dir=tmp_path)
    assert not ok


def test_apps_dev_commands_forbidden(tmp_path):
    (tmp_path / "minimoslib").mkdir()
    (tmp_path / "minimoslib" / "__init__.py").write_text("", encoding="utf-8")
    ok, _ = validate_command_source(BAD_APP, app_dir=tmp_path)
    assert not ok