"""Primitivas de red para ia_check. Sin I/O de negocio."""

from __future__ import annotations

import socket
import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

JAN = 1337
GPT4ALL = 4891
PUENTE = 17337
SERVICIOS = (("jan", JAN), ("gpt4all", GPT4ALL), ("puente", PUENTE))
SCOPES = ("all", "share", "jan", "gpt4all", "grok", "openrouter")


def item(ident: str, ok: bool, motivo: str, url: str = "", accion: str = "") -> dict:
    d = {"id": ident, "ok": ok, "motivo": motivo, "url": url}
    if accion:
        d["accion"] = accion
    return d


def tcp(ip: str, port: int, timeout: float = 0.8) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((ip, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def http(url: str, headers: dict | None = None, timeout: float = 5.0):
    req = Request(url, method="GET", headers=headers or {})
    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read(120).decode("utf-8", errors="replace")
            return True, f"HTTP {resp.status} {body[:60]}", int(resp.status)
    except HTTPError as exc:
        if exc.code in (400, 401, 403, 404, 405, 410, 422):
            return True, f"HTTP {exc.code}", int(exc.code)
        return False, f"HTTP {exc.code}", int(exc.code)
    except URLError as exc:
        return False, str(exc.reason if hasattr(exc, "reason") else exc), -1
    except Exception as exc:
        return False, str(exc), -1


def dns(host: str) -> tuple[bool, str]:
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        ips = sorted({i[4][0] for i in infos if i[4]})
        return True, ", ".join(ips[:4]) or "ok"
    except Exception as exc:
        return False, str(exc)


def tls_handshake(host: str, port: int = 443) -> tuple[bool, str]:
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                subj = dict(x[0] for x in cert.get("subject", ()))
                return True, f"TLS OK CN={subj.get('commonName', '?')}"
    except Exception as exc:
        return False, str(exc)


def es_privada(ip: str) -> bool:
    try:
        p = [int(x) for x in ip.split(".")]
    except ValueError:
        return False
    return p[0] == 10 or (p[0] == 192 and p[1] == 168) or (
        p[0] == 172 and 16 <= p[1] <= 31
    )


def es_wsl() -> bool:
    if Path("/mnt/c/Windows").is_dir():
        return True
    proc = Path("/proc/version")
    if not proc.is_file():
        return False
    try:
        return "microsoft" in proc.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False


def ipv4_propia() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return [ip for ip in found if not ip.startswith("127.")]