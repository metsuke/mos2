# AGENTS.md — Punto de entrada para IA (MetsuOS / MOS2)

Si eres un agente o modelo y te piden estudiar este repositorio, empieza aquí y sigue `docs/AI_ONBOARDING.md`.

## Lectura mínima
1. Este archivo
2. docs/AI_ONBOARDING.md
3. docs/INCENTIVOS.md
4. docs/METHODOLOGY.md
5. docs/INTERACTION_REVIEW.md
6. docs/ENVIRONMENTS.md
7. docs/VERSIONING.md
8. docs/A11Y.md y docs/a11y/DECLARACION.md
9. docs/STYLE_GUIDE.md
10. docs/specs/00-OVERVIEW.md
11. docs/plans/ si hay campaña
12. Código y resto de specs según la tarea

## Avance de campaña
- `siguiente`, `siguiente paso` y `:s` son el mismo mandato: ejecutar el siguiente paso de la campaña activa.
- Un fichero por lote si es gordo; hasta tres si son cortos. Primero los claros, después un solo bloque multi con los `write`.
- Ritual de escritura: `write`/`w` solo en multi; primera línea del payload = sha256; luego Base64; `.` cierra; `code` abre el resultado.

## Normas que no se improvisan
- Comandos: execute(args) y help() -> str
- Ficheros de sistema moslib: tope 120 líneas
- Entregar archivos enteros; un paso cada vez
- Tests de arranque bloqueantes; integridad SHA de lo tracked
- Accesibilidad mandatoria
- Git, no funciones exclusivas de un forge
- Psicología: acompañar; no dañar, desestabilizar ni engañar

## Documentación y docgen
- Fuente: JSON en docs/docgen/
- generate no ingiere; ingest solo primera vez o recuperación
- En el próximo cierre de documentación: copiar la norma `:s` a METHODOLOGY.md e INTERACTION_REVIEW.md vía JSON + `docgen generate`

## Versiones
Runtime → bump pyproject.toml + tag. Solo docs → tag -docs.
Producto de referencia: 0.2.7 / árbol 0.2.8.
