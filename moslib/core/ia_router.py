"""Fachada pública. Los tests parchean nombres de ESTE módulo."""

from moslib.core import ia_keys
from moslib.core.ia_router_ask import complete, complete_openai, detectar, set_provider, status
from moslib.core.ia_router_detect import (
    listar_modelos,
    modelo_activo,
    resolver_gpt4all_url,
    resolver_jan_url,
    set_modelo,
    url_chat,
)
from moslib.core.ia_router_http import listar_modelos_url
from moslib.core.ia_router_policy import (
    DEFAULT_POLICY,
    GPT4ALL_PORT,
    JAN_PORT,
    PLACEHOLDER_MODELS,
    PROVIDERS,
    PUENTE_PORT,
    load_policy,
    policy_path,
    save_policy,
    set_destino,
)

_complete_openai = complete_openai
_listar_modelos = listar_modelos_url