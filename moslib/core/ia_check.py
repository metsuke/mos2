"""
moslib.core.ia_check
Diagnóstico por ámbitos: share/LAN, proveedores y escenario Grok-in-X.
Solo stdlib + moslib. No imprime claves.
"""

from __future__ import annotations

import re
import socket
import ssl
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

JAN = 1337
GPT4ALL = 4891
PUENTE = 17337
SERVICIOS = (("jan", JAN), ("gpt4all", GPT4ALL), ("puente", PUENTE))

SCOPES = ("all", "share", "jan", "gpt4all", "grok", "openrouter")

XAI_HOST = "api.x.ai"
XAI_MODELS = "https://api.x.ai/v1/models"
XAI_CHAT = "https://api.x.ai/v1/chat/completions"
OPENROUTER_MODELS = "https://openrouter.ai/api/v1/models"

# Paths del cliente web de X (no de la API pública de xAI).
X_CLIENT_PATHS = (
    "/i/api/1.1/flow/timeline.json",
    "/i/api/1.1/graphql/viewer_context.json",
)
X_HOSTS = ("x.com", "api.x.com", "twitter.com")


def _item(ident: str, ok: bool, motivo: str, url: str = "", accion: str = "") -> dict:
    d = {"id": ident, "ok": ok, "motivo": motivo, "url": url}
    if accion:
        d["accion"] = accion
    return d


def _tcp(ip: str, port: int, timeout: float = 0.8) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ok = s.connect_ex((ip, port)) == 0
        s.close()
        return ok
    except Exception:
        return False


def _http(url: str, headers: dict | None = None, timeout: float = 5.0) -> tuple[bool, str, int]:
    """Devuelve (alcanzable, detalle, codigo_http o -1)."""
    req = Request(url, method="GET", headers=headers or {})
    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read(120).decode("utf-8", errors="replace")
            return True, f"HTTP {resp.status} {body[:60]}", int(resp.status)
    except HTTPError as exc:
        # 4xx con cuerpo es red/TLS OK (auth o ruta esperable sin sesión).
        if exc.code in (400, 401, 403, 404, 405, 410, 422):
            return True, f"HTTP {exc.code}", int(exc.code)
        return False, f"HTTP {exc.code}", int(exc.code)
    except URLError as exc:
        return False, str(exc.reason if hasattr(exc, "reason") else exc), -1
    except Exception as exc:
        return False, str(exc), -1


def _dns(host: str) -> tuple[bool, str]:
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        ips = sorted({i[4][0] for i in infos if i[4]})
        return True, ", ".join(ips[:4]) or "ok"
    except Exception as exc:
        return False, str(exc)


def _tls_handshake(host: str, port: int = 443) -> tuple[bool, str]:
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                subj = dict(x[0] for x in cert.get("subject", ()) )
                cn = subj.get("commonName", "?")
                return True, f"TLS OK CN={cn}"
    except Exception as exc:
        return False, str(exc)


def _es_privada(ip: str) -> bool:
    try:
        p = [int(x) for x in ip.split(".")]
    except ValueError:
        return False
    return (
        p[0] == 10
        or (p[0] == 192 and p[1] == 168)
        or (p[0] == 172 and 16 <= p[1] <= 31)
    )


def _es_wsl() -> bool:
    if Path("/mnt/c/Windows").is_dir():
        return True
    proc = Path("/proc/version")
    if not proc.is_file():
        return False
    try:
        return "microsoft" in proc.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False


def _ipv4_propia() -> list[str]:
    found = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        found.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return [ip for ip in found if not ip.startswith("127.")]


