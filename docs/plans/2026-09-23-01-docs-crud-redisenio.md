# Plan 2026-09-23-01 — Recorte de docs, CRUD reqs, rediseño docgen

**Estado:** En curso  
**Rama:** desarrollo actual (no main)  
**Supersede:** refundido masivo de documentación de esta misma campaña

---

## Decisión (2026-09-23)

Se cancela el refundido fichero-a-fichero de documentación (specs restantes, mans, generate forzado contra umbral 50 %). El método actual no escala (tokens, abortos, riesgo de pérdida).

Orden nuevo, único vigente:

1. Requisitos CRUD (huecos del código ya existente).
2. Rediseño de raíz del sistema de documentación (incluye evaluar el método docgen actual).
3. Cierre de campaña (tests, integridad, publicar/consolidar).

---

## Lista de trabajo

| # | Ítem | Estado |
|---|------|--------|
| 1 | Tope 120 + test 120 | Hecho |
| 2 | Integridad + sellos + write registra hash | Hecho |
| 3 | multi / write.sh / codecs | Hecho |
| 4 | dev / update dev | Hecho |
| 5 | docs menú + sufijo h | Hecho |
| 6 | docgen índice disco + CRUD índice | Hecho (se rediseña después) |
| 7 | Historial MOSh con tope | Hecho |
| 8 | Locale es_ES al arranque | Hecho |
| 9 | arreglar_integridad.sh | Hecho |
| 10 | Refundido pages + root (parcial) | Hecho / congelado |
| 11 | Refundido specs (00–11) | **Cancelado** — rediseño |
| 12 | Refundido mans | **Cancelado** — rediseño |
| 13 | Generate masivo / umbral 50 % | **Cancelado** — rediseño |
| 14 | Requisitos CRUD alineados al código nuevo | **Siguiente** |
| 15 | Rediseño de raíz de documentación + evaluación del método docgen | **Después de 14** |
| 16 | Cierre: tests, integridad, dev publicar / consolidar | **Después de 15** |

---

## Alcance del bloque 14 (CRUD reqs)

Alta/edición/baja vía `docgen req` / `docgen area` (fuente JSON, no editar MD a mano). Cubrir al menos lo que el código ya hace y el SRS no tiene trazado:

- Integridad (manifiesto, sello, arranque, recargar consciente)
- write / multi / write.sh / codecs
- Tope 120 / test 120
- update dev / dev
- Locale es_ES
- docs menú + HTML
- Historial con tope

No regenerar specs enteras en este bloque salvo que el CRUD lo exija para un generate puntual de 02-srs.

---

## Fuera de alcance hasta el rediseño

- Volver a pintar 00-overview, 01-sss y resto de specs “a mano” desde el chat
- Inventario man comando a comando
- Relajar o pelear el umbral 50 % como parche permanente

---

## Criterio de cierre

El cierre no se abre hasta que 14 y 15 estén aceptados por el humano.
