from pathlib import Path

from moslib.core.cmd_loader import CommandManager

LEGAL = """
def execute(args):
    print("app-ok")

def help():
    return "Uso: app_fx_hola - prueba app"
"""


def test_loads_app_command(tmp_path):
    system = tmp_path / "sys"
    system.mkdir()
    (system / "help.py").write_text(
        "def execute(args):\n    print('sys')\ndef help():\n    return 'h'\n",
        encoding="utf-8",
    )
    apps = tmp_path / "apps" / "fx" / "commands"
    apps.mkdir(parents=True)
    (apps / "app_fx_hola.py").write_text(LEGAL, encoding="utf-8")
    mgr = CommandManager(system, apps_root=tmp_path / "apps")
    mod = mgr.get_command("app_fx_hola")
    assert mod is not None
    assert "prueba app" in mod.help()


def test_system_wins_over_app(tmp_path):
    system = tmp_path / "sys"
    system.mkdir()
    (system / "echo.py").write_text(
        "def execute(args):\n    print('sys')\ndef help():\n    return 'sys'\n",
        encoding="utf-8",
    )
    apps = tmp_path / "apps" / "fx" / "commands"
    apps.mkdir(parents=True)
    (apps / "echo.py").write_text(LEGAL, encoding="utf-8")
    mgr = CommandManager(system, apps_root=tmp_path / "apps")
    mod = mgr.get_command("echo")
    assert mod.help() == "sys"