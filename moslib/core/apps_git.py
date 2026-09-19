"""Instalar app desde repositorio git."""

from __future__ import annotations

import subprocess
from pathlib import Path

from moslib.core.user import get_project_root


def install_from_repo(url: str, ref: str | None = None) -> tuple[bool, str]:
    from moslib.core.apps import install_from_path

    cache = get_project_root() / ".mos-cache" / "app-repos"
    cache.mkdir(parents=True, exist_ok=True)
    name = url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    dest = cache / name
    try:
        if dest.exists():
            subprocess.run(
                ["git", "fetch", "--all"],
                cwd=str(dest),
                check=True,
                capture_output=True,
                text=True,
            )
            if ref:
                subprocess.run(
                    ["git", "checkout", ref],
                    cwd=str(dest),
                    check=True,
                    capture_output=True,
                    text=True,
                )
        else:
            cmd = ["git", "clone", url, str(dest)]
            if ref:
                cmd = ["git", "clone", "--branch", ref, url, str(dest)]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        return False, f"No se pudo clonar o actualizar el repo: {exc}"
    return install_from_path(dest)
