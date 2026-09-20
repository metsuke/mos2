"""iarouter share (anfitrión) y connect (cliente)."""

from moslib.core import ia_router, ia_share
from moslib.core.ia_check_share import check_share
from moslib.core.ia_share_run import aplicar_share
from moslib.core.iarouter_print import ofrecer_destino, print_lista


def cmd_share() -> None:
    print_lista(ia_share.diagnostico(), "Share LAN (diagnóstico)")
    print_lista(aplicar_share(), "Share LAN (secuencia)")


def cmd_connect() -> None:
    items = check_share(True)
    print_lista(items, "Connect LAN (cliente)")
    ofrecer_destino(items)
    ok, msg = ia_router.set_provider("jan")
    print(msg)
    if not ok:
        print("Si no hay Jan local, guarda la URL del anfitrión cuando se ofrezca.")
