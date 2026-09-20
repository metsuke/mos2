"""Check LAN/share de iarouter."""

from moslib.core.ia_check_net import SERVICIOS, item
from moslib.core.ia_check_share_hechos import hechos_share


def decidir_share(h: dict) -> tuple[str, str, str]:
    if h["urls"]:
        return (
            "Esta instancia ya ve una compartición usable.",
            "Cuando pregunte si guardar la URL, responde s. "
            "Después: iarouter usar jan   y   iarouter preguntar hola",
            h["urls"][0],
        )
    loc = h["local"]
    if (not h["wsl"]) and (loc["jan"] or loc["gpt4all"] or loc["puente"]):
        if h["perfil"] and "Public" in h["perfil"]:
            return (
                "Hay servidor local, pero esta red Windows está en perfil Público.",
                "Pon la red en Privada. Luego: iarouter publicar.",
                "",
            )
        if not h["puente_sesion"]:
            return (
                "Hay Jan en localhost y no hay puente en esta sesión.",
                "iarouter puente on    Luego: iarouter publicar",
                "",
            )
        return ("Hay servicio local. Esta instancia usa 127.0.0.1.", "Deja este MOSh abierto.", "")
    if h["wsl"]:
        return (
            "Estás en WSL y no se alcanza Jan ni el puente. "
            f"IPs: {', '.join(h.get('probadas') or []) or 'ninguna'}.",
            "En Git Bash: puente on y publicar.",
            "",
        )
    return (
        "Aquí no hay servidor local ni se ve ninguno ajeno.",
        "En el win que comparte: puente on, publicar. Aquí: iarouter check.",
        "",
    )


def check_share(detalle: bool) -> list[dict]:
    h = hechos_share()
    conclusion, accion, url = decidir_share(h)
    out = [item("conclusion", bool(url), conclusion, url), item("accion", True, accion, url)]
    if not detalle:
        return out
    out.append(
        item(
            "detalle-entorno",
            h["wsl"],
            f"wsl={h['wsl']} ip_lan={h['ip_lan']} win={h['ips_windows']}",
        )
    )
    out.append(item("detalle-puente-sesion", h["puente_sesion"], "puente en ESTE MOSh"))
    for n, p in SERVICIOS:
        out.append(
            item(
                f"detalle-listen-{n}",
                h["local"][n],
                f"local={h['local'][n]} lan={h['lan_ok'][n]} puerto={p}",
            )
        )
    out.extend(h["pruebas"])
    return out
