"""Escenario cliente Grok dentro de X (no api.x.ai)."""

from __future__ import annotations

import sys

from moslib.core.ia_check_host import perfil_windows, proxy_env
from moslib.core.ia_check_net import dns, es_wsl, http, item, tls_handshake
from moslib.core.ia_check_prov import XAI_MODELS

X_CLIENT_PATHS = (
    "/i/api/1.1/flow/timeline.json",
    "/i/api/1.1/graphql/viewer_context.json",
)
X_HOSTS = ("x.com", "api.x.com", "twitter.com")
ACCIONES = (
    "DevTools → Service Workers → Unregister x.com",
    "Borrar datos de x.com o incógnito",
    "Quitar inspección SSL del antivirus",
    "ipconfig /flushdns y winsock reset (Admin)",
    "Comprobar proxy/VPN distinta a la del Mac",
    "Otro navegador o cliente de escritorio de X",
)


def check_grok_twitter(detalle: bool) -> list[dict]:
    out = [
        item(
            "contexto",
            True,
            "Cliente Grok en X usa /i/api/1.1/* , no api.x.ai. 404/410 sin sesión son esperables.",
        )
    ]
    for host in X_HOSTS:
        ok, det = dns(host)
        out.append(item(f"dns-{host}", ok, det))
    tls_ok, tls_det = tls_handshake("x.com")
    out.append(item("tls-x.com", tls_ok, tls_det))
    for path in X_CLIENT_PATHS:
        url = f"https://x.com{path}"
        ok, det, code = http(url)
        out.append(
            item(f"path-{path.split('/')[-1]}", ok or code > 0, f"{det} (sin sesión)", url)
        )
    xai_ok, xai_det, xai_code = http(XAI_MODELS)
    xai_reach = xai_ok or xai_code in (401, 403)
    out.append(item("api-xai-contrast", xai_reach, f"api.x.ai: {xai_det}", XAI_MODELS))
    proxy = proxy_env()
    out.append(item("proxy-env", not bool(proxy), proxy or "sin HTTP(S)_PROXY"))
    perfil = perfil_windows()
    if perfil:
        out.append(item("windows-perfil", "Public" not in perfil, f"NetworkCategory={perfil}"))
    out.append(item("plataforma", True, f"sys.platform={sys.platform} wsl={es_wsl()}"))
    out.append(item("acciones-manuales", True, "MOS2 no toca el JS de X.", accion=" | ".join(ACCIONES)))
    for i, a in enumerate(ACCIONES, 1):
        out.append(item(f"accion-{i}", True, a))
    if detalle:
        for host in ("api.x.com", "x.com"):
            ok, det = tls_handshake(host)
            out.append(item(f"tls-detalle-{host}", ok, det))
    paths_ok = all(it.get("ok") for it in out if it["id"].startswith("path-"))
    if xai_reach and paths_ok:
        concl = item("conclusion", True, "Red/TLS a X y api.x.ai OK. Si 404 solo en Windows: caché/SW/antivirus.")
    elif not xai_reach and not paths_ok:
        concl = item("conclusion", False, "No se alcanza ni api.x.ai ni x.com.")
    else:
        concl = item("conclusion", False, "Alcance parcial. Revisa acciones manuales.")
    out.insert(0, concl)
    return out