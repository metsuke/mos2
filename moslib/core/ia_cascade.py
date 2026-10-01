"""Cascada de sistema: google, grok, openai, openrouter, jan, gpt4all.

Jan en red local va antes que GPT4All (sin GPU). Un modelo que el
proveedor no tiene se saca de la lista y no se vuelve a elegir.
"""

from __future__ import annotations

ORDEN = ("google", "grok", "openai", "openrouter", "jan", "gpt4all")
ENV = {
    "google": "GEMINI_API_KEY",
    "grok": "XAI_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}
MODELOS = {
    "google": "gemini-2.0-flash",
    "grok": "grok-3",
    "openai": "gpt-4o-mini",
    "openrouter": "openrouter/auto",
    "jan": "auto",
    "gpt4all": "auto",
}
_VETADOS: dict[str, set[str]] = {pid: set() for pid in ORDEN}


def vetar(pid: str, model: str) -> None:
    if model and model != "auto":
        _VETADOS.setdefault(pid, set()).add(model)


def vetados(pid: str) -> set[str]:
    return set(_VETADOS.get(pid, ()))


def _clave(pid: str) -> str | None:
    if pid in ("jan", "gpt4all"):
        return "local"
    from moslib.core import ia_keys

    ia_keys.ingest_env()
    return ia_keys.resolve_key(pid)


def _modelo(pid: str) -> str:
    elegido = MODELOS[pid]
    if elegido in vetados(pid):
        return ""
    return elegido


def complete(prompt: str) -> tuple[bool, str, str]:
    from moslib.core.ia_cascade_net import intentar

    fallos = []
    for pid in ORDEN:
        model = _modelo(pid)
        if not model:
            fallos.append(f"{pid}: modelo vetado, no seleccionable")
            continue
        key = _clave(pid)
        if not key:
            fallos.append(f"{pid}: sin clave ({ENV.get(pid, '')})")
            continue
        ok, msg, cuota, inexistente = intentar(pid, prompt, key, model)
        if inexistente:
            vetar(pid, model)
            fallos.append(f"{pid}: {model} no existe, quitado de la lista")
            continue
        if ok:
            return True, msg, pid
        fallos.append(msg)
        if not cuota and pid not in ("jan", "gpt4all"):
            continue
    return False, "cascada agotada: " + " | ".join(fallos), ""
