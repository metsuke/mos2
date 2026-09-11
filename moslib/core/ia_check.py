"""
moslib.core.ia_check
Batería ampliable + conclusión y acción recomendada.
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
        if m and m.group(1) not in ("localhost",):
            out.append((m.group(1), f"politica-{campo}"))
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
        m = re.search(r"https?://([^/:]+)", val) or re.match(
            r"^(\d{1,3}(?:\.\d{1,3}){3})$", val
        )
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

SERVICIOS = [
    {"id": "jan", "puerto": JAN, "rutas": ("/v1/models", "/v1", "/v1/chat/completions")},
    {"id": "gpt4all", "puerto": GPT4ALL, "rutas": ("/v1/models", "/v1", "/v1/chat/completions")},
    {"id": "puente", "puerto": PUENTE, "rutas": ("/health", "/v1/models", "/v1/chat/completions")},
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
            if (ip, origen) in vistos:
                continue
            vistos.add((ip, origen))
            out.append((ip, origen))
    return out


def _sintesis(crudos: list[dict], wsl: bool) -> list[dict]:
    ok_local_jan = any(
        d.get("ok") and str(d.get("id", "")).startswith("jan-localhost") for d in crudos
    )
    ok_local_puente = any(
        d.get("ok") and str(d.get("id", "")).startswith("puente-localhost") for d in crudos
    )
    urls = [d["url"] for d in crudos if d.get("ok") and d.get("url")]
    urls_remotas = [u for u in urls if "127.0.0.1" not in u]
    ok_win_desde_wsl = any(
        d.get("ok") and "ipconfig-windows" in str(d.get("id", "")) for d in crudos
    )
    hay_ips_win = any("ipconfig-windows" in str(d.get("id", "")) for d in crudos)

    if urls_remotas:
        return [
            _item(
                "conclusion",
                True,
                "Hay un destino usable fuera de localhost: " + urls_remotas[0],
                urls_remotas[0],
            ),
            _item(
                "accion",
                True,
                "Acepta guardar la URL si lo pregunta. Luego: iarouter usar jan   y   iarouter preguntar hola",
                urls_remotas[0],
            ),
        ]
    if ok_local_jan or ok_local_puente:
        return [
            _item(
                "conclusion",
                True,
                "Jan o el puente responden en esta máquina (localhost) y no en las otras IPs.",
            ),
            _item(
                "accion",
                False,
                "En la instancia que comparte: iarouter puente on   y   iarouter publicar. "
                "En Windows la red debe ser perfil Privado. Luego en esta instancia otra vez: iarouter check",
            ),
        ]
    if wsl and hay_ips_win and not ok_win_desde_wsl:
        return [
            _item(
                "conclusion",
                False,
                "Estás en WSL. Se vieron IPs de Windows y ninguna acepta 1337/4891/17337.",
            ),
            _item(
                "accion",
                False,
                "En Git Bash de Windows (deja la sesión abierta): iarouter puente on. "
                "Luego iarouter publicar (UAC). Red Privada. Vuelve aquí y: iarouter check",
            ),
        ]
    return [
        _item(
            "conclusion",
            False,
            "Esta instancia no alcanza ningún Jan, GPT4All ni puente.",
        ),
        _item(
            "accion",
            False,
            "Arranca Jan o GPT4All, o en la máquina que debe compartir: iarouter puente on. "
            "Después: iarouter check",
        ),
    ]


def check() -> list[dict]:
    wsl = Path("/mnt/c/Windows").is_dir()
    crudos: list[dict] = []
    destinos = _destinos()

    for ip, origen in destinos:
        if ip == "0.0.0.0" or str(origen).startswith("error-"):
            crudos.append(_item(f"origen-{origen}", False, str(ip)))
            continue
        for svc in SERVICIOS:
            ident = f"{svc['id']}-{origen}-{ip}-{svc['puerto']}"
            if not _tcp(ip, svc["puerto"]):
                crudos.append(_item(ident, False, f"TCP cerrado {ip}:{svc['puerto']}"))
                continue
            ok_http = False
            detalle = ""
            for ruta in svc["rutas"]:
                ok, mot = _http(f"http://{ip}:{svc['puerto']}{ruta}")
                if ok:
                    ok_http = True
                    detalle = mot
                    break
                detalle = mot
            chat = f"http://{ip}:{svc['puerto']}/v1/chat/completions"
            crudos.append(_item(ident, ok_http, detalle, chat if ok_http else ""))

    sintesis = _sintesis(crudos, wsl)
    cabecera = [
        _item("ctx-plataforma", True, f"sys.platform={sys.platform}"),
        _item("ctx-wsl", wsl, "WSL" if wsl else "no WSL"),
    ]
    return sintesis + cabecera + crudos