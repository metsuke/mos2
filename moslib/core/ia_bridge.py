"""Proxy LAN -> Jan/GPT4All en localhost. Nunca reenvía al 17337."""

from __future__ import annotations

import socket
import threading
from http.server import ThreadingHTTPServer
from urllib.parse import urlparse

from moslib.core.ia_bridge_http import Handler

PUERTO = 17337
JAN_LOCAL = "http://127.0.0.1:1337/v1"
GPT4ALL_LOCAL = "http://127.0.0.1:4891/v1"
_server = None
_thread = None
_Handler = Handler


def _tcp(host: str, port: int) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        ok = s.connect_ex((host, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def _ips_propias() -> set[str]:
    out = {"127.0.0.1", "0.0.0.0", "localhost"}
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        out.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return out


def _es_bucle(url: str) -> bool:
    try:
        u = urlparse(url)
        host = (u.hostname or "").lower()
        port = u.port or (443 if u.scheme == "https" else 80)
    except Exception:
        return False
    if port == PUERTO:
        return True
    return host in _ips_propias() and port == PUERTO


def _backend() -> str:
    if _tcp("127.0.0.1", 1337):
        return JAN_LOCAL
    if _tcp("127.0.0.1", 4891):
        return GPT4ALL_LOCAL
    return JAN_LOCAL


def estado() -> dict:
    vivo = _server is not None
    ips = [ip for ip in _ips_propias() if ip not in {"127.0.0.1", "0.0.0.0", "localhost"}]
    return {
        "activo": vivo,
        "puerto": PUERTO,
        "urls": [f"http://{ip}:{PUERTO}/v1/chat/completions" for ip in ips],
        "destino": _backend(),
    }


def arrancar() -> tuple[bool, str]:
    global _server, _thread
    if _server is not None:
        return True, "El puente ya estaba activo."
    try:
        _server = ThreadingHTTPServer(("0.0.0.0", PUERTO), Handler)
    except OSError as exc:
        _server = None
        return False, f"No se pudo abrir {PUERTO}: {exc}"
    _thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _thread.start()
    st = estado()
    urls = " ".join(st["urls"]) or f"http://127.0.0.1:{PUERTO}/v1"
    return True, f"Puente activo hacia {_backend()}. Otro MetsuOS: {urls}"


def parar() -> tuple[bool, str]:
    global _server, _thread
    if _server is None:
        return True, "El puente ya estaba parado."
    _server.shutdown()
    _server.server_close()
    _server = None
    _thread = None
    return True, "Puente parado."
