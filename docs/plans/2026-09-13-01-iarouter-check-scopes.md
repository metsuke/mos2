# Plan: iarouter check por ámbitos (grok, jan, twitter)

**Fecha:** 2026-09-13  
**NN del día:** 01  
**Slug:** iarouter-check-scopes  
**Estado:** En curso  
**Baseline de partida:** v0.2.7 / trabajo hacia 0.2.8 (iarouter ya en árbol)  
**Documentos relacionados:** docs/specs/10-IA-ROUTER.md, docs/man/iarouter.md, docs/AI_ONBOARDING.md, docs/VERSIONING.md, docs/STYLE_GUIDE.md, docs/specs/04-SEC-Security-Policy.md, AGENTS.md

---

## Propósito

Ampliar `iarouter check` para que acepte ámbitos por fuente de IA y un escenario concreto del cliente Grok dentro de X (Twitter), sin romper el check de compartición LAN ya existente.

El humano sustituye ficheros a mano o aplica el PR. La IA entrega ficheros enteros o el parche de la rama.

---

## Alcance

| Incluye | No incluye |
|---------|------------|
| Subcomandos de check por proveedor | Cambiar transporte de complete() |
| `iarouter check` = todos los ámbitos | Cliente web de X ni Service Workers |
| `iarouter check grok` | Nuevos proveedores |
| `iarouter check jan` / `gpt4all` / `openrouter` / `share` | DepManager / geo |
| `iarouter check grok twitter` (diagnóstico + acciones manuales) | Autocommit o apagar tests |
| Actualizar help del comando y man | Bump de versión sin criterio VERSIONING |
| Mantener solo stdlib + moslib | Volcar claves o `.mos` |

---

## Criterios de aceptación

1. `iarouter check` sin argumentos ejecuta el conjunto de diagnósticos (share + proveedores).
2. `iarouter check jan|gpt4all|grok|openrouter|share` limita el alcance.
3. `iarouter check grok twitter` (o `x`) distingue API xAI de paths internos `/i/api/1.1/*` del cliente X y lista acciones que MOS2 no puede aplicar por código.
4. Flag `detalle` / `-v` / `verbose` amplía salida; en grok puede incluir ping de chat solo si hay clave y se pidió detalle.
5. Imports de comandos: solo stdlib + moslib (SEC).
6. help() y man reflejan los nuevos usos.
7. No se desactivan tests ni A11Y.
8. El check de compartición LAN previo sigue siendo invocable (`share` o equivalente).

---

## Orden de pasos

| Paso | Fichero | Acción |
|------|---------|--------|
| 1 | docs/plans/2026-09-13-01-iarouter-check-scopes.md | Este plan |
| 2 | moslib/core/ia_check.py | Scopes + grok + grok twitter |
| 3 | moslib/commands/iarouter.py | Parser de check y help/uso |
| 4 | docs/man/iarouter.md | Sección check y sinopsis |
| 5 | Cierre | Validación humana + INTERACTION_REVIEW si cierra grupo |

---

## Notas técnicas (no son código)

- Paths `/i/api/1.1/flow/timeline.json` y `/i/api/1.1/graphql/viewer_context.json` son del front de X, no de `api.x.ai`.
- 404/410 en esos paths sin sesión de navegador son esperables; fallo de red (sin HTTP) apunta a proxy/antivirus/TLS en la máquina.
- `iarouter check grok twitter` orienta al humano en Windows cuando Mac funciona; no “arregla” el JS de X.

---

## Riesgos

| Riesgo | Mitigación |
|--------|------------|
| Romper check LAN existente | Conservar scope `share` y comportamiento legado |
| Gastar tokens en check | Ping chat solo con `detalle` y clave presente |
| Filtrar secretos | Nunca imprimir valores de clave |
| Incumplir SEC | Sin HTTP directo en el comando; stdlib en ia_check |

---

## Autoridad

Plan de campaña. Implementación en la rama `feature/iarouter-check-scopes`.
