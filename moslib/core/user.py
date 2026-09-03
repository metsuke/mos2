"""
moslib.core.user
Gestión del usuario del sistema anfitrión y de su espacio personal en MetsuOS.

El espacio personal vive en:
    rootfs/home/<usuario>/.mos/

Incluye migración automática desde la ubicación antigua
(<project_root>/home/<usuario>/) para no romper instalaciones alpha existentes.
"""

import os
import getpass
import shutil
from pathlib import Path


def get_username() -> str:
    """Devuelve el nombre de usuario real del sistema operativo anfitrión."""
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
    """Ruta nueva (correcta): rootfs/home/<username>/"""
    if username is None:
        username = get_username()
    return get_rootfs() / "home" / username


def get_old_user_home(username: str | None = None) -> Path:
    """Ruta antigua (legacy): <project_root>/home/<username>/"""
    if username is None:
        username = get_username()
    return get_project_root() / "home" / username


def get_user_mos_dir(username: str | None = None) -> Path:
    """Ruta de la carpeta .mos del usuario (siempre la nueva)."""
    return get_user_home(username) / ".mos"


def _migrate_user_home_if_needed(username: str) -> None:
    """
    Migra automáticamente la carpeta de usuario desde la ubicación antigua
    a la nueva si es necesario.
    """
    old_home = get_old_user_home(username)
    new_home = get_user_home(username)

    # Caso 1: no existe la antigua → no hay nada que migrar
    if not old_home.exists():
        return

    # Caso 2: existe la antigua y NO existe la nueva → migrar
    if not new_home.exists():
        print(f"[MetsuOS] Migrando espacio de usuario de:")
        print(f"          {old_home}")
        print(f"          → {new_home}")
        try:
            # Aseguramos que rootfs/home exista
            new_home.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_home), str(new_home))
            print("[MetsuOS] Migración completada correctamente.")
        except Exception as e:
            print(f"[MetsuOS] ERROR al migrar el espacio de usuario: {e}")
            print("[MetsuOS] Se continuará usando la ubicación antigua temporalmente.")
        return

    # Caso 3: existen ambas → no tocamos nada, solo avisamos
    print(f"[MetsuOS] Aviso: existen tanto la carpeta antigua como la nueva de usuario.")
    print(f"          Antigua: {old_home}")
    print(f"          Nueva:   {new_home}")
    print("[MetsuOS] Se usará la nueva. Puedes borrar la antigua manualmente si lo deseas.")

def get_user_apps_dir(username: str | None = None) -> Path:
    return get_user_mos_dir(username) / "apps"

def ensure_user_space(username: str | None = None) -> Path:
    """
    1. Realiza la migración automática si es necesario.
    2. Crea la estructura completa de carpetas del usuario en la ubicación correcta.

    Estructura final:
    rootfs/home/<username>/
    └── .mos/
        ├── apps/
        ├── commands/
        ├── data/
        ├── config/
        ├── packages/
        └── repos/
    """
    if username is None:
        username = get_username()

    # 1. Migración automática (si aplica)
    _migrate_user_home_if_needed(username)

    # 2. Crear estructura en la ubicación nueva
    mos_dir = get_user_mos_dir(username)

    subdirs = [
        mos_dir / "apps",
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
    """Solo se permiten comandos de usuario que empiecen por 'user_'."""
    return isinstance(name, str) and name.startswith("user_") and len(name) > 5