"""Comando apps: listar, ver, instalar (path local), quitar."""

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
            print(f"- {m['id']}  {m['version']}  {m['nombre']}")
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
        print("comandos: " + ", ".join(m["comandos"]))
        return
    if args[0] == "install" and len(args) >= 2:
        ok, msg = apps_core.install_from_path(args[1])
        print(msg)
        return
    if args[0] == "remove" and len(args) >= 2:
        ok, msg = apps_core.remove_app(args[1])
        print(msg)
        return
    print("Uso: apps [list|show <id>|install <ruta>|remove <id>]")


def help():
    return (
        "Uso: apps [list|show <id>|install <ruta>|remove <id>] - "
        "Gestiona apps locales (espacio .mos/apps). "
        "Sin A11Y/SEC la app no se instala."
    )