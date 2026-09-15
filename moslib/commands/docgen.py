"""
Comando docgen de MetsuOS.
Fachada de moslib.core.docgen.
"""

from moslib.core import docgen as motor


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("list", "ls"):
        _listar()
        return

    cmd = args[0]

    if cmd == "ingest":
        objetivo = args[1] if len(args) > 1 else "man"
        if objetivo in ("man", "all-man"):
            try:
                escritos = motor.ingest_man_todos(forzar=True)
            except Exception as exc:
                print(f"[docgen] Ingesta fallida: {exc}")
                return
            if not escritos:
                print("[docgen] No hay páginas man que absorber.")
                return
            print("[docgen] Absorbidos:")
            for path in escritos:
                print(f"  {path}")
            return
        nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
        try:
            dest = motor.ingest_man(nombre)
        except Exception as exc:
            print(f"[docgen] Ingesta fallida: {exc}")
            return
        print(f"[docgen] Absorbido en {dest}")
        return

    if cmd in ("generate", "gen"):
        objetivo = args[1] if len(args) > 1 else "man"
        if objetivo in ("man", "all-man"):
            try:
                destinos = motor.generate_man_todos()
            except Exception as exc:
                print(f"[docgen] No se ha escrito el lote: {exc}")
                return
            print("[docgen] Regenerados:")
            for path in destinos:
                print(f"  {path}")
            return
        nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
        try:
            dest = motor.generate_man(nombre)
        except Exception as exc:
            print(f"[docgen] No se ha escrito: {exc}")
            return
        print(f"[docgen] Regenerado {dest}")
        return

    if cmd == "backup-list":
        if len(args) < 2:
            print("[docgen] Uso: docgen backup-list <id>")
            return
        encontrados = motor.list_backups(args[1])
        if not encontrados:
            print(f"[docgen] No hay backups para {args[1]}.")
            return
        print(f"[docgen] Backups de {args[1]}:")
        for path in encontrados:
            print(f"  {path.name}")
        return

    if cmd == "backup":
        if len(args) < 2:
            print("[docgen] Uso: docgen backup <id>")
            return
        dest = motor.backup_document(args[1])
        if dest is None:
            print("[docgen] No se pudo copiar. Id desconocido o el fichero no existe.")
            return
        print(f"[docgen] Backup escrito en {dest}")
        return

    print(f"[docgen] Subcomando no disponible: {cmd}")
    print("[docgen] Pista: docgen list | ingest man | generate man")


def _listar():
    motor.ensure_docgen_dirs()
    print("[docgen] Documentos registrados:")
    for item in motor.todos_documentos():
        path = motor.get_project_root() / item["rel"]
        marca = "ok" if path.is_file() else "falta"
        print(f"  {item['id']:22} {marca:5} {item['rel']}")


def help():
    return (
        "Uso: docgen [list|ingest man|generate man|backup <id>|backup-list <id>] - "
        "Inventario, ingesta y regeneración de documentos."
    )