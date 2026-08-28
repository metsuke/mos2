"""Comprueba que la versión de producto en pyproject.toml es SemVer X.Y.Z."""

from pathlib import Path
import re
import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = PROJECT_ROOT / "pyproject.toml"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def _poetry_version() -> str:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    return data["tool"]["poetry"]["version"]


def test_pyproject_exists():
    assert PYPROJECT.is_file()


def test_poetry_version_is_semver_xyz():
    version = _poetry_version()
    assert SEMVER.match(version), (
        f"pyproject.toml version debe ser X.Y.Z, no {version!r}"
    )