def _ips_de_texto(texto: str) -> list[str]:
    ips = []
    for m in re.finditer(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", texto or ""):
        ip = m.group(1)
        if _es_privada(ip) and not ip.endswith(".0") and not ip.endswith(".255"):
            if ip not in ips:
                ips.append(ip)
    return ips


def _ips_windows() -> list[str]:
    cmds = []
    for exe in (
        Path("/mnt/c/Windows/System32/ipconfig.exe"),
        Path("/mnt/c/WINDOWS/System32/ipconfig.exe"),
        Path("/mnt/c/Windows/System32/cmd.exe"),
        Path("/mnt/c/WINDOWS/System32/cmd.exe"),
    ):
        if not exe.is_file():
            continue
        if exe.name.lower() == "cmd.exe":
            cmds.append([str(exe), "/c", "ipconfig"])
        else:
            cmds.append([str(exe)])
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        except Exception:
            continue
        ips = _ips_de_texto((r.stdout or "") + (r.stderr or ""))
        if ips:
            return ips
    return []


def _pasarela() -> list[str]:
    found = []
    try:
        r = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=5)
        for m in re.finditer(r"default via (\d{1,3}(?:\.\d{1,3}){3})", r.stdout or ""):
            ip = m.group(1)
            if ip not in found:
                found.append(ip)
    except Exception:
        pass
    resolv = Path("/etc/resolv.conf")
    if resolv.is_file():
        try:
            for line in resolv.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("nameserver"):
                    ip = line.split()[1]
                    if ip and not ip.startswith("127.") and ip not in found:
                        found.append(ip)
        except OSError:
            pass
    return found


def _listen(puerto: int) -> str:
    try:
        r = subprocess.run(["netstat", "-an"], capture_output=True, text=True, timeout=8)
        texto = (r.stdout or "") + (r.stderr or "")
    except Exception:
        return ""
    lineas = [
        ln
        for ln in texto.splitlines()
        if str(puerto) in ln and ("LISTEN" in ln.upper() or "LISTENING" in ln.upper())
    ]
    return " | ".join(ln.strip() for ln in lineas[:3])


def _perfil_windows() -> str:
    if not sys.platform.startswith("win"):
        return ""
    try:
        r = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-NetConnectionProfile | Select-Object -ExpandProperty NetworkCategory",
            ],
            capture_output=True,
            text=True,
            timeout=8,
        )
        return (r.stdout or "").strip()
    except Exception:
        return ""


def _proxy_env() -> str:
    keys = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY")
    found = []
    import os

    for k in keys:
        v = os.environ.get(k)
        if v:
            found.append(f"{k}=***")
    return ", ".join(found) if found else ""


def _puente_sesion() -> bool:
    try:
        from moslib.core import ia_bridge

        return bool(ia_bridge.estado().get("activo"))
    except Exception:
        return False


def _tiene_clave(pid: str) -> bool:
    try:
        from moslib.core import ia_keys

        return bool(ia_keys.has_any_key(pid))
    except Exception:
        return False


def _hechos_share() -> dict:
    lan = _ipv4_propia()
    win_ips = _ips_windows()
    extra = _pasarela()
    propias_lan = set(lan)
    ip_lan = lan[0] if lan else None
    listen = {n: _listen(p) for n, p in SERVICIOS}
    local = {n: _tcp("127.0.0.1", p) for n, p in SERVICIOS}
    lan_ok = {n: (_tcp(ip_lan, p) if ip_lan else False) for n, p in SERVICIOS}
    solo_loop = {
        n: bool(listen[n]) and "127.0.0.1" in listen[n] and "0.0.0.0" not in listen[n]
        for n, _p in SERVICIOS
    }
    urls = []
    pruebas = []
    destinos = []
    if _es_wsl():
        destinos.append(("127.0.0.1", "wsl-localhost"))
        for ip in extra:
            destinos.append((ip, "wsl-host"))
        for ip in win_ips:
            destinos.append((ip, "windows-host"))
    else:
        destinos.append(("127.0.0.1", "localhost"))
        for ip in extra:
            if ip not in propias_lan:
                destinos.append((ip, "pasarela"))
    vistos = set()
    for ip, origen in destinos:
        if ip in vistos:
            continue
        vistos.add(ip)
        for n, p in SERVICIOS:
            ruta = "/health" if n == "puente" else "/v1/models"
            if not _tcp(ip, p):
                pruebas.append(_item(f"prueba-{n}-{origen}-{ip}", False, f"cerrado {ip}:{p}"))
                continue
            ok, det, _code = _http(f"http://{ip}:{p}{ruta}")
            chat = f"http://{ip}:{p}/v1/chat/completions"
            pruebas.append(_item(f"prueba-{n}-{origen}-{ip}", ok, det, chat if ok else ""))
            if not ok:
                continue
            if _es_wsl():
                urls.append(chat)
            elif ip not in propias_lan and ip != "127.0.0.1":
                urls.append(chat)
    return {
        "wsl": _es_wsl(),
        "ip_lan": ip_lan,
        "listen": listen,
        "local": local,
        "lan_ok": lan_ok,
        "solo_loop": solo_loop,
        "perfil": _perfil_windows(),
        "puente_sesion": _puente_sesion(),
        "ips_windows": win_ips,
        "pasarela": extra,
        "urls": urls,
        "pruebas": pruebas,
        "probadas": [f"{o}:{i}" for i, o in destinos],
    }


