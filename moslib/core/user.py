"""
moslib.core.user
Gestión del usuario del sistema anfitrión y de su espacio personal en MetsuOS.
"""

import os
import getpass
from pathlib import Path


def get_username() -> str:
    """
    Devuelve el nombre de usuario real del sistema operativo anfitrión.
    Nunca hardcodeado.
    """
    try:
        return getpass.getuser()
    except Exception:
        return (
            os.environ.get("USER")
            or os.environ.get("USERNAME")
            or os.environ.get("LOGNAME")
            or "usuario"
        )


def get_project_root() -> Path:
    """
    Devuelve la raíz del proyecto MOS2 de forma fiable
    (donde están las carpetas moslib/ y home/).
    """
    # Este archivo está en moslib/core/user.py
    current = Path(__file__).resolve()
    # Subimos: core/ → moslib/ → raíz del proyecto
    return current.parent.parent.parent


def get_user_home(username: str | None = None) -> Path:
    """
    Ruta completa de la carpeta personal del usuario:
    <project_root>/home/<username>/
    """
    if username is None:
        username = get_username()
    return get_project_root() / "home" / username


def get_user_mos_dir(username: str | None = None) -> Path:
    """
    Ruta de la carpeta .mos del usuario:
    <project_root>/home/<username>/.mos/
    """
    return get_user_home(username) / ".mos"


def ensure_user_space(username: str | None = None) -> Path:
    """
    Crea (si no existe) toda la estructura de carpetas del usuario.

    Estructura:
    home/<username>/
    └── .mos/
        ├── commands/      ← solo archivos user_*.py
        ├── data/
        ├── config/
        ├── packages/
        └── repos/

    Devuelve la ruta de .mos/
    """
    if username is None:
        username = get_username()

    mos_dir = get_user_mos_dir(username)

    subdirs = [
        mos_dir / "commands",
        mos_dir / "data",
        mos_dir / "config",
        mos_dir / "packages",
        mos_dir / "repos",
    ]

    for d in subdirs:
        d.mkdir(parents=True, exist_ok=True)

    return mos_dir


def is_valid_user_command_name(name: str) -> bool:
    """
    Un comando de usuario SOLO es válido si empieza por 'user_'
    y tiene contenido después del prefijo.
    """
    return isinstance(name, str) and name.startswith("user_") and len(name) > 5