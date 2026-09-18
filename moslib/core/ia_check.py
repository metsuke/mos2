"""Diagnóstico por ámbitos. Fachada. Solo stdlib + moslib."""

from __future__ import annotations

from moslib.core.ia_check_net import GPT4ALL, JAN, SCOPES, item
from moslib.core.ia_check_prov import (
    check_grok,
    check_local_provider,
    check_openrouter,
)
from moslib.core.ia_check_share import check_share
from moslib.core.ia_check_x import check_grok_twitter


def check(detalle: bool = False, scope: str = "all", extra: str | None = None) -> list[dict]:
    scope = (scope or "all").lower().strip()
    extra = (extra or "").lower().strip() or None
    if scope not in SCOPES:
        return [item("error", False, f"Ámbito desconocido: {scope}. Usa: {'|'.join(SCOPES)}")]
    if scope == "grok" and extra in ("twitter", "x", "cliente"):
        return check_grok_twitter(detalle)
    out: list[dict] = []
    if scope in ("all", "share"):
        out.extend(check_share(detalle))
    if scope in ("all", "jan"):
        out.extend(check_local_provider("jan", JAN, detalle))
    if scope in ("all", "gpt4all"):
        out.extend(check_local_provider("gpt4all", GPT4ALL, detalle))
    if scope in ("all", "grok"):
        out.extend(check_grok(detalle))
    if scope in ("all", "openrouter"):
        out.extend(check_openrouter(detalle))
    if not out:
        out.append(item("vacio", False, f"Sin comprobaciones para scope={scope}"))
    return out