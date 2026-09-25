# Plan 2026-09-24-01 — Tuplas CRUD para documentación (hacia 0.3.0)

**Rama de trabajo:** `docs/ritual-write-reqs` (o rama derivada `docs/tuplas` si se abre al primer commit de código).
**Estado:** Diseñada
**Versión del plan:** 1.0
**Alcance de producto:** 0.3.0 cuando documentación + (más adelante) código estén modelados como tuplas.
**Fuera de esta campaña:** codegen / MPL / MCL (campaña posterior; este plan es la referencia).

## Decisiones cerradas (2026-09-24)

1. Un archivo JSON por tupla. Árbol de carpetas = rutas de id (`docs/docgen/tuplas/req/REQ-INT-001.json`, `docs/docgen/tuplas/doc/02-srs/sec/requisitos.json`, …).
2. Si el texto sale de código, el cuerpo no va vacío: lleva la referencia exacta (comando o lote) que genera el trozo.
3. `influye_de` / `influye_a` son bidireccionales: al escribir A→B se escribe B←A.
4. Piloto: `ia-write`. Después todos los documentos del índice salvo, de momento, los planes de campaña. Incluye LICENSE: GPLv3 completa ingerida como tuplas.
5. Este fichero + anexo recogen prompt original, planteamiento previo y conclusión con Q&A.

## Objetivo

Sustituir MD/JSON monolíticos como fuente por un almacén de tuplas con CRUD. El MD (y el HTML) son un recorrido ordenado. Requisitos, sinopsis, secciones, índice y modos de render son tipos de la misma tupla.

## Fases de esta campaña

| Id | Fase | Hecho cuando |
|----|------|----------------|
| A | Schema `metsuos-tupla-1` + CRUD `tupla add\|set\|rm\|list` + dirs = rutas | Comando operativo; un JSON por nodo |
| B | Requisitos como `tipo=req` (fachada `docgen req`); campos humano/IA/orden/relaciones | Req existentes migrados o envueltos |
| C | CRUD de `render-modo` (parrafo, tabla consecutiva, h1–h6, lista, imagen, mermaid) | Un doc de prueba pinta tabla agrupada |
| D | Piloto `ia-write` solo con tuplas; generate recorre; MD desechable | `docgen generate ia-write` no aborta por longitud |
| E | Resto de documentos del índice (no planes); LICENSE = GPLv3 en tuplas | Cada doc tiene secciones obligatorias |
| F | Quitar umbral 50 % y JSON monolítico pages/specs como fuente | Generate no defiende el MD viejo |

## No hacer ahora

- Regenerar specs a mano / refundido página a página.
- Codegen de `moslib/` desde tuplas.
- Tratar `docs/plans/*.md` como tuplas (excepción explícita hasta revisión).

## Anexos

- `docs/plans/2026-09-24-01-tuplas-docgen-anexo.md` — prompt, planteamiento, conclusión y Q&A íntegros.

## Relación con 0.3.0

La campaña de código (tuplas de función/bucle/fichero/carpeta + codegen) debe citar **este** plan y el anexo como especificación de la tupla base. No se redefine el schema ahí; se hereda (`tipo` de programación).