def _decidir_share(h: dict) -> tuple[str, str, str]:
    urls = h["urls"]
    if urls:
        return (
            "Esta instancia ya ve una compartición usable.",
            "Cuando pregunte si guardar la URL, responde s. "
            "Después: iarouter usar jan   y   iarouter preguntar hola",
            urls[0],
        )

    if (not h["wsl"]) and (h["local"]["jan"] or h["local"]["gpt4all"] or h["local"]["puente"]):
        if h["perfil"] and "Public" in h["perfil"]:
            return (
                "Hay servidor local, pero esta red Windows está en perfil Público.",
                "Pon la red en Privada. Luego: iarouter publicar. En WSL o Mac: iarouter check.",
                "",
            )
        if not h["puente_sesion"]:
            return (
                "Hay Jan en localhost y no hay puente en esta sesión.",
                "iarouter puente on    Luego: iarouter publicar    En WSL/Mac: iarouter check",
                "",
            )
        return (
            "Hay servicio local. Esta instancia usa 127.0.0.1.",
            "Deja este MOSh abierto. En Mac/WSL: iarouter check",
            "",
        )

    if h["wsl"]:
        vistos = ", ".join(h.get("probadas") or []) or "ninguna"
        return (
            "Estás en WSL y no se alcanza Jan ni el puente de Windows. "
            f"IPs sondeadas: {vistos}.",
            "En Git Bash: puente on y publicar, MOSh abierto. "
            "Si Mac ya funciona, la LAN está bien; WSL2 no usa esa ruta. "
            "Acepta 127.0.0.1 si este check lo ofrece.",
            "",
        )
    return (
        "Aquí no hay servidor local ni se ve ninguno ajeno.",
        "En el win que comparte: iarouter puente on, publicar. Aquí: iarouter check.",
        "",
    )


def _check_share(detalle: bool) -> list[dict]:
    h = _hechos_share()
    conclusion, accion, url = _decidir_share(h)
    out = [
        _item("conclusion", bool(url), conclusion, url),
        _item("accion", True, accion, url),
    ]
    if not detalle:
        return out
    out.append(
        _item(
            "detalle-entorno",
            h["wsl"],
            f"wsl={h['wsl']} ip_lan={h['ip_lan']} win={h['ips_windows']} pasarela={h['pasarela']}",
        )
    )
    out.append(_item("detalle-puente-sesion", h["puente_sesion"], "puente en ESTE MOSh"))
    for n, p in SERVICIOS:
        out.append(
            _item(
                f"detalle-listen-{n}",
                h["local"][n],
                f"local={h['local'][n]} lan={h['lan_ok'][n]} loop_only={h['solo_loop'][n]} "
                f"listen={h['listen'][n] or 'nadie'} puerto={p}",
            )
        )
    out.extend(h["pruebas"])
    return out


def _check_local_provider(nombre: str, puerto: int, detalle: bool) -> list[dict]:
    out = []
    local = _tcp("127.0.0.1", puerto)
    out.append(
        _item(
            f"{nombre}-localhost",
            local,
            f"127.0.0.1:{puerto} {'abierto' if local else 'cerrado'}",
        )
    )
    if local:
        ruta = "/v1/models"
        ok, det, _c = _http(f"http://127.0.0.1:{puerto}{ruta}")
        out.append(
            _item(
                f"{nombre}-http",
                ok,
                det,
                f"http://127.0.0.1:{puerto}/v1/chat/completions" if ok else "",
            )
        )
    else:
        out.append(
            _item(
                f"{nombre}-accion",
                False,
                f"Arranca {nombre} en este host o usa share/puente.",
                accion=f"Si está en otro PC: iarouter check share",
            )
        )
    if detalle:
        listen = _listen(puerto)
        out.append(_item(f"{nombre}-listen", bool(listen), listen or "nadie escuchando"))
    return out


