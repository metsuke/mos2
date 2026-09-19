"""Comando docgen. Fuente JSON. generate no ingiere."""

from moslib.core import docgen as motor
from moslib.core import docgen_cli as cli
from moslib.core import docgen_cmd_run as run


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
        run.ingest(objetivo)
        return
    if cmd in ("generate", "gen"):
        run.generate(objetivo)
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
