"""Handler HTTP del puente LAN -> Jan/GPT4All."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _send(self, code: int, body: bytes, ctype: str = "application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        from moslib.core.ia_bridge import _backend
        if self.path.startswith("/v1/models"):
            self._proxy("GET", _backend() + "/models", b"")
            return
        if self.path in ("/", "/health"):
            self._send(200, json.dumps({"ok": True, "bridge": True, "backend": _backend()}).encode("utf-8"))
            return
        self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        from moslib.core.ia_bridge import _backend
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
        from moslib.core.ia_bridge import _es_bucle
        if _es_bucle(url):
            self._send(508, b'{"error":"rechazado: el puente no puede llamarse a si mismo"}')
            return
        headers = {"Content-Type": "application/json"}
        req = Request(url, data=body if method == "POST" else None, method=method, headers=headers)
        try:
            with urlopen(req, timeout=120) as resp:
                self._send(resp.status, resp.read())
        except HTTPError as exc:
            self._send(exc.code, exc.read() or b"")
        except URLError as exc:
            self._send(502, json.dumps({"error": str(exc.reason)}).encode("utf-8"))
        except Exception as exc:
            self._send(502, json.dumps({"error": str(exc)}).encode("utf-8"))