def _check_grok(detalle: bool) -> list[dict]:
    out = []
    dns_ok, dns_det = _dns(XAI_HOST)
    out.append(_item("grok-dns", dns_ok, f"{XAI_HOST} -> {dns_det}"))

    tls_ok, tls_det = _tls_handshake(XAI_HOST)
    out.append(_item("grok-tls", tls_ok, tls_det))

    http_ok, http_det, code = _http(XAI_MODELS)
    # 401 sin clave es red OK.
    reachable = http_ok or code in (401, 403)
    out.append(_item("grok-http-models", reachable, http_det, XAI_MODELS))

    has_key = _tiene_clave("grok")
    out.append(
        _item(
            "grok-clave",
            has_key,
            "clave presente en .mos o XAI_API_KEY" if has_key else "sin clave (iarouter clave grok)",
        )
    )

    if detalle and has_key and reachable:
        try:
            from moslib.core import ia_keys

            key = ia_keys.resolve_key("grok")
            if key:
                ok2, det2, _c2 = _http(
                    XAI_MODELS,
                    headers={"Authorization": f"Bearer {key}"},
                )
                out.append(_item("grok-models-auth", ok2, det2))
        except Exception as exc:
            out.append(_item("grok-models-auth", False, str(exc)))

    if not reachable:
        out.append(
            _item(
                "grok-accion",
                False,
                "No se alcanza api.x.ai. Revisa DNS, proxy, antivirus SSL inspection.",
                accion="nslookup api.x.ai ; curl -v https://api.x.ai/v1/models",
            )
        )
    elif not has_key:
        out.append(
            _item(
                "grok-accion",
                False,
                "Red OK, falta clave.",
                accion="iarouter clave grok",
            )
        )
    else:
        out.append(_item("grok-accion", True, "API xAI alcanzable y clave presente."))
    return out


def _check_openrouter(detalle: bool) -> list[dict]:
    out = []
    host = "openrouter.ai"
    dns_ok, dns_det = _dns(host)
    out.append(_item("openrouter-dns", dns_ok, f"{host} -> {dns_det}"))
    http_ok, http_det, code = _http(OPENROUTER_MODELS)
    reachable = http_ok or code in (401, 403)
    out.append(_item("openrouter-http", reachable, http_det, OPENROUTER_MODELS))
    has_key = _tiene_clave("openrouter")
    out.append(
        _item(
            "openrouter-clave",
            has_key,
            "clave presente" if has_key else "sin clave (iarouter clave openrouter)",
        )
    )
    if not reachable:
        out.append(
            _item(
                "openrouter-accion",
                False,
                "No se alcanza openrouter.ai.",
                accion="Revisa DNS/proxy/firewall",
            )
        )
    elif not has_key:
        out.append(
            _item(
                "openrouter-accion",
                False,
                "Red OK, falta clave.",
                accion="iarouter clave openrouter",
            )
        )
    else:
        out.append(_item("openrouter-accion", True, "OpenRouter alcanzable y clave presente."))
    return out


