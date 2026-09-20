"""Secuencia anfitrión: diagnóstico + puente + publicar + diagnóstico."""

from moslib.core import ia_bridge, ia_share
from moslib.core.ia_check_net import item


def aplicar_share() -> list[dict]:
    out = []
    print("[share] 1/3 puente on")
    ok_p, msg_p = ia_bridge.arrancar()
    out.append(item("puente", ok_p, msg_p))
    print(msg_p)
    print("[share] 2/3 publicar")
    pubs = ia_share.publicar()
    out.extend(pubs)
    for row in pubs:
        print(f"  {row.get('id')}: {row.get('motivo') or row}")
    print("[share] 3/3 diagnóstico posterior")
    diags = ia_share.diagnostico()
    out.extend(diags)
    jan_ok = any(r.get("id") == "jan-lan" and r.get("ok") for r in diags)
    if jan_ok:
        out.append(item(
            "listo",
            True,
            "Jan visible en LAN. En el cliente: iarouter connect.",
        ))
    else:
        out.append(item(
            "listo",
            False,
            "Jan aún no responde en LAN. Perfil Privado y Jan en 0.0.0.0.",
        ))
    return out
