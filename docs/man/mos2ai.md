# mos2ai

Comando de sistema. La misma funcion que `mos2AI.py` en la raiz: `moslib.core.mos2ai_bucle.main`.

## Uso

    mos2ai
    python mos2AI.py

## Que hace

Puente de ingesta. Lista modelos Flash, quita de la cola los que ya no existen y no deja elegirlos. Rota si la cuota de Google se agota. Guarda historial en `rootfs/home/Metsuke/`.

Herramientas, con permiso en cada llamada: listar directorio, leer fichero, escribir fichero, crear fichero, crear directorio. Sandbox: directorio de trabajo.

Si todos los modelos Google estan bloqueados hoy: Grok, OpenAI, OpenRouter, Jan en la red local, GPT4All al final (sin GPU).

## Claves

GEMINI_API_KEY, XAI_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY, o el almacen de iarouter.
