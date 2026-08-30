"""Tests de accesibilidad baseline (marca a11y)."""

from pathlib import Path

import pytest

from moslib.commands import a11y as a11y_cmd
from moslib.commands import docs as docs_cmd
from moslib.commands import help as help_cmd


ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.a11y
def test_a11y_policy_and_declaration_exist():
    assert (ROOT / "docs" / "A11Y.md").is_file()
    assert (ROOT / "docs" / "a11y" / "DECLARACION.md").is_file()
    assert (ROOT / "docs" / "a11y" / "informe.md").is_file()
    assert (ROOT / "docs" / "a11y" / "informe.json").is_file()


@pytest.mark.a11y
def test_a11y_command_contract():
    assert callable(a11y_cmd.execute)
    text = a11y_cmd.help()
    assert isinstance(text, str) and text.strip()


@pytest.mark.a11y
def test_docs_command_contract():
    assert callable(docs_cmd.execute)
    text = docs_cmd.help()
    assert isinstance(text, str) and text.strip()


@pytest.mark.a11y
def test_help_returns_non_empty():
    text = help_cmd.help()
    assert isinstance(text, str) and text.strip()


@pytest.mark.a11y
def test_security_prefix_documented_in_sec():
    sec = (ROOT / "docs" / "specs" / "04-SEC-Security-Policy.md").read_text(encoding="utf-8")
    assert "[SEGURIDAD]" in sec