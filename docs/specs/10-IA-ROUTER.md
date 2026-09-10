# 10 – Enrutador de IA

**Versión del documento:** 1.2  
**Estado:** Normativo (mini campaña iarouter)  
**Baseline:** v0.2.7 hacia v0.2.8  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/04-SEC-Security-Policy.md, docs/INCENTIVOS.md, docs/A11Y.md, docs/man/iarouter.md, docs/plans/2026-09-07-01-iarouter-modelos-lan.md

---

## Propósito

Fachada única de MetsuOS para llamar a modelos **sin** que la IA fije la política.

Proveedores de esta versión:

| Id | Tipo | Disponibilidad |
|----|------|----------------|
| jan | local o LAN | HTTP en jan_url, localhost, cache o /24 privada puerto 1337 |
| gpt4all | local o LAN | HTTP en gpt4all_url, localhost, cache o /24 privada puerto 4891 |
| grok | remoto | clave en .mos o XAI_API_KEY (se ingiere al almacén) |
| openrouter | remoto | clave en .mos o OPENROUTER_API_KEY (se ingiere al almacén) |

---

## Qué no es

- No es la suite de desarrollo (08).
- No es un agente que commitea solo.
- No lee `.mos` salvo allowlist explícita del humano.
- No sustituye INCENTIVOS ni A11Y/SEC.
- No es la malla P2P (campaña 10). El puente LAN es un HTTP local opcional.

---

## Contrato moslib.core.ia_router

| Operación | Comportamiento |
|-----------|----------------|
| status | proveedor, enabled, modelo, lista de detectados |
| detectar | jan/gpt4all HTTP + LAN; grok/openrouter por clave .mos o env |
| set_provider(id) | solo si detectar lo marca disponible; enabled=true |
| listar_modelos(id) | GET /v1/models del proveedor |
| set_modelo(id) | persiste jan_model / gpt4all_model / grok_model / openrouter_model |
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
| jan_model | auto |
| gpt4all_url | http://127.0.0.1:4891/v1/chat/completions |
| gpt4all_model | auto |
| grok_url | https://api.x.ai/v1/chat/completions |
| grok_model | auto |
| openrouter_url | https://openrouter.ai/api/v1/chat/completions |
| openrouter_model | auto |
| allow_mos_paths | [] |
| cost_ceiling | null |
| project | null |

La IA no escribe este fichero. Lo escribe `iarouter usar` / `iarouter modelo` o el humano.

---

## Claves

moslib.core.ia_keys + moslib.core.secreto.

Orden: almacén `.mos` → si falta, entorno → se copia al almacén.  
Ficheros: `.mos/config/.ia_wrap` y `ia_keys.json` (no git, 0600).  
HMAC detecta manipulación. Quien copie wrap+json puede recuperar.  
`iarouter clave` pide sin eco. No se listan en status.

---

## Transporte

Solo a través de moslib. `urllib` de la stdlib. Comandos no hacen HTTP directo.

Cuerpo: chat completions (role user + content). Respuesta: `choices[0].message.content`.

OpenRouter añade HTTP-Referer y X-Title.

---

## LAN, share, publicar, puente

| Pieza | Efecto |
|-------|--------|
| resolver local | localhost → cache TTL 600 s → /24 privada |
| share | diagnóstico bind/puerto; guía por entorno; no cambia el anfitrión |
| publicar | autorización explícita; regla mínima LAN/privado |
| puente | HTTP MetsuOS :17337, proxy a Jan/GPT4All; off hasta puente on; rechaza .mos |

---

## Comando de sistema

| Subcomando | Efecto |
|------------|--------|
| status | política + detección |
| detectar | solo detección |
| share | diagnóstico LAN |
| publicar | intenta abrir LAN (explícito) |
| puente on\|off\|status | endpoint 17337 |
| usar ID | activa proveedor disponible; pide clave si falta |
| clave ID [borrar] | alta / baja en .mos |
| modelos [ID] | lista ids |
| modelo [ID] texto... | fija modelo (espacios permitidos) |
| preguntar TEXTO | complete explícito |

Sin `preguntar` no hay envío.

Salida: tabla corta + párrafo por ítem.

---

## Criterios de aceptación

1. Spec 1.2 publicado.
2. enabled=false: no hay llamada de red (test).
3. Payload con `.mos` no allowlist: rechazo.
4. detectar distingue local caído y remoto sin clave.
5. usar un id no disponible: no cambia política.
6. preguntar con Jan/GPT4All/Grok/OpenRouter implementados en la fachada.
7. Fallo de red o clave: error usable, shell vivo.
8. listar/fijar modelo; id con espacios no se toma como proveedor.
9. clave en .mos no aparece en claro en ia_keys.json (test).
10. env se ingiere al almacén (test).
11. share no llama a publicar.
12. puente off por defecto.
13. **Pruebas humanas antes del tag 0.2.8:** pytest completo; en una máquina `preguntar` local; si hay segunda máquina, share o puente; Grok u OpenRouter con clave real al menos una vez.

---

## Autoridad

Normativo para llamadas a modelos. Choca con SEC/A11Y → ganan esas.