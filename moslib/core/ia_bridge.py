"""
moslib.core.ia_bridge
Endpoint HTTP de este MetsuOS para la LAN.
No es P2P. Off hasta arrancar. Proxy a Jan/GPT4All locales.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from moslib.core.ia_router import DEFAULT_POLICY, load_policy

PUERTO = 17337
_server = None
_thread = None


def _destino() -> str:
    p = load_policy()
    if p.get("provider") == "gpt4all":
        return p.get("gpt4all_url") or DEFAULT_POLICY["gpt4all_url"]
    return p.get("jan_url") or DEFAULT_POLICY["jan_url"]


def _base() -> str:
    url = _destino().rstrip("/")
    if url.endswith("chat/completions"):
        return url[: -len("/chat/completions")]
    if url.endswith("/v1"):
        return url
    return url


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
            self._proxy("GET", _base() + "/models", b"")
            return
        if self.path in ("/", "/health"):
            self._send(200, json.dumps({"ok": True, "bridge": True}).encode("utf-8"))
            return
        self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        if b".mos" in raw:
            self._send(403, b'{"error":".mos no permitido"}')
            return
        if self.path.startswith("/v1/chat/completions"):
            self._proxy("POST", _base() + "/chat/completions", raw)
            return
        self._send(404, b'{"error":"not found"}')

    def _proxy(self, method: str, url: str, body: bytes):
        headers = {"Content-Type": "application/json"}
        req = Request(url, data=body if method == "POST" else None, method=method, headers=headers)
        try:
            with urlopen(req, timeout=60) as resp:
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
    ips = []
    try:
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ips.append(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return {
        "activo": vivo,
        "puerto": PUERTO,
        "urls": [f"http://{ip}:{PUERTO}/v1/chat/completions" for ip in ips],
        "destino": _destino(),
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
    return True, f"Puente activo. Otro MetsuOS puede usar: {urls}"


def parar() -> tuple[bool, str]:
    global _server, _thread
    if _server is None:
        return True, "El puente ya estaba parado."
    _server.shutdown()
    _server.server_close()
    _server = None
    _thread = None
    return True, "Puente parado."