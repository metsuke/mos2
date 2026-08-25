"""Tests básicos del comando man."""

import importlib.util
from pathlib import Path

from moslib.core.user import get_project_root


def _load_man_module():
    path = get_project_root() / "moslib" / "commands" / "man.py"
    spec = importlib.util.spec_from_file_location("man", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_man_module_has_contract():
    module = _load_man_module()
    assert hasattr(module, "execute") and callable(module.execute)
    assert hasattr(module, "help") and callable(module.help)
    assert isinstance(module.help(), str)
    assert module.help().strip()


def test_man_pages_directory_exists_and_has_pages():
    man_dir = get_project_root() / "docs" / "man"
    assert man_dir.is_dir()
    pages = list(man_dir.glob("*.md"))
    assert pages, "docs/man/ debe contener páginas .md"