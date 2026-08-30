"""
Comando synccheck de MetsuOS.
Compara HEAD local con origin/main tras git fetch.
"""

import subprocess
from pathlib import Path


def _root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _run(args, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def execute(args):
    root = _root()
    print("[synccheck] fetch origin...")
    fetch = _run(["git", "fetch", "origin"], root)
    if fetch.returncode != 0:
        print("[synccheck] Error: no se pudo hacer git fetch origin.")
        if fetch.stderr:
            print(fetch.stderr.rstrip())
        print("Comprueba red y que este directorio es un clone Git.")
        return

    local = _run(["git", "rev-parse", "HEAD"], root)
    remote = _run(["git", "rev-parse", "origin/main"], root)
    if local.returncode != 0 or remote.returncode != 0:
        print("[synccheck] Error: no hay HEAD o no existe origin/main.")
        return

    local_sha = local.stdout.strip()
    remote_sha = remote.stdout.strip()
    print(f"[synccheck] HEAD local:     {local_sha}")
    print(f"[synccheck] origin/main:    {remote_sha}")

    if local_sha == remote_sha:
        print("[synccheck] Estado: sincronizado (mismo commit).")
    else:
        print("[synccheck] Estado: NO sincronizado.")
        print("Pega esta salida a la IA. En el clone: git pull origin main")
        print("o publica tus commits si vas por delante.")

    poetry = _run(["git", "show", "origin/main:pyproject.toml"], root)
    if poetry.returncode == 0:
        for line in poetry.stdout.splitlines():
            if line.strip().startswith("version"):
                print(f"[synccheck] Poetry en origin/main: {line.strip()}")
                break

    readme = _run(["git", "show", "origin/main:README.md"], root)
    if readme.returncode == 0:
        for line in readme.stdout.splitlines():
            if "Versión:" in line or "Version:" in line:
                print(f"[synccheck] README en origin/main: {line.strip()}")
                break

    print("[synccheck] Raw fiable: https://raw.githubusercontent.com/metsuke/mos2/" + remote_sha + "/")


def help():
    return (
        "Uso: synccheck - Fetch origin y compara HEAD local con origin/main. "
        "Muestra SHAs, si coinciden, versión Poetry/README en origin/main y la URL raw por SHA."
    )