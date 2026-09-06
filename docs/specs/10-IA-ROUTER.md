# 10 – Enrutador de IA

**Versión del documento:** 1.1  
**Estado:** Normativo (campaña 07 completa, frente C)  
**Baseline:** v0.2.6  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/04-SEC-Security-Policy.md, docs/INCENTIVOS.md, docs/A11Y.md, docs/man/iarouter.md, docs/plans/2026-09-04-02-07-completa.md

---

## Propósito

Fachada única de MetsuOS para llamar a modelos **sin** que la IA fije la política.

Proveedores de esta versión:

| Id | Tipo | Disponibilidad |
|----|------|----------------|
| jan | local | servidor HTTP en jan_url |
| gpt4all | local | servidor HTTP en gpt4all_url |
| grok | remoto | variable XAI_API_KEY |
| openrouter | remoto | variable OPENROUTER_API_KEY |

---

## Qué no es

- No es la suite de desarrollo (08).
- No es un agente que commitea solo.
- No lee `.mos` salvo allowlist explícita del humano.
- No sustituye INCENTIVOS ni A11Y/SEC.

---

## Contrato moslib.core.ia_router

| Operación | Comportamiento |
|-----------|----------------|
| status | proveedor, enabled, lista de detectados |
| detectar | jan/gpt4all por HTTP corto; grok/openrouter por env |
| set_provider(id) | solo si detectar lo marca disponible; enabled=true |
| complete(prompt, meta) | envía o error claro en español |

`meta.provider` puede forzar el id de esa llamada. Si falta, usa la política.

Errores (sin clave, sin red, off, `.mos` no autorizado): mensaje usable, sin volcar secretos, shell vivo.

---

## Política

Ruta: `.mos/config/ia_router.json` (espacio del usuario).

| Campo | Default |
|-------|---------|
| enabled | false |
| provider | jan |
| jan_url | http://127.0.0.1:1337/v1/chat/completions |
| gpt4all_url | http://127.0.0.1:4891/v1/chat/completions |
| grok_url | https://api.x.ai/v1/chat/completions |
| grok_model | grok-3 |
| openrouter_url | https://openrouter.ai/api/v1/chat/completions |
| openrouter_model | openrouter/auto |
| allow_mos_paths | [] |
| cost_ceiling | null |
| project | null |

La IA no escribe este fichero. Lo escribe `iarouter usar` o el humano.

Claves: solo entorno. Nunca git.

---

## Transporte

Solo a través de moslib. `urllib` de la stdlib. Comandos no hacen HTTP directo.

Cuerpo: chat completions (role user + content). Respuesta: `choices[0].message.content`.

---

## Comando de sistema

| Subcomando | Efecto |
|------------|--------|
| status | política + detección |
| detectar | solo detección |
| usar ID | activa proveedor disponible |
| preguntar TEXTO | complete explícito; imprime el texto |

Sin `preguntar` no hay envío.

Salida lineal, A11Y.

---

## Criterios de aceptación

1. Spec 1.1 publicado.
2. enabled=false: no hay llamada de red (test).
3. Payload con `.mos` no allowlist: rechazo.
4. detectar distingue local caído y remoto sin clave.
5. usar un id no disponible: no cambia política.
6. preguntar con Jan/GPT4All/Grok/OpenRouter implementados en la fachada.
7. Fallo de red o clave: error usable, shell vivo.

---

## Autoridad

Normativo para llamadas a modelos. Choca con SEC/A11Y → ganan esas.