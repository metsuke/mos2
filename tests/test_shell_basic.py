"""Tests básicos del shell y del espacio de usuario."""

from moslib.core.user import get_username, ensure_user_space, get_user_mos_dir
from pathlib import Path


def test_ensure_user_space_returns_mos_dir():
    mos_dir = ensure_user_space()
    assert isinstance(mos_dir, Path)
    assert mos_dir.name == ".mos"
    assert mos_dir.exists()
    assert (mos_dir / "commands").is_dir()
    assert (mos_dir / "data").is_dir()


def test_username_is_non_empty():
    username = get_username()
    assert isinstance(username, str)
    assert len(username) > 0