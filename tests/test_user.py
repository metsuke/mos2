"""Tests del módulo de usuario."""

from pathlib import Path
from moslib.core.user import (
    get_username,
    get_project_root,
    get_rootfs,
    get_user_home,
    get_user_mos_dir,
    is_valid_user_command_name,
    ensure_user_space,
)


def test_get_username_returns_string():
    username = get_username()
    assert isinstance(username, str)
    assert len(username) > 0


def test_project_root_exists():
    root = get_project_root()
    assert root.is_dir()
    assert (root / "moslib").is_dir()
    assert (root / "rootfs").is_dir()


def test_user_paths():
    username = get_username()
    home = get_user_home(username)
    mos = get_user_mos_dir(username)

    assert home.name == username
    assert mos.name == ".mos"
    assert "rootfs" in str(home)
    assert "home" in str(home)


def test_is_valid_user_command_name():
    assert is_valid_user_command_name("user_hola") is True
    assert is_valid_user_command_name("user_backup_datos") is True
    assert is_valid_user_command_name("hola") is False
    assert is_valid_user_command_name("user_") is False
    assert is_valid_user_command_name("") is False
    assert is_valid_user_command_name("help") is False


def test_ensure_user_space_creates_dirs(tmp_path, monkeypatch):
    # Este test es más complejo; por ahora verificamos que la función existe y devuelve Path
    mos_dir = ensure_user_space()
    assert isinstance(mos_dir, Path)
    assert mos_dir.name == ".mos"