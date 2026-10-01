"""Llamadas de la cascada mos2ai. Jan de red antes que GPT4All."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URLS = {
    "google": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    "grok": "https://api.x.ai/v1/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
}


def _cuota(code: int, body: str) -> bool:
    texto = (body or "").lower()
    if code in (429, 402):
        return True
    marcas = ("resource_exhausted", "quota", "rate_limit", "insufficient_quota", "billing")
    return any(m in texto for m in marcas)


def _inexistente(code: int, body: str) -> bool:
    texto = (body or "").lower()
    if code == 404 and "model" in texto:
        return True
    return any(m in texto for m in ("model_not_found", "no such model", "does not exist"))


def _leer(req: Request, pid: str) -> tuple[bool, str, bool, bool]:
    try:
        with urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            code = getattr(resp, "status", 200)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return False, f"{pid} HTTP {exc.code}: {body[:180]}", _cuota(exc.code, body), _inexistente(exc.code, body)
    except URLError as exc:
        return False, f"{pid} no alcanzable: {exc.reason}", True, False
    except Exception as exc:
        return False, f"{pid}: {exc}", True, False
    return _texto(pid, raw, code)


def _texto(pid: str, raw: str, code: int) -> tuple[bool, str, bool, bool]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return False, f"{pid} respuesta no json", _cuota(code, raw), False
    if pid == "google":
        cands = data.get("candidates") or []
        parts = ((cands[0].get("content") or {}).get("parts") if cands else []) or []
        texto = parts[0].get("text") if parts else ""
        if texto:
            return True, texto, False, False
        return False, f"google sin texto: {raw[:180]}", _cuota(code, raw), _inexistente(code, raw)
    choices = data.get("choices") or []
    if choices:
        return True, choices[0]["message"]["content"], False, False
    return False, f"{pid} sin choices: {raw[:180]}", _cuota(code, raw), _inexistente(code, raw)


def _openai(pid: str, prompt: str, key: str, model: str, url: str) -> tuple[bool, str, bool, bool]:
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode()
    headers = {"Content-Type": "application/json"}
    if key and key != "local":
        headers["Authorization"] = "Bearer " + key
    req = Request(url, data=body, method="POST", headers=headers)
    return _leer(req, pid)


def _local(pid: str) -> str:
    from moslib.core.ia_router_detect import resolver_gpt4all_url, resolver_jan_url
    from moslib.core.ia_router_policy import load_policy

    policy = load_policy()
    if pid == "jan":
        return resolver_jan_url(policy)[0]
    return resolver_gpt4all_url(policy)[0]


def intentar(pid: str, prompt: str, key: str, model: str) -> tuple[bool, str, bool, bool]:
    if pid == "google":
        url = URLS["google"].format(model=model) + "?key=" + key
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
        req = Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
        return _leer(req, pid)
    if pid in URLS:
        return _openai(pid, prompt, key, model, URLS[pid])
    return _openai(pid, prompt, key, model, _local(pid))
