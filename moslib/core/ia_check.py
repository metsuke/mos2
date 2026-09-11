"""
moslib.core.ia_check
Batería ampliable de comprobaciones de conectividad IA.
Añadir un caso = añadir un dict a CASES o un origen a ORIGENES.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

JAN = 1337
GPT4ALL = 4891
PUENTE = 17337


def _es_privada(ip: str) -> bool:
    try:
        p = [int(x) for x in ip.split(".")]
    except ValueError:
        return False
    if p[0] == 10:
        return True
    if p[0] == 192 and p[1] == 168:
        return True
    if p[0] == 172 and 16 <= p[1] <= 31:
        return True
    return False


def _tcp(ip: str, port: int, timeout: float = 0.6) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((ip, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def _http(url: str) -> tuple[bool, str]:
    req = Request(url, method="GET")
    try:
        with urlopen(req, timeout=3) as resp:
            cuerpo = resp.read(160).decode("utf-8", errors="replace")
        return True, f"HTTP OK {url} {cuerpo[:80]}"
    except HTTPError as exc:
        if exc.code in (400, 401, 404, 405, 422):
            return True, f"HTTP {exc.code} {url}"
        return False, f"HTTP {exc.code} {url}"
    except URLError as exc:
        return False, f"no: {exc.reason} {url}"
    except Exception as exc:
        return False, f"{exc} {url}"


def _item(ident: str, ok: bool, motivo: str, url: str = "") -> dict:
    return {"id": ident, "ok": ok, "motivo": motivo, "url": url}


def origen_localhost() -> list[tuple[str, str]]:
    return [("127.0.0.1", "localhost")]


def origen_ipv4_propia() -> list[tuple[str, str]]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                found.add(ip)
    except Exception:
        pass
    return [(ip, "ipv4-propia") for ip in sorted(found)]


def origen_resolv() -> list[tuple[str, str]]:
    path = Path("/etc/resolv.conf")
    if not path.is_file():
        return []
    out = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("nameserver"):
                ip = line.split()[1]
                if ip and not ip.startswith("127."):
                    out.append((ip, "resolv"))
    except OSError:
        pass
    return out


def origen_pasarela() -> list[tuple[str, str]]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        yo = s.getsockname()[0]
        s.close()
        partes = yo.split(".")
        if len(partes) == 4:
            return [(".".join(partes[:3] + ["1"]), "pasarela-.1")]
    except Exception:
        pass
    return []


def origen_ipconfig_windows() -> list[tuple[str, str]]:
    for exe in (
        Path("/mnt/c/Windows/System32/ipconfig.exe"),
        Path("/mnt/c/WINDOWS/system32/ipconfig.exe"),
    ):
        if not exe.is_file():
            continue
        try:
            r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=8)
        except Exception:
            return []
        texto = (r.stdout or "") + (r.stderr or "")
        ips = []
        for m in re.finditer(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", texto):
            ip = m.group(1)
            if _es_privada(ip) and not ip.endswith(".255") and not ip.endswith(".0"):
                if ip not in ips:
                    ips.append(ip)
        return [(ip, "ipconfig-windows") for ip in ips]
    return []


def origen_politica() -> list[tuple[str, str]]:
    try:
        from moslib.core.ia_router import load_policy
    except Exception:
        return []
    p = load_policy()
    out = []
    for campo in ("jan_url", "gpt4all_url"):
        raw = str(p.get(campo) or "")
        m = re.search(r"https?://([^/:]+)", raw)
        if m:
            host = m.group(1)
            if host not in ("localhost",):
                out.append((host, f"politica-{campo}"))
    return out


def origen_cache() -> list[tuple[str, str]]:
    try:
        from moslib.core.user import get_user_mos_dir
    except Exception:
        return []
    out = []
    d = get_user_mos_dir() / "config"
    for nombre in ("ia_jan_cache.json", "ia_gpt4all_cache.json"):
        path = d / nombre
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        raw = str(data.get("url") or "")
        m = re.search(r"https?://([^/:]+)", raw)
        if m:
            out.append((m.group(1), f"cache-{nombre}"))
    return out


def origen_env() -> list[tuple[str, str]]:
    out = []
    for var in ("JAN_URL", "METSUOS_JAN_URL", "JAN_HOST"):
        val = os.environ.get(var)
        if not val:
            continue
        m = re.search(r"https?://([^/:]+)", val) or re.match(r"^(\d{1,3}(?:\.\d{1,3}){3})$", val)
        if m:
            out.append((m.group(1), f"env-{var}"))
    return out


ORIGENES = [
    origen_localhost,
    origen_ipv4_propia,
    origen_resolv,
    origen_pasarela,
    origen_ipconfig_windows,
    origen_politica,
    origen_cache,
    origen_env,
]


# servicio, puerto, rutas HTTP a probar, tipo de URL de chat si responde
SERVICIOS = [
    {
        "id": "jan",
        "puerto": JAN,
        "rutas": ("/v1/models", "/v1", "/v1/chat/completions"),
    },
    {
        "id": "gpt4all",
        "puerto": GPT4ALL,
        "rutas": ("/v1/models", "/v1", "/v1/chat/completions"),
    },
    {
        "id": "puente",
        "puerto": PUENTE,
        "rutas": ("/health", "/v1/models", "/v1/chat/completions"),
    },
]


def _destinos() -> list[tuple[str, str]]:
    vistos = set()
    out = []
    for fn in ORIGENES:
        try:
            pares = fn()
        except Exception as exc:
            pares = [("0.0.0.0", f"error-{fn.__name__}:{exc}")]
        for ip, origen in pares:
            clave = (ip, origen)
            if clave in vistos:
                continue
            vistos.add(clave)
            out.append((ip, origen))
    return out


def _caso_contexto() -> list[dict]:
    wsl = Path("/mnt/c/Windows").is_dir()
    items = [
        _item("ctx-plataforma", True, f"sys.platform={sys.platform}"),
        _item("ctx-wsl", wsl, "WSL con /mnt/c" if wsl else "no parece WSL"),
        _item("ctx-hostname", True, socket.gethostname()),
    ]
    try:
        from moslib.core.ia_router import load_policy

        p = load_policy()
        items.append(
            _item(
                "ctx-politica",
                True,
                f"enabled={p.get('enabled')} provider={p.get('provider')} "
                f"jan_url={p.get('jan_url')} gpt4all_url={p.get('gpt4all_url')}",
            )
        )
    except Exception as exc:
        items.append(_item("ctx-politica", False, str(exc)))
    try:
        from moslib.core import ia_bridge

        st = ia_bridge.estado()
        items.append(
            _item(
                "ctx-puente-proceso",
                bool(st.get("activo")),
                f"activo={st.get('activo')} puerto={st.get('puerto')} destino={st.get('destino')}",
            )
        )
    except Exception as exc:
        items.append(_item("ctx-puente-proceso", False, str(exc)))
    return items


def check() -> list[dict]:
    items = list(_caso_contexto())
    destinos = _destinos()
    items.append(
        _item(
            "mapa-destinos",
            bool(destinos),
            "Destinos: " + ", ".join(f"{o}={i}" for i, o in destinos)
            if destinos
            else "sin destinos",
        )
    )

    halladas: list[str] = []
    for ip, origen in destinos:
        if ip == "0.0.0.0" or origen.startswith("error-"):
            items.append(_item(f"origen-{origen}", False, ip))
            continue
        for svc in SERVICIOS:
            ident = f"{svc['id']}-{origen}-{ip}-{svc['puerto']}"
            if not _tcp(ip, svc["puerto"]):
                items.append(_item(ident, False, f"TCP cerrado {ip}:{svc['puerto']}"))
                continue
            ok_http = False
            detalle = ""
            for ruta in svc["rutas"]:
                url = f"http://{ip}:{svc['puerto']}{ruta}"
                ok, mot = _http(url)
                if ok:
                    ok_http = True
                    detalle = mot
                    break
                detalle = mot
            chat = f"http://{ip}:{svc['puerto']}/v1/chat/completions"
            items.append(_item(ident, ok_http, detalle, chat if ok_http else ""))
            if ok_http:
                halladas.append(chat)

    if halladas:
        unicas = []
        for u in halladas:
            if u not in unicas:
                unicas.append(u)
        items.append(
            _item(
                "resumen",
                True,
                "URLs utilizables: " + " ".join(unicas),
                unicas[0],
            )
        )
    else:
        items.append(
            _item(
                "resumen",
                False,
                "Ningún Jan, GPT4All ni puente respondió en los destinos conocidos.",
            )
        )
    return items 