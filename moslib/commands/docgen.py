"""Comando docgen. Fuente JSON. generate no ingiere."""

from moslib.core import docgen as motor
from moslib.core import docgen_cli as cli
from moslib.core import docgen_plan as planes
from moslib.core import docgen_req as reqs


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("list", "ls"):
        cli.listar()
        return
    cmd = args[0]
    objetivo = args[1] if len(args) > 1 else ""
    if cmd == "req":
        cli.req(args[1:])
        return
    if cmd == "area":
        cli.area(args[1:])
        return
    if cmd in ("plan", "planes"):
        cli.plan(args[1:])
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
        print(f"[docgen] Backups de {objetivo}:" if encontrados else f"[docgen] No hay backups para {objetivo}.")
        for path in encontrados:
            print(f"  {path.name}")
        return
    if cmd == "backup":
        if not objetivo:
            print("[docgen] Uso: docgen backup <id>")
            return
        dest = motor.backup_document(objetivo)
        print("[docgen] No se pudo copiar." if dest is None else f"[docgen] Backup escrito en {dest}")
        return
    print(f"[docgen] Subcomando no disponible: {cmd}")


def _ingest(objetivo):
    print("[docgen] Ingesta: solo primera vez o recuperación.")
    try:
        if objetivo in ("plans", "plan", "planes"):
            cli.mostrar("[docgen] Planes absorbidos:", planes.ingest_planes())
        elif objetivo in ("reqs", "req", "requisitos"):
            cli.mostrar("[docgen] Requisitos absorbidos:", reqs.ingest_reqs_srs())
        elif objetivo in ("", "man", "all-man"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_man_todos(forzar=True))
        elif objetivo in ("specs", "spec", "all-specs"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_spec_todos(forzar=True))
        elif objetivo in ("pages", "page", "docs"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_page_todos(forzar=True))
        elif objetivo in ("all", "todo"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_todo())
        elif objetivo.startswith("man-") or objetivo in motor.list_man_nombres():
            nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
            print(f"[docgen] Absorbido en {motor.ingest_man(nombre)}")
        else:
            print(f"[docgen] Absorbido en {motor.ingest_doc(objetivo)}")
    except Exception as exc:
        print(f"[docgen] Ingesta fallida: {exc}")


def _generate(objetivo):
    try:
        if objetivo in ("", "man", "all-man"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_man_todos())
        elif objetivo in ("specs", "spec", "all-specs"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_spec_todos())
        elif objetivo in ("pages", "page", "docs"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_page_todos())
        elif objetivo in ("all", "todo"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_todo())
        elif objetivo.startswith("man-") or objetivo in motor.list_man_nombres():
            nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
            print(f"[docgen] Regenerado {motor.generate_man(nombre)}")
        else:
            print(f"[docgen] Regenerado {motor.generate_doc(objetivo)}")
    except Exception as exc:
        print(f"[docgen] No se ha escrito: {exc}")


def help():
    return (
        "Uso: docgen generate ... | docgen req ... | docgen area ... | "
        "docgen plan list|add|set|rm | docgen ingest ... (solo recuperación)."
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