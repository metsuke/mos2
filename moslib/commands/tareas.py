"""Comando tareas: listar, crear manual, marcar, tick."""

from moslib.core import tasks as T


def execute(args):
    args = list(args or [])
    if not args or args[0] in ("list", "ls"):
        items = T.load_all()
        if not items:
            print("No hay tareas.")
            return
        print("Tareas (manuales y automáticas):")
        for t in items:
            print(T.format_line(t))
        return
    if args[0] == "add" and len(args) >= 2:
        cmd = " ".join(args[1:])
        t = T.create_task(comando=cmd)
        print("Creada: " + T.format_line(t))
        return
    if args[0] == "hecha" and len(args) >= 2:
        t = T.set_estado(args[1], "hecha")
        print("No existe." if not t else "OK: " + T.format_line(t))
        return
    if args[0] == "tick":
        log = T.tick()
        if not log:
            print("Tick: nada que reencolar.")
            return
        for line in log:
            print(line)
        return
    print("Uso: tareas [list|add <comando>|hecha <id>|tick]")


def help():
    return (
        "Uso: tareas [list|add <comando>|hecha <id>|tick] - "
        "Tareas locales. bloqueada_a11y_sec no se ejecuta."
    )