"""Comando apps: listar, ver, instalar (path o repo), quitar."""

from moslib.core import apps as apps_core


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("list", "ls"):
        items = apps_core.list_apps()
        if not items:
            print("No hay apps instaladas.")
            return
        print("Apps instaladas:")
        for m in items:
            ambito = m.get("ambito", "usuario")
            print(f"- {m['id']}  {m['version']}  {ambito}  {m['nombre']}")
        return
    if args[0] == "show" and len(args) >= 2:
        m = apps_core.show_app(args[1])
        if not m:
            print(f"No está instalada: {args[1]}")
            return
        print(f"id: {m['id']}")
        print(f"nombre: {m['nombre']}")
        print(f"version: {m['version']}")
        print(f"acceso: {m['acceso']}")
        print(f"ambito: {m.get('ambito', 'usuario')}")
        print("comandos: " + ", ".join(m["comandos"]))
        return
    if args[0] == "install" and len(args) >= 2:
        src = args[1]
        ref = args[2] if len(args) >= 3 else None
        if src.endswith(".git") or src.startswith("git@") or src.startswith("http"):
            ok, msg = apps_core.install_from_repo(src, ref)
        else:
            ok, msg = apps_core.install_from_path(src)
        print(msg)
        return
    if args[0] == "remove" and len(args) >= 2:
        ok, msg = apps_core.remove_app(args[1])
        print(msg)
        return
    print("Uso: apps [list|show <id>|install <ruta|url> [ref]|remove <id>]")


def help():
    return (
        "Uso: apps [list|show <id>|install <ruta|url> [ref]|remove <id>] - "
        "Instala apps desde el clone o un repo git. "
        "ambito usuario o sistema según app.json. "
        "Sin SEC/A11Y no se instala."
    )