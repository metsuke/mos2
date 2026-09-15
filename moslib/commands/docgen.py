"""
Comando docgen de MetsuOS.
Fachada del motor moslib.core.docgen. En esta fase: listar e inventario.
Aún no regenera markdown.
"""

from moslib.core import docgen as motor


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("list", "ls"):
        _listar()
        return
    cmd = args[0]
    if cmd == "backup-list":
        if len(args) < 2:
            print("[docgen] Falta el id del documento. Uso: docgen backup-list <id>")
            print("[docgen] Pista: docgen list")
            return
        _backup_list(args[1])
        return
    if cmd == "backup":
        if len(args) < 2:
            print("[docgen] Falta el id del documento. Uso: docgen backup <id>")
            return
        dest = motor.backup_document(args[1])
        if dest is None:
            print("[docgen] No se pudo copiar. Id desconocido o el fichero no existe.")
            print("[docgen] Pista: docgen list")
            return
        print(f"[docgen] Backup escrito en {dest}")
        return
    if cmd == "ingest" and (len(args) == 1 or args[1] in ("man", "all-man")):
        try:
            escritos = motor.ingest_man_faltantes()
        except Exception as exc:
            print(f"[docgen] Ingesta fallida: {exc}")
            return
        if not escritos:
            print("[docgen] Nada que absorber: todos los man ya tienen json.")
            return
        print("[docgen] Absorbidos:")
        for p in escritos:
            print(f"  {p}")
        return

    if cmd in ("generate", "gen") and (len(args) == 1 or args[1] in ("man", "all-man")):
        try:
            destinos = motor.generate_man_todos()
        except Exception as exc:
            print(f"[docgen] No se ha escrito el lote: {exc}")
            return
        print("[docgen] Regenerados:")
        for p in destinos:
            print(f"  {p}")
        return
    if cmd == "ingest" and len(args) >= 2:
        objetivo = args[1]
        nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
        try:
            dest = motor.ingest_man(nombre)
        except Exception as exc:
            print(f"[docgen] Ingesta fallida: {exc}")
            return
        print(f"[docgen] Absorbido en {dest}")
        print("[docgen] El markdown no se ha tocado. Sigue: docgen generate man-<cmd>")
        return
    if cmd in ("generate", "gen") and len(args) >= 2:
        objetivo = args[1]
        nombre = objetivo
        if objetivo.startswith("man-"):
            nombre = objetivo[4:]
        try:
            dest = motor.generate_man(nombre)
        except Exception as exc:
            print(f"[docgen] No se ha escrito: {exc}")
            print("[docgen] Pista: crea docs/docgen/man/<comando>.json o revisa help()")
            return
        print(f"[docgen] Regenerado {dest}")
        return
    print(f"[docgen] Subcomando no disponible aún: {cmd}")
    print("[docgen] Pista: docgen list | docgen backup <id> | docgen backup-list <id>")


def _listar():
    motor.ensure_docgen_dirs()
    print("[docgen] Documentos registrados:")
    for item in motor.DOCUMENTOS:
        path = motor.get_project_root() / item["rel"]
        marca = "ok" if path.is_file() else "falta"
        print(f"  {item['id']:22} {marca:5} {item['rel']}")


def _backup_list(doc_id):
    encontrados = motor.list_backups(doc_id)
    if not encontrados:
        print(f"[docgen] No hay backups para {doc_id}.")
        return
    print(f"[docgen] Backups de {doc_id}:")
    for p in encontrados:
        print(f"  {p.name}")


def help():
    return (
        "Uso: docgen [list|backup <id>|backup-list <id>] - "
        "Inventario y backup de documentos. La regeneración llega en fases siguientes."
    )