def _check_grok_twitter(detalle: bool) -> list[dict]:
    """Escenario cliente Grok dentro de X (paths internos, no api.x.ai)."""
    out = []
    out.append(
        _item(
            "contexto",
            True,
            "Cliente Grok en X usa paths /i/api/1.1/* del front de X, "
            "no la API pública api.x.ai. 404/410 sin cookies de sesión son esperables.",
        )
    )

    # DNS de hosts de X
    for host in X_HOSTS:
        ok, det = _dns(host)
        out.append(_item(f"dns-{host}", ok, det))

    # TLS a x.com
    tls_ok, tls_det = _tls_handshake("x.com")
    out.append(_item("tls-x.com", tls_ok, tls_det))

    # Paths del cliente (sin sesión → 401/403/404/410 = red OK)
    for path in X_CLIENT_PATHS:
        url = f"https://x.com{path}"
        ok, det, code = _http(url)
        # Cualquier respuesta HTTP (incluso 4xx/410) prueba que la red llega.
        reachable = ok or code > 0
        out.append(
            _item(
                f"path-{path.split('/')[-1]}",
                reachable,
                f"{det} (sin sesión de navegador; 404/410 esperables)",
                url,
            )
        )

    # API xAI en paralelo para contrastar
    xai_ok, xai_det, xai_code = _http(XAI_MODELS)
    xai_reach = xai_ok or xai_code in (401, 403)
    out.append(_item("api-xai-contrast", xai_reach, f"api.x.ai: {xai_det}", XAI_MODELS))

    proxy = _proxy_env()
    out.append(
        _item(
            "proxy-env",
            not bool(proxy),
            proxy or "sin HTTP(S)_PROXY en entorno",
        )
    )

    perfil = _perfil_windows()
    if perfil:
        out.append(_item("windows-perfil", "Public" not in perfil, f"NetworkCategory={perfil}"))

    platform = sys.platform
    out.append(_item("plataforma", True, f"sys.platform={platform} wsl={_es_wsl()}"))

    # Acciones manuales (MOS2 no puede tocar el JS de X ni el Service Worker)
    acciones = [
        "1. En el navegador de Windows: DevTools → Application → Service Workers → Unregister para x.com",
        "2. Borrar datos del sitio x.com (cookies + cache) o ventana de incógnito",
        "3. Desactivar temporalmente antivirus con inspección SSL (HTTPS scanning)",
        "4. ipconfig /flushdns  y  netsh winsock reset  (Admin) luego reiniciar",
        "5. Comprobar que no hay proxy corporativo / VPN distinta a la del Mac",
        "6. Probar otro navegador o el cliente de escritorio de X si existe",
        "7. Si api.x.ai responde aquí y Mac también, el fallo es del front de X en este Windows",
    ]
    out.append(
        _item(
            "acciones-manuales",
            True,
            "MOS2 no puede arreglar el cliente JS de X. Sigue en orden:",
            accion=" | ".join(acciones),
        )
    )
    for i, a in enumerate(acciones, 1):
        out.append(_item(f"accion-{i}", True, a))

    if detalle:
        for host in ("api.x.com", "x.com"):
            ok, det = _tls_handshake(host)
            out.append(_item(f"tls-detalle-{host}", ok, det))

    # Conclusión orientativa
    paths_ok = all(
        (it.get("ok") for it in out if it["id"].startswith("path-"))
    )
    if xai_reach and paths_ok:
        concl = (
            "Red y TLS a X y a api.x.ai OK desde este host. "
            "Si el cliente de X sigue en 404 solo en Windows, es caché/Service Worker/antivirus o perfil de red."
        )
        out.insert(
            0,
            _item("conclusion", True, concl),
        )
    elif not xai_reach and not paths_ok:
        out.insert(
            0,
            _item(
                "conclusion",
                False,
                "No se alcanza ni api.x.ai ni x.com. Problema de red/DNS/proxy general.",
            ),
        )
    else:
        out.insert(
            0,
            _item(
                "conclusion",
                False,
                "Alcance parcial. Revisa las acciones manuales (Service Worker, antivirus SSL, DNS).",
            ),
        )
    return out


def check(
    detalle: bool = False,
    scope: str = "all",
    extra: str | None = None,
) -> list[dict]:
    """
    Diagnóstico por ámbito.

    scope: all|share|jan|gpt4all|grok|openrouter
    extra: twitter|x|cliente  (solo con scope=grok)
    """
    scope = (scope or "all").lower().strip()
    extra = (extra or "").lower().strip() or None

    if scope not in SCOPES and scope != "share":
        return [
            _item(
                "error",
                False,
                f"Ámbito desconocido: {scope}. Usa: {'|'.join(SCOPES)}",
            )
        ]

    # Escenario Grok-in-X
    if scope == "grok" and extra in ("twitter", "x", "cliente"):
        return _check_grok_twitter(detalle)

    out: list[dict] = []

    if scope in ("all", "share"):
        out.extend(_check_share(detalle))

    if scope in ("all", "jan"):
        out.extend(_check_local_provider("jan", JAN, detalle))

    if scope in ("all", "gpt4all"):
        out.extend(_check_local_provider("gpt4all", GPT4ALL, detalle))

    if scope in ("all", "grok"):
        out.extend(_check_grok(detalle))

    if scope in ("all", "openrouter"):
        out.extend(_check_openrouter(detalle))

    if not out:
        out.append(_item("vacio", False, f"Sin comprobaciones para scope={scope}"))

    return out
