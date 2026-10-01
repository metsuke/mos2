"""Cascada de cuota: google, luego grok, luego openai."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ORDEN = ("google", "grok", "openai")

URLS = {
    "google": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    "grok": "https://api.x.ai/v1/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
}
MODELOS = {"google": "gemini-2.0-flash", "grok": "grok-3", "openai": "gpt-4o-mini"}
ENV = {"google": "GEMINI_API_KEY", "grok": "XAI_API_KEY", "openai": "OPENAI_API_KEY"}


def _clave(pid: str) -> str | None:
    from moslib.core import ia_keys

    ia_keys.ingest_env()
    return ia_keys.resolve_key(pid)


def _cuota(code: int, body: str) -> bool:
    texto = (body or "").lower()
    if code in (429, 402):
        return True
    marcas = ("resource_exhausted", "quota", "rate_limit", "insufficient_quota", "billing")
    return any(m in texto for m in marcas)


def _google(prompt: str, key: str, model: str) -> tuple[bool, str, bool]:
    url = URLS["google"].format(model=model) + "?key=" + key
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
    return _leer(req, "google")


def _openai_like(pid: str, prompt: str, key: str, model: str) -> tuple[bool, str, bool]:
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode()
    req = Request(
        URLS[pid],
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
    )
    return _leer(req, pid)


def _leer(req: Request, pid: str) -> tuple[bool, str, bool]:
    try:
        with urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            code = getattr(resp, "status", 200)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return False, f"{pid} HTTP {exc.code}: {body[:240]}", _cuota(exc.code, body)
    except URLError as exc:
        return False, f"{pid} no alcanzable: {exc.reason}", False
    except Exception as exc:
        return False, f"{pid}: {exc}", False
    return _texto(pid, raw, code)


def _texto(pid: str, raw: str, code: int) -> tuple[bool, str, bool]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return False, f"{pid} respuesta no json", _cuota(code, raw)
    if pid == "google":
        cands = data.get("candidates") or []
        parts = ((cands[0].get("content") or {}).get("parts") if cands else []) or []
        texto = parts[0].get("text") if parts else ""
        if texto:
            return True, texto, False
        return False, f"google sin texto: {raw[:240]}", _cuota(code, raw)
    choices = data.get("choices") or []
    if choices:
        return True, choices[0]["message"]["content"], False
    return False, f"{pid} sin choices: {raw[:240]}", _cuota(code, raw)


def complete(prompt: str) -> tuple[bool, str, str]:
    fallos = []
    for pid in ORDEN:
        key = _clave(pid)
        if not key:
            fallos.append(f"{pid}: sin clave ({ENV[pid]})")
            continue
        if pid == "google":
            ok, msg, cuota = _google(prompt, key, MODELOS[pid])
        else:
            ok, msg, cuota = _openai_like(pid, prompt, key, MODELOS[pid])
        if ok:
            return True, msg, pid
        fallos.append(msg)
        if not cuota:
            return False, msg, pid
    return False, "cuota agotada en la cascada: " + " | ".join(fallos), ""
