"""CRUD CLI de plan/area/req."""

from moslib.core import docgen_plan as planes
from moslib.core import docgen_req as reqs


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
            print(
                f"  {item.get('id'):16} {item.get('area'):6} "
                f"{item.get('prioridad') or '-':8} {item.get('texto') or ''}"
            )
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
