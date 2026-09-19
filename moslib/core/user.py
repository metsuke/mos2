"""Usuario del anfitrión y rutas de su espacio personal en MetsuOS."""

import os
import getpass
from pathlib import Path


def get_username() -> str:
    """Nombre de usuario real del SO anfitrión."""
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
    """Raíz del proyecto (donde están moslib/ y rootfs/)."""
    current = Path(__file__).resolve()
    return current.parent.parent.parent


def get_rootfs() -> Path:
    return get_project_root() / "rootfs"


def get_user_home(username: str | None = None) -> Path:
    """Ruta nueva: rootfs/home/<username>/"""
    if username is None:
        username = get_username()
    return get_rootfs() / "home" / username


def get_old_user_home(username: str | None = None) -> Path:
    """Ruta antigua: <project_root>/home/<username>/"""
    if username is None:
        username = get_username()
    return get_project_root() / "home" / username


def get_user_mos_dir(username: str | None = None) -> Path:
    return get_user_home(username) / ".mos"


def get_user_apps_dir(username: str | None = None) -> Path:
    return get_user_mos_dir(username) / "apps"


def get_system_apps_dir() -> Path:
    d = get_rootfs() / "opt" / "apps"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _migrate_user_home_if_needed(username: str) -> None:
    from moslib.core.user_space import migrate_user_home_if_needed as _fn
    return _fn(username)


def ensure_user_space(username: str | None = None):
    from moslib.core.user_space import ensure_user_space as _fn
    return _fn(username)


def is_valid_user_command_name(name: str) -> bool:
    return isinstance(name, str) and name.startswith("user_") and len(name) > 5
