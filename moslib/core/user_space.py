"""Migración y creación del espacio personal .mos."""

from __future__ import annotations

import shutil

from moslib.core.user import (
    get_old_user_home,
    get_user_home,
    get_user_mos_dir,
    get_username,
)


def migrate_user_home_if_needed(username: str) -> None:
    old_home = get_old_user_home(username)
    new_home = get_user_home(username)
    if not old_home.exists():
        return
    if not new_home.exists():
        print("[MetsuOS] Migrando espacio de usuario de:")
        print(f"          {old_home}")
        print(f"          → {new_home}")
        try:
            new_home.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_home), str(new_home))
            print("[MetsuOS] Migración completada correctamente.")
        except Exception as e:
            print(f"[MetsuOS] ERROR al migrar el espacio de usuario: {e}")
            print("[MetsuOS] Se continuará usando la ubicación antigua temporalmente.")
        return
    print("[MetsuOS] Aviso: existen tanto la carpeta antigua como la nueva de usuario.")
    print(f"          Antigua: {old_home}")
    print(f"          Nueva:   {new_home}")
    print("[MetsuOS] Se usará la nueva. Puedes borrar la antigua manualmente si lo deseas.")


def ensure_user_space(username: str | None = None):
    if username is None:
        username = get_username()
    migrate_user_home_if_needed(username)
    mos_dir = get_user_mos_dir(username)
    for d in (
        mos_dir / "apps",
        mos_dir / "commands",
        mos_dir / "data",
        mos_dir / "config",
        mos_dir / "packages",
        mos_dir / "repos",
    ):
        d.mkdir(parents=True, exist_ok=True)
    return mos_dir
