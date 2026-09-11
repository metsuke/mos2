"""
moslib.core.ia_bridge
Proxy LAN -> Jan/GPT4All en localhost.
Nunca reenvía a la IP de esta máquina ni al puerto 17337.
"""

from __future__ import annotations

import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

PUERTO = 17337
JAN_LOCAL = "http://127.0.0.1:1337/v1"
GPT4ALL_LOCAL = "http://127.0.0.1:4891/v1"
_server = None
_thread = None


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
    """Solo localhost. Si Jan no está, GPT4All. Nunca la política LAN."""
    if _tcp("127.0.0.1", 1337):
        return JAN_LOCAL
    if _tcp("127.0.0.1", 4891):
        return GPT4ALL_LOCAL
    return JAN_LOCAL


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _send(self, code: int, body: bytes, ctype: str = "application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/v1/models"):
            self._proxy("GET", _backend() + "/models", b"")
            return
        if self.path in ("/", "/health"):
            self._send(
                200,
                json.dumps({"ok": True, "bridge": True, "backend": _backend()}).encode("utf-8"),
            )
            return
        self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        if b".mos" in raw:
            self._send(403, b'{"error":".mos no permitido"}')
            return
        if self.path.startswith("/v1/chat/completions"):
            self._proxy("POST", _backend() + "/chat/completions", raw)
            return
        self._send(404, b'{"error":"not found"}')

    def _proxy(self, method: str, url: str, body: bytes):
        if _es_bucle(url):
            self._send(508, b'{"error":"rechazado: el puente no puede llamarse a si mismo"}')
            return
        headers = {"Content-Type": "application/json"}
        req = Request(url, data=body if method == "POST" else None, method=method, headers=headers)
        try:
            with urlopen(req, timeout=120) as resp:
                data = resp.read()
                self._send(resp.status, data)
        except HTTPError as exc:
            self._send(exc.code, exc.read() or b"")
        except URLError as exc:
            self._send(502, json.dumps({"error": str(exc.reason)}).encode("utf-8"))
        except Exception as exc:
            self._send(502, json.dumps({"error": str(exc)}).encode("utf-8"))


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
        _server = ThreadingHTTPServer(("0.0.0.0", PUERTO), _Handler)
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