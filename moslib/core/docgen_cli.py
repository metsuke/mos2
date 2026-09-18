"""Subcomandos de docgen (no es un comando de MOSh)."""

from moslib.core import docgen as motor
from moslib.core import docgen_plan as planes
from moslib.core import docgen_req as reqs


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


def plan(args):
    if not args or args[0] == "list":
        items = planes.list_planes()
        if not items:
            print("[docgen] No hay planes. Primera vez: docgen ingest plans")
            return
        for item in items:
            print(f"  {item.get('id'):36} {item.get('estado') or '-'}")
        return
    try:
        if args[0] == "add" and len(args) >= 2:
            print(f"[docgen] Plan en {planes.plan_add(args[1], args[2] if len(args) > 2 else 'Diseñada')}")
            return
        if args[0] == "set" and len(args) >= 3:
            print(f"[docgen] Plan actualizado {planes.plan_set(args[1], 'estado', ' '.join(args[2:]))}")
            return
        if args[0] == "rm" and len(args) >= 2:
            print(f"[docgen] Plan metadato eliminado {planes.plan_rm(args[1])}")
            return
    except Exception as exc:
        print(f"[docgen] plan: {exc}")
        return
    print("[docgen] Uso: docgen plan list|add|set|rm")


def area(args):
    if not args or args[0] == "list":
        items = reqs.list_areas()
        if not items:
            print("[docgen] No hay áreas.")
            return
        for item in items:
            print(f"  {item.get('id'):8} {item.get('nombre') or ''}")
        return
    try:
        if args[0] == "add" and len(args) >= 2:
            print(f"[docgen] Área en {reqs.area_add(args[1], ' '.join(args[2:]) if len(args) > 2 else '')}")
            return
        if args[0] == "set" and len(args) >= 3:
            print(f"[docgen] Área actualizada {reqs.area_set(args[1], ' '.join(args[2:]))}")
            return
        if args[0] == "rm" and len(args) >= 2:
            print(f"[docgen] Área eliminada. {reqs.area_rm(args[1])}")
            return
    except Exception as exc:
        print(f"[docgen] area: {exc}")
        return
    print("[docgen] Uso: docgen area list|add|set|rm")


def req(args):
    if not args or args[0] == "list":
        items = reqs.list_reqs()
        if not items:
            print("[docgen] No hay requisitos.")
            return
        for item in items:
            print(f"  {item.get('id'):16} {item.get('area'):6} {item.get('prioridad') or '-':8} {item.get('texto') or ''}")
        return
    try:
        if args[0] == "add" and len(args) >= 3:
            print(f"[docgen] Creado {reqs.req_add(args[1], ' '.join(args[2:]))}")
            return
        if args[0] == "set" and len(args) >= 4:
            print(f"[docgen] Actualizado {reqs.req_set(args[1], args[2], ' '.join(args[3:]))}")
            return
        if args[0] == "rm" and len(args) >= 2:
            print(f"[docgen] Eliminado {reqs.req_rm(args[1])}")
            return
    except Exception as exc:
        print(f"[docgen] req: {exc}")
        return
    print("[docgen] Uso: docgen req list|add|set|rm")