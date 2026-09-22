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

## Normas que no se improvisan
- Comandos: execute(args) y help() -> str
- Imports en comandos: solo biblioteca estándar y moslib
- El usuario no sobrescribe comandos de sistema (prefijo user_)
- Tests de arranque bloqueantes
- Accesibilidad de interfaz mandatoria (docs/A11Y.md)
- Tope 120 líneas por fichero de código; consultar con `test 120`
- Dirección de trabajo: docs/INCENTIVOS.md (mandatorio para la IA; los humanos se inclinan, no se puntúan)
- Asimov (cita + nota) y psicología de acompañamiento: capítulo IA de INCENTIVOS.md
- Sin rutas personales ni nombres de máquina en docs públicas
- Encabezados de documentación sin numeración
- Entregar archivos enteros; tablas ya montadas; un paso cada vez
- No remitir a un pegado anterior: volver a pegar
- Cacho 1 sustituye el fichero; no cortar un spec a mitad sin aviso
- Si el archivo nuevo es más corto, avisarlo
- Directorios en tablas (una columna por nivel)
- Comandos de sistema: Tipo A–Z, comandos A–Z dentro del tipo
- Breadcrumb de campaña en cada paso; explicar saltos de número
- Git, no funciones exclusivas de un forge
- Edición habitual: multi (dentro) o ./write.sh (fuera); lote write + hash + payload + punto + docgen generate
- Estado del repo: comando synccheck y lectura por SHA
- Psicología: acompañar; no dañar, desestabilizar ni engañar

## Documentación y docgen
- Fuente de verdad de la docs: JSON en docs/docgen/ (man/, specs/, pages/, root/, areas.json, index.json).
- El markdown publicado se obtiene con `docgen generate`.
- La IA no reescribe specs, manual ni man enteros en el chat salvo que el humano lo pida.
- Flujo normal: editar el JSON (átomo) y `docgen generate <id>` en el mismo lote.
- Si el id no está en el índice: `docgen index add <id> <rel>`.
- `docgen ingest` solo en la primera absorción o si hay que recuperar desde markdown/backup.
- `generate` no debe volver a ingerir: ingerir al generar pisa el JSON con un md viejo o corto.
- Un fichero por mensaje; fichero entero; no parches sueltos.
- Ids de pages: el fichero es docs/docgen/pages/<id>.json (ai-onboarding, no ia-onboarding).

## multi y write.sh
Dentro de MOS: `m` / `multi`. Acumula el pegado. Parseo solo con una línea que sea `:e` o `:q` (también `;e` `;q`).
Fuera: `./write.sh` lanza el mismo multi. No emular en bash.
Lote:
write <ruta>
<sha256 del claro>
[gz:|xz:|b85:|gzb85:|xzb85:]payload
.
docgen generate <id>
Máximo tres writes pequeños por lote.

## Contexto de sesión
```text
Contexto: <sistema> / <entorno> / <rol>
```

Si falta y hace falta para paths o Poetry, preguntar.

## Versiones
Cambio de runtime → bump en pyproject.toml + tag vX.Y.Z.
Solo docs → sin bump; tag vX.Y.Z-docs o vX.Y.Z-docs.N.
Detalle: docs/VERSIONING.md.

Producto de referencia: 0.2.7 / árbol 0.2.8. Comandos a11y, docs, synccheck, docgen.

## Qué no hacer
- No inventar features ausentes en código o specs
- No desactivar seguridad ni tests para hacer pasar un cambio
- No excluir un perfil A11Y por comodidad
- No asumir Mac, Git Bash o WSL sin contexto declarado
- No diagnosticar el remoto solo con raw .../main/
- No abrir DepManager ni política geo de paquetes en esta baseline (solo dirección)
- No usar ingest como paso rutinario de edición
- No usar ./arreglar_integridad.sh como atajo diario
- No crear .py de más de 120 líneas