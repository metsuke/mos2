"""Manifiesto SHA-256: estado, sembrar, aceptar, recargar."""

import subprocess

from moslib.core.integridad import (
    cargar_local,
    cargar_repo,
    copiar_repo_a_local,
    fallos,
    project_root,
    registrar,
    sha256_fichero,
)


def execute(args):
    args = list(args or [])
    cmd = args[0] if args else "estado"
    if cmd == "estado":
        loc = cargar_local()
        repo = cargar_repo()
        print(f"[integridad] local {len(loc)}  repo {len(repo)}")
        problemas = fallos("local")
        if not problemas:
            print("[integridad] local OK")
            return
        print(f"[integridad] {len(problemas)} fallo(s):")
        for linea in problemas[:20]:
            print(f"  {linea}")
        return
    if cmd == "recargar":
        dest = copiar_repo_a_local()
        print(f"[integridad] local ← repo  {dest}")
        return
    if cmd == "aceptar":
        if len(args) < 2:
            print("[integridad] Uso: integridad aceptar <ruta>")
            return
        rel = args[1].replace("\\", "/")
        hexaje = registrar(rel)
        print(f"[integridad] aceptado {rel} {hexaje}")
        return
    if cmd == "sembrar":
        root = project_root()
        r = subprocess.run(
            ["git", "ls-files"],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print("[integridad] git ls-files falló")
            return
        n = 0
        for rel in r.stdout.splitlines():
            rel = rel.strip()
            path = root / rel
            if rel and path.is_file():
                registrar(rel, sha256_fichero(path))
                n += 1
        print(f"[integridad] sembrados {n} ficheros")
        return
    print("[integridad] Uso: integridad estado|sembrar|aceptar <ruta>|recargar")


def help():
    return "Uso: integridad estado|sembrar|aceptar <ruta>|recargar"


def sinopsis():
    return [
        "integridad estado",
        "integridad sembrar",
        "integridad aceptar <ruta>",
        "integridad recargar",
    ]