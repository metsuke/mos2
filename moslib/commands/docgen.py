"""
Comando docgen de MetsuOS.
Fuente: JSON. generate no ingiere.
"""

from moslib.core import docgen as motor
from moslib.core import docgen_plan as planes
from moslib.core import docgen_req as reqs


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("list", "ls"):
        _listar()
        return
    cmd = args[0]
    objetivo = args[1] if len(args) > 1 else ""
    if cmd == "req":
        _req(args[1:])
        return
    if cmd == "area":
        _area(args[1:])
        return
    if cmd in ("plan", "planes"):
        _plan(args[1:])
        return
    if cmd == "ingest":
        _ingest(objetivo)
        return
    if cmd in ("generate", "gen"):
        _generate(objetivo)
        return
    if cmd == "backup-list":
        if not objetivo:
            print("[docgen] Uso: docgen backup-list <id>")
            return
        encontrados = motor.list_backups(objetivo)
        if not encontrados:
            print(f"[docgen] No hay backups para {objetivo}.")
            return
        print(f"[docgen] Backups de {objetivo}:")
        for path in encontrados:
            print(f"  {path.name}")
        return
    if cmd == "backup":
        if not objetivo:
            print("[docgen] Uso: docgen backup <id>")
            return
        dest = motor.backup_document(objetivo)
        if dest is None:
            print("[docgen] No se pudo copiar.")
            return
        print(f"[docgen] Backup escrito en {dest}")
        return
    print(f"[docgen] Subcomando no disponible: {cmd}")
    print("[docgen] generate | req | area | plan | ingest | list | backup")


def _plan(args):
    if not args or args[0] == "list":
        items = planes.list_planes()
        if not items:
            print("[docgen] No hay planes en docs/docgen/plans/")
            print("[docgen] Primera vez: docgen ingest plans")
            return
        for item in items:
            print(
                f"  {item.get('id'):36} {item.get('estado') or '-'}"
            )
        return
    accion = args[0]
    try:
        if accion == "add":
            if len(args) < 2:
                print("[docgen] Uso: docgen plan add YYYY-MM-DD-NN-slug.md [estado]")
                return
            estado = args[2] if len(args) > 2 else "Diseñada"
            dest = planes.plan_add(args[1], estado)
            print(f"[docgen] Plan en {dest}")
            return
        if accion == "set":
            if len(args) < 3:
                print("[docgen] Uso: docgen plan set <id> estado")
                return
            dest = planes.plan_set(args[1], "estado", " ".join(args[2:]))
            print(f"[docgen] Plan actualizado {dest}")
            return
        if accion == "rm":
            if len(args) < 2:
                print("[docgen] Uso: docgen plan rm <id>")
                return
            dest = planes.plan_rm(args[1])
            print(f"[docgen] Plan metadato eliminado {dest}")
            return
    except Exception as exc:
        print(f"[docgen] plan: {exc}")
        return
    print("[docgen] Uso: docgen plan list|add|set|rm")


def _area(args):
    if not args or args[0] == "list":
        items = reqs.list_areas()
        if not items:
            print("[docgen] No hay áreas.")
            return
        for item in items:
            print(f"  {item.get('id'):8} {item.get('nombre') or ''}")
        return
    accion = args[0]
    try:
        if accion == "add":
            if len(args) < 2:
                print("[docgen] Uso: docgen area add ID [nombre]")
                return
            dest = reqs.area_add(args[1], " ".join(args[2:]) if len(args) > 2 else "")
            print(f"[docgen] Área en {dest}")
            return
        if accion == "set":
            if len(args) < 3:
                print("[docgen] Uso: docgen area set ID nombre")
                return
            dest = reqs.area_set(args[1], " ".join(args[2:]))
            print(f"[docgen] Área actualizada {dest}")
            return
        if accion == "rm":
            if len(args) < 2:
                print("[docgen] Uso: docgen area rm ID")
                return
            dest = reqs.area_rm(args[1])
            print(f"[docgen] Área eliminada. {dest}")
            return
    except Exception as exc:
        print(f"[docgen] area: {exc}")
        return
    print("[docgen] Uso: docgen area list|add|set|rm")


