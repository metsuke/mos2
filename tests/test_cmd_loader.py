"""Tests del cargador de comandos y de la integración de seguridad."""

import textwrap
from pathlib import Path

from moslib.core.cmd_loader import CommandManager


def test_system_command_loads(tmp_path):
    system_dir = tmp_path / "system"
    system_dir.mkdir()
    (system_dir / "echo.py").write_text(textwrap.dedent("""
        def execute(args):
            print("hola")
        def help():
            return "echo help"
    """))

    manager = CommandManager(system_commands_dir=system_dir, enforce_security=True)
    mod = manager.get_command("echo")
    assert mod is not None
    assert hasattr(mod, "execute")


def test_user_command_with_forbidden_import_is_rejected(tmp_path):
    system_dir = tmp_path / "system"
    user_dir = tmp_path / "user"
    system_dir.mkdir()
    user_dir.mkdir()

    # Comando de usuario con import prohibido
    (user_dir / "user_malicious.py").write_text(textwrap.dedent("""
        import requests
        def execute(args):
            pass
        def help():
            return "malicious"
    """))

    manager = CommandManager(
        system_commands_dir=system_dir,
        user_commands_dir=user_dir,
        enforce_security=True,
    )

    mod = manager.get_command("user_malicious")
    assert mod is None  # Debe ser rechazado


def test_user_command_allowed_imports_loads(tmp_path):
    system_dir = tmp_path / "system"
    user_dir = tmp_path / "user"
    system_dir.mkdir()
    user_dir.mkdir()

    (user_dir / "user_hola.py").write_text(textwrap.dedent("""
        import os
        from pathlib import Path
        def execute(args):
            print("hola seguro")
        def help():
            return "hola help"
    """))

    manager = CommandManager(
        system_commands_dir=system_dir,
        user_commands_dir=user_dir,
        enforce_security=True,
    )

    mod = manager.get_command("user_hola")
    assert mod is not None
    assert hasattr(mod, "execute")

    # También por nombre corto
    mod2 = manager.get_command("hola")
    assert mod2 is not None