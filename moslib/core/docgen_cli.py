"""Subcomandos de docgen (no es un comando de MOSh)."""

from moslib.core import docgen as motor
from moslib.core.docgen_cli_crud import area, plan, req


def mostrar(titulo, paths):
    print(titulo)
    for path in paths:
        print(f"  {path}")


def listar():
    motor.ensure_docgen_dirs()
    print("[docgen] Documentos registrados:")
    for item in motor.todos_documentos():
        path = motor.get_project_root() / item["rel"]
        marca = "ok" if path.is_file() else "falta"
        print(f"  {item['id']:22} {marca:5} {item['rel']}")


def crud(nombre, args, lister, add, setter, rm, uso_add, uso_set, uso_rm):
    if not args or args[0] == "list":
        items = lister()
        if not items:
            print(f"[docgen] No hay {nombre}.")
            return
        for item in items:
            yield item
        return
    accion = args[0]
    try:
        if accion == "add":
            print(add(args) if args else uso_add)
            return
        if accion == "set":
            print(setter(args) if args else uso_set)
            return
        if accion == "rm":
            print(rm(args) if args else uso_rm)
            return
    except Exception as exc:
        print(f"[docgen] {nombre}: {exc}")
        return
    print(f"[docgen] Uso: docgen {nombre} list|add|set|rm")