def _req(args):
    if not args or args[0] == "list":
        items = reqs.list_reqs()
        if not items:
            print("[docgen] No hay requisitos en docs/docgen/reqs/")
            return
        for item in items:
            print(
                f"  {item.get('id'):16} {item.get('area'):6} "
                f"{item.get('prioridad') or '-':8} {item.get('texto') or ''}"
            )
        return
    accion = args[0]
    try:
        if accion == "add":
            if len(args) < 3:
                print("[docgen] Uso: docgen req add REQ-AREA-000 texto")
                return
            dest = reqs.req_add(args[1], " ".join(args[2:]))
            print(f"[docgen] Creado {dest}")
            return
        if accion == "set":
            if len(args) < 4:
                print("[docgen] Uso: docgen req set REQ-AREA-000 campo valor")
                return
            dest = reqs.req_set(args[1], args[2], " ".join(args[3:]))
            print(f"[docgen] Actualizado {dest}")
            return
        if accion == "rm":
            if len(args) < 2:
                print("[docgen] Uso: docgen req rm REQ-AREA-000")
                return
            dest = reqs.req_rm(args[1])
            print(f"[docgen] Eliminado {dest}")
            return
    except Exception as exc:
        print(f"[docgen] req: {exc}")
        return
    print("[docgen] Uso: docgen req list|add|set|rm")


def _mostrar(titulo, paths):
    print(titulo)
    for path in paths:
        print(f"  {path}")


def _ingest(objetivo):
    print("[docgen] Ingesta: solo primera vez o recuperación.")
    try:
        if objetivo in ("plans", "plan", "planes"):
            _mostrar("[docgen] Planes absorbidos:", planes.ingest_planes())
            return
        if objetivo in ("reqs", "req", "requisitos"):
            _mostrar("[docgen] Requisitos absorbidos:", reqs.ingest_reqs_srs())
            return
        if objetivo in ("", "man", "all-man"):
            _mostrar("[docgen] Absorbidos:", motor.ingest_man_todos(forzar=True))
            return
        if objetivo in ("specs", "spec", "all-specs"):
            _mostrar("[docgen] Absorbidos:", motor.ingest_spec_todos(forzar=True))
            return
        if objetivo in ("pages", "page", "docs"):
            _mostrar("[docgen] Absorbidos:", motor.ingest_page_todos(forzar=True))
            return
        if objetivo in ("all", "todo"):
            _mostrar("[docgen] Absorbidos:", motor.ingest_todo())
            return
        if objetivo.startswith("man-") or objetivo in motor.list_man_nombres():
            nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
            print(f"[docgen] Absorbido en {motor.ingest_man(nombre)}")
            return
        print(f"[docgen] Absorbido en {motor.ingest_doc(objetivo)}")
    except Exception as exc:
        print(f"[docgen] Ingesta fallida: {exc}")


def _generate(objetivo):
    try:
        if objetivo in ("", "man", "all-man"):
            _mostrar("[docgen] Regenerados:", motor.generate_man_todos())
            return
        if objetivo in ("specs", "spec", "all-specs"):
            _mostrar("[docgen] Regenerados:", motor.generate_spec_todos())
            return
        if objetivo in ("pages", "page", "docs"):
            _mostrar("[docgen] Regenerados:", motor.generate_page_todos())
            return
        if objetivo in ("all", "todo"):
            _mostrar("[docgen] Regenerados:", motor.generate_todo())
            return
        if objetivo.startswith("man-") or objetivo in motor.list_man_nombres():
            nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
            print(f"[docgen] Regenerado {motor.generate_man(nombre)}")
            return
        print(f"[docgen] Regenerado {motor.generate_doc(objetivo)}")
    except Exception as exc:
        print(f"[docgen] No se ha escrito: {exc}")


def _listar():
    motor.ensure_docgen_dirs()
    print("[docgen] Documentos registrados:")
    for item in motor.todos_documentos():
        path = motor.get_project_root() / item["rel"]
        marca = "ok" if path.is_file() else "falta"
        print(f"  {item['id']:22} {marca:5} {item['rel']}")


def help():
    return (
        "Uso: docgen generate ... | docgen req ... | docgen area ... | "
        "docgen plan list|add|set|rm | docgen ingest plans|... "
        "(ingest solo recuperación)."
    )

def sinopsis():
    return [
        "docgen list",
        "docgen generate man|specs|pages|all|<id>",
        "docgen req list|add|set|rm",
        "docgen area list|add|set|rm",
        "docgen plan list|add|set|rm",
        "docgen ingest man|specs|pages|reqs|plans|all|<id>",
        "docgen backup <id>",
        "docgen backup-list <id>",
    ]