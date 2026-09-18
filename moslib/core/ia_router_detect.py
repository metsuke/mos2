"""Resolución de URL, listado y modelo activo."""

from __future__ import annotations

from moslib.core.ia_router_http import probe_http
from moslib.core.ia_router_lan import (
    escanear_lan,
    hosts_extra,
    load_url_cache,
    probar_host,
    save_url_cache,
)
from moslib.core.ia_router_policy import (
    DEFAULT_POLICY,
    GPT4ALL_PORT,
    JAN_PORT,
    PROVIDERS,
    PUENTE_PORT,
    campo_modelo,
    load_policy,
    save_policy,
)


def resolver_local(url_cfg: str, cache_name: str, puertos: list[int], etiqueta: str):
    ok, motivo = probe_http(url_cfg)
    if ok:
        return url_cfg, f"local o configurada: {motivo}"
    cache = load_url_cache(cache_name)
    if cache:
        ok, motivo = probe_http(cache["url"])
        if ok:
            return cache["url"], f"cache: {motivo}"
    for ip, origen in hosts_extra():
        for port in puertos:
            url = probar_host(ip, port)
            if url:
                save_url_cache(cache_name, url, origen)
                return url, f"{origen} puerto {port}: {url}"
    hallado = escanear_lan(puertos)
    if hallado:
        url, port = hallado
        save_url_cache(cache_name, url, "lan")
        return url, f"LAN puerto {port}: {url}"
    return url_cfg, f"no hay {etiqueta} en localhost, host WSL, puente ni LAN visible"


def resolver_jan_url(policy: dict):
    return resolver_local(
        policy.get("jan_url") or DEFAULT_POLICY["jan_url"],
        "ia_jan_cache.json",
        [JAN_PORT, PUENTE_PORT],
        "Jan",
    )


def resolver_gpt4all_url(policy: dict):
    return resolver_local(
        policy.get("gpt4all_url") or DEFAULT_POLICY["gpt4all_url"],
        "ia_gpt4all_cache.json",
        [GPT4ALL_PORT],
        "GPT4All",
    )


def url_chat(provider: str, policy: dict) -> str:
    if provider == "jan":
        url, _ = resolver_jan_url(policy)
        return url
    if provider == "gpt4all":
        url, _ = resolver_gpt4all_url(policy)
        return url
    if provider == "grok":
        return policy.get("grok_url") or DEFAULT_POLICY["grok_url"]
    if provider == "openrouter":
        return policy.get("openrouter_url") or DEFAULT_POLICY["openrouter_url"]
    raise ValueError(provider)


def listar_modelos(provider: str | None = None):
    from moslib.core import ia_router as R

    p = load_policy()
    pid = (provider or p.get("provider") or "jan").lower()
    if pid not in PROVIDERS:
        return False, f"Proveedor desconocido: {pid}", []
    ids, raw = R._listar_modelos(url_chat(pid, p), pid)
    if not ids:
        return False, raw or "sin modelos", []
    return True, pid, ids


def modelo_activo(provider: str | None = None) -> str:
    p = load_policy()
    pid = (provider or p.get("provider") or "jan").lower()
    return str(p.get(campo_modelo(pid)) or "auto")


def set_modelo(model_id: str, provider: str | None = None):
    from moslib.core import ia_router as R

    pid = (provider or load_policy().get("provider") or "jan").lower()
    if pid not in PROVIDERS:
        return False, f"Proveedor desconocido: {pid}"
    mid = model_id.strip()
    if not mid:
        return False, "Indica un id de modelo."
    if mid != "auto":
        ok, msg, ids = R.listar_modelos(pid)
        if ok and ids and mid not in ids:
            return False, f"'{mid}' no está en la lista de {pid}."
        if not ok and pid in ("grok", "openrouter"):
            return False, f"No se pudo validar el modelo: {msg}"
    save_policy({campo_modelo(pid): mid})
    return True, f"Modelo de {pid}: {mid}"