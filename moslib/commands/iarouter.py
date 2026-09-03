"""Consulta el estado del enrutador de IA. No envía nada solo."""

from moslib.core import ia_router


def execute(args):
    args = list(args or [])
    if args and args[0] not in ("status",):
        print("Uso: iarouter [status]")
        return
    st = ia_router.status()
    print(f"proveedor: {st['provider']}")
    print(f"enabled: {st['enabled']}")
    print(f"providers: {', '.join(st['providers'])}")
    if st["motivo"]:
        print(f"motivo: {st['motivo']}")


def help():
    return (
        "Uso: iarouter [status] - Estado del enrutador de IA. "
        "Off por defecto. No envía prompts."
    )