"""Checks jan/gpt4all/grok/openrouter."""

from __future__ import annotations

from moslib.core import ia_keys
from moslib.core.ia_check_host import listen
from moslib.core.ia_check_net import dns, http, item, tcp, tls_handshake

XAI_HOST = "api.x.ai"
XAI_MODELS = "https://api.x.ai/v1/models"
OPENROUTER_MODELS = "https://openrouter.ai/api/v1/models"


def _clave(pid: str) -> bool:
    try:
        return bool(ia_keys.has_any_key(pid))
    except Exception:
        return False


def check_local_provider(nombre: str, puerto: int, detalle: bool) -> list[dict]:
    local = tcp("127.0.0.1", puerto)
    out = [
        item(
            f"{nombre}-localhost",
            local,
            f"127.0.0.1:{puerto} {'abierto' if local else 'cerrado'}",
        )
    ]
    if local:
        ok, det, _c = http(f"http://127.0.0.1:{puerto}/v1/models")
        chat = f"http://127.0.0.1:{puerto}/v1/chat/completions" if ok else ""
        out.append(item(f"{nombre}-http", ok, det, chat))
    else:
        out.append(
            item(
                f"{nombre}-accion",
                False,
                f"Arranca {nombre} en este host o usa share/puente.",
                accion="Si está en otro PC: iarouter check share",
            )
        )
    if detalle:
        lis = listen(puerto)
        out.append(item(f"{nombre}-listen", bool(lis), lis or "nadie escuchando"))
    return out


def check_grok(detalle: bool) -> list[dict]:
    out = []
    dns_ok, dns_det = dns(XAI_HOST)
    out.append(item("grok-dns", dns_ok, f"{XAI_HOST} -> {dns_det}"))
    tls_ok, tls_det = tls_handshake(XAI_HOST)
    out.append(item("grok-tls", tls_ok, tls_det))
    http_ok, http_det, code = http(XAI_MODELS)
    reachable = http_ok or code in (401, 403)
    out.append(item("grok-http-models", reachable, http_det, XAI_MODELS))
    has_key = _clave("grok")
    out.append(
        item(
            "grok-clave",
            has_key,
            "clave presente" if has_key else "sin clave (iarouter clave grok)",
        )
    )
    if detalle and has_key and reachable:
        try:
            key = ia_keys.resolve_key("grok")
            if key:
                ok2, det2, _c2 = http(XAI_MODELS, headers={"Authorization": f"Bearer {key}"})
                out.append(item("grok-models-auth", ok2, det2))
        except Exception as exc:
            out.append(item("grok-models-auth", False, str(exc)))
    if not reachable:
        out.append(item("grok-accion", False, "No se alcanza api.x.ai.", accion="nslookup api.x.ai"))
    elif not has_key:
        out.append(item("grok-accion", False, "Red OK, falta clave.", accion="iarouter clave grok"))
    else:
        out.append(item("grok-accion", True, "API xAI alcanzable y clave presente."))
    return out


def check_openrouter(detalle: bool) -> list[dict]:
    host = "openrouter.ai"
    dns_ok, dns_det = dns(host)
    http_ok, http_det, code = http(OPENROUTER_MODELS)
    reachable = http_ok or code in (401, 403)
    has_key = _clave("openrouter")
    out = [
        item("openrouter-dns", dns_ok, f"{host} -> {dns_det}"),
        item("openrouter-http", reachable, http_det, OPENROUTER_MODELS),
        item(
            "openrouter-clave",
            has_key,
            "clave presente" if has_key else "sin clave (iarouter clave openrouter)",
        ),
    ]
    if not reachable:
        out.append(item("openrouter-accion", False, "No se alcanza openrouter.ai."))
    elif not has_key:
        out.append(item("openrouter-accion", False, "Red OK, falta clave.", accion="iarouter clave openrouter"))
    else:
        out.append(item("openrouter-accion", True, "OpenRouter alcanzable y clave presente."))
    return out