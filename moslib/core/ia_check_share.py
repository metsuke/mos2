"""Check LAN/share de iarouter."""

from __future__ import annotations

from moslib.core import ia_bridge
from moslib.core.ia_check_host import ips_windows, listen, pasarela, perfil_windows
from moslib.core.ia_check_net import (
    SERVICIOS,
    es_wsl,
    http,
    ipv4_propia,
    item,
    tcp,
)


def _puente_sesion() -> bool:
    try:
        return bool(ia_bridge.estado().get("activo"))
    except Exception:
        return False


def hechos_share() -> dict:
    lan = ipv4_propia()
    win_ips = ips_windows()
    extra = pasarela()
    propias = set(lan)
    ip_lan = lan[0] if lan else None
    lis = {n: listen(p) for n, p in SERVICIOS}
    local = {n: tcp("127.0.0.1", p) for n, p in SERVICIOS}
    lan_ok = {n: (tcp(ip_lan, p) if ip_lan else False) for n, p in SERVICIOS}
    solo = {
        n: bool(lis[n]) and "127.0.0.1" in lis[n] and "0.0.0.0" not in lis[n]
        for n, _p in SERVICIOS
    }
    destinos = []
    if es_wsl():
        destinos.append(("127.0.0.1", "wsl-localhost"))
        destinos.extend((ip, "wsl-host") for ip in extra)
        destinos.extend((ip, "windows-host") for ip in win_ips)
    else:
        destinos.append(("127.0.0.1", "localhost"))
        destinos.extend((ip, "pasarela") for ip in extra if ip not in propias)
    urls, pruebas, vistos = [], [], set()
    for ip, origen in destinos:
        if ip in vistos:
            continue
        vistos.add(ip)
        for n, p in SERVICIOS:
            ruta = "/health" if n == "puente" else "/v1/models"
            if not tcp(ip, p):
                pruebas.append(item(f"prueba-{n}-{origen}-{ip}", False, f"cerrado {ip}:{p}"))
                continue
            ok, det, _c = http(f"http://{ip}:{p}{ruta}")
            chat = f"http://{ip}:{p}/v1/chat/completions"
            pruebas.append(item(f"prueba-{n}-{origen}-{ip}", ok, det, chat if ok else ""))
            if ok and (es_wsl() or (ip not in propias and ip != "127.0.0.1")):
                urls.append(chat)
    return {
        "wsl": es_wsl(),
        "ip_lan": ip_lan,
        "listen": lis,
        "local": local,
        "lan_ok": lan_ok,
        "solo_loop": solo,
        "perfil": perfil_windows(),
        "puente_sesion": _puente_sesion(),
        "ips_windows": win_ips,
        "pasarela": extra,
        "urls": urls,
        "pruebas": pruebas,
        "probadas": [f"{o}:{i}" for i, o in destinos],
    }


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