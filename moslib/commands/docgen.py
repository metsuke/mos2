"""
Comando docgen de MetsuOS.
Fuente: JSON en docs/docgen/. generate no ingiere.
ingest solo primera vez o recuperación.
"""

from moslib.core import docgen as motor
from moslib.core import docgen_req as reqs


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("list", "ls"):
        _listar()
        return

    cmd = args[0]
    objetivo = args[1] if len(args) > 1 else ""

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
    print("[docgen] Edita docs/docgen JSON y luego: docgen generate <id|man|specs|pages|all>")


def _mostrar(titulo, paths):
    print(titulo)
    for path in paths:
        print(f"  {path}")


def _ingest(objetivo):
    print("[docgen] Ingesta: solo primera vez o recuperación.")
    try:
        if objetivo in ("reqs", "req", "requisitos"):
            escritos = reqs.ingest_reqs_srs()
            _mostrar("[docgen] Requisitos absorbidos:", escritos)
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
        "Uso: docgen generate man|specs|pages|all|<id> - "
        "Pinta markdown desde docs/docgen JSON. "
        "ingest man|specs|pages|reqs|all solo primera vez o recuperación."
    )