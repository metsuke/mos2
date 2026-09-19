"""Diagnóstico y publicación LAN de Jan/GPT4All. publicar no se llama solo."""

from __future__ import annotations

from moslib.core.ia_share_net import (
    GPT4ALL_PORT,
    JAN_PORT,
    PUENTE_PORT,
    PUERTOS,
    escucha,
    http,
    local_ipv4,
    netstat_puerto,
    perfil,
    run,
)

_perfil = perfil
_run = run
_local_ipv4 = local_ipv4
_escucha = escucha
_http = http
_netstat_puerto = netstat_puerto


def _guia(p: str, puerto: int) -> str:
    if p == "macos/native":
        return (
            f"En macOS el servidor debe escuchar en 0.0.0.0:{puerto}, no solo 127.0.0.1. "
            "Permite Jan o GPT4All en el Firewall de aplicaciones."
        )
    if p.startswith("windows"):
        return (
            f"En Windows bind 0.0.0.0:{puerto}. Regla TCP {puerto} solo perfil privado. "
            f"Plan B: iarouter puente on y TCP {PUENTE_PORT}."
        )
    return f"Bind 0.0.0.0:{puerto}. Abre TCP {puerto} hacia la LAN, no Internet."


def diagnostico() -> list[dict]:
    p = perfil()
    lan = local_ipv4()
    ip_lan = lan[0] if lan else None
    items = []
    ok_j, mot_j = escucha("127.0.0.1", JAN_PORT)
    items += [
        {"id": "jan-local", "ok": ok_j, "motivo": mot_j},
        {"id": "jan-listen", "ok": ok_j, "motivo": netstat_puerto(JAN_PORT)},
    ]
    if ip_lan:
        ok_jl, mot_jl = escucha(ip_lan, JAN_PORT)
        http_ok, http_m = http(f"http://{ip_lan}:{JAN_PORT}/v1")
        items += [
            {"id": "jan-lan", "ok": ok_jl, "motivo": mot_jl},
            {"id": "jan-http-lan", "ok": http_ok, "motivo": http_m},
        ]
    else:
        items.append({"id": "jan-lan", "ok": False, "motivo": "sin IPv4 privada"})
    ok_g, mot_g = escucha("127.0.0.1", GPT4ALL_PORT)
    items += [
        {"id": "gpt4all-local", "ok": ok_g, "motivo": mot_g},
        {"id": "gpt4all-listen", "ok": ok_g, "motivo": netstat_puerto(GPT4ALL_PORT)},
    ]
    if ip_lan:
        ok_gl, mot_gl = escucha(ip_lan, GPT4ALL_PORT)
        items.append({"id": "gpt4all-lan", "ok": ok_gl, "motivo": mot_gl})
    else:
        items.append({"id": "gpt4all-lan", "ok": False, "motivo": "sin IPv4 privada"})
    ok_p, mot_p = escucha("127.0.0.1", PUENTE_PORT)
    items += [
        {"id": "puente-local", "ok": ok_p, "motivo": mot_p + ". iarouter puente on si está parado."},
        {"id": "puente-listen", "ok": ok_p, "motivo": netstat_puerto(PUENTE_PORT)},
    ]
    if ip_lan:
        ok_pl, mot_pl = escucha(ip_lan, PUENTE_PORT)
        items.append({"id": "puente-lan", "ok": ok_pl, "motivo": mot_pl})
    items.append({"id": "perfil", "ok": True, "motivo": f"entorno {p}; IP LAN {ip_lan or 'desconocida'}"})
    if not any(i["id"] == "jan-lan" and i["ok"] for i in items):
        items.append({"id": "guia-jan", "ok": False, "motivo": _guia(p, JAN_PORT)})
    if not any(i["id"] == "gpt4all-lan" and i["ok"] for i in items):
        items.append({"id": "guia-gpt4all", "ok": False, "motivo": _guia(p, GPT4ALL_PORT)})
    return items


def publicar() -> list[dict]:
    from moslib.core.ia_share_pub import publicar as _pub
    return _pub()
