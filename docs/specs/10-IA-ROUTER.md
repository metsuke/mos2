# 10 – Enrutador de IA

**Versión del documento:** 1.0  
**Estado:** Normativo (campaña 07, frente C)  
**Baseline:** v0.2.5  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/04-SEC-Security-Policy.md, docs/INCENTIVOS.md, docs/A11Y.md, docs/plans/2026-09-01-02-campana-07-soporte-apps-tareas-ia.md

---

## Propósito

Definir la fachada de MetsuOS para llamar a modelos (Grok, OpenRouter, local, futuros) **sin** que la IA fije la política.

En la 07: **un** proveedor, API estable, off por defecto. El resto de proveedores se enchufa después sin cambiar el contrato.

---

## Qué no es

- No es la suite de desarrollo (08).
- No es un agente que commitea solo.
- No lee `.mos` salvo whitelist explícita del humano.
- No sustituye INCENTIVOS ni Asimov: quien responde sigue obligado.

---

## Contrato de la fachada (moslib)

Operaciones mínimas:

| Operación | Comportamiento 07 |
|-----------|-------------------|
| status | proveedor, on/off, motivo si off |
| complete(prompt, meta) | envía payload mínimo o error claro |
| providers | lista; en 07 un id |

`meta` puede llevar `proyecto`, `prioridad` (stubs). No hace falta implementar todos los parámetros del diseño largo.

Errores: sin clave, sin red, política off, payload que incluye ruta `.mos` no autorizada → mensaje en español, sin traza que filtre secretos. No crash del shell.

---

## Política (la guarda el sistema)

Fichero de config (ICD fijará la ruta). Campos 07:

| Campo | Default |
|-------|---------|
| enabled | false |
| provider | un id (p. ej. grok) |
| cost_ceiling | stub (número o null) |
| project | stub |
| allow_mos_paths | lista vacía |

La IA **no** persiste esta tabla. La lee moslib.

---

## Transporte

Solo a través de moslib. Comandos y apps no hacen HTTP a pelo.

07: `urllib` de la stdlib detrás de la fachada, o la misma API devolviendo “desactivado / no implementado” si aún no hay llamada real. Las dos formas deben ser intercambiables para la 08.

---

## Payload

Incluye: texto del paso, normas citadas por referencia (rutas de docs), fichero en edición si el humano lo pide.

No incluye: home anfitrión, `.mos` salvo allowlist, claves, dumps de otras apps.

---

## Comando de sistema (nombre en ICD)

Consultar status, no enviar nada por accidente. Envío = acción explícita del humano.

Salida: texto lineal, A11Y.

---

## Criterios de aceptación del frente C

1. Este spec publicado.
2. Política `enabled=false`: no hay llamada de red (test).
3. Por defecto el cuerpo no contiene `.mos`.
4. Fallo de red o de clave: error usable, shell vivo.
5. Un solo proveedor en 07; el campo `providers` admite más ids después.

---

## Autoridad

Normativo para llamadas a modelos. Choca con SEC/A11Y → ganan esas. Claves nunca en git.