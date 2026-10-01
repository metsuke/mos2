# mos2ai

Comando de sistema. No es un comando de usuario ni una app.

## Uso

    mos2ai <texto>
    mos2ai vetados

## Cascada

1. Google (Gemini), si hay cuota.
2. Grok y sus modelos, si Google agota cuota o rate limit.
3. OpenAI y sus modelos.
4. OpenRouter y sus modelos.
5. Jan en la red local, y sus modelos. Prioridad sobre GPT4All, sea o no local.
6. GPT4All y sus modelos. Ultimo: va sin GPU.

## Modelo inexistente

Si el proveedor responde que el modelo no existe, mos2ai lo quita de la lista de esa sesion y no lo vuelve a seleccionar. `mos2ai vetados` muestra esos ids.

## Claves

GEMINI_API_KEY, XAI_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY.
Jan y GPT4All no usan clave; se buscan en localhost y en la LAN.
