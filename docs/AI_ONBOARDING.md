# Onboarding para agentes IA (MetsuOS)

**Versión del documento:** 1.7
**Estado:** Normativo de proceso
**Documentos relacionados:** AGENTS.md, docs/INCENTIVOS.md, docs/METHODOLOGY.md, docs/INTERACTION_REVIEW.md, docs/ENVIRONMENTS.md, docs/VERSIONING.md, docs/A11Y.md, docs/STYLE_GUIDE.md, docs/specs/00-OVERVIEW.md, docs/IA_WRITE.md, docs/IA_LOTE.md

## Propósito
Que cualquier modelo, al estudiar el repo desde cero, trabaje sin reinventar normas, sin romper lo existente y sin marear al humano.

Punto de entrada corto: `AGENTS.md`.
Dirección de trabajo: `docs/INCENTIVOS.md` (mandatorio para la IA).

## Orden de lectura
1. AGENTS.md
2. Este archivo
3. docs/INCENTIVOS.md
4. docs/METHODOLOGY.md
5. docs/INTERACTION_REVIEW.md
6. docs/ENVIRONMENTS.md
7. docs/VERSIONING.md
8. docs/A11Y.md y docs/a11y/DECLARACION.md
9. docs/STYLE_GUIDE.md
10. docs/specs/00-OVERVIEW.md y el resto de specs según la tarea
11. docs/plans/ si hay campaña
12. Código solo cuando se sepa qué norma aplica

No inventar features que no estén en código o specs.

## Qué es MetsuOS (férreo)
- SO simulado modular en Python; shell MOSh.
- Núcleo moslib/; rootfs/ simulado.
- Contrato: execute(args) y help() -> str no vacío.
- Imports de comandos: solo stdlib + moslib (AST).
- Usuario anfitrión; comandos user_*.py; nunca pisan sistema.
- Tests de arranque bloqueantes.
- A11Y de interfaz mandatoria.
- Poetry + mos2.sh / install.sh multi-entorno.
- Git, no APIs de un forge.
- Comandos de calidad actuales: test, update, synccheck, docgen.
- Tope 120 líneas por fichero de código; `test 120` consulta sin tumbar el sistema.
- Incentivos: vectores comunes; humanos se inclinan; IA está obligada. Sin karma.

## Documentación y docgen
Fuente de verdad: JSON en docs/docgen/ (man/, specs/, pages/, root/, areas.json, index.json).
El markdown publicado se pinta con `docgen generate`.
Flujo normal de la IA: un JSON por mensaje, fichero entero, luego `docgen generate <id>` en el mismo lote.
Si el id no está en el índice: `docgen index add <id> <rel>` en ese lote.
`docgen ingest` solo primera absorción o recuperación desde markdown/backup.
`generate` no ingerir: si ingerir al generar, el JSON se pisa con un md viejo o corto.
Prohibido reescribir specs/manual/man enteros en el chat como vía habitual.

## Edición: multi y write.sh
Dentro de MOS: `m` o `multi`. Se pega el bloque entero. multi acumula; no parsea hasta una línea que sea solo `:e` (ejecuta) o `:q` (cancela). `;e` y `;q` valen igual.
Fuera de MOS: `./write.sh` lanza el mismo multi. No emular el lote en bash.
Forma del lote:
write <ruta>
<sha256 del fichero en claro>
[prefijo]payload
.
docgen index add <id> <rel>
docgen generate <id>
Luego línea sola `:e`.
Máximo tres writes por lote si son ficheros pequeños. write registra integridad si el hash coincide.

## Codecs del payload
El hash es siempre SHA-256 del contenido en claro, no del payload.
sin prefijo = Base64 del fichero
`gz:` gzip+Base64
`xz:` lzma+Base64
`b85:` ascii85
`gzb85:` gzip+ascii85
`xzb85:` lzma+ascii85
La IA elige el más corto que el decoder ya tenga. Si CRC o payload inválido: el pegado se cortó; repetir en Base64 plano o pegar el fichero con `code` y `./arreglar_integridad.sh`.

## Contexto de sesión
```text
Contexto: <sistema> / <entorno> / <rol>
```

Si falta y hace falta para paths o Poetry, preguntar. Sin hostnames ni rutas home en el repo público.

## Cómo entregar trabajo al humano
- Un paso / un fichero por mensaje, salvo pareja inseparable avisada (write + generate cuenta como un lote).
- Fichero **entero**. Prohibido “añade esta fila”: las tablas van montadas.
- Prohibido “usa lo que te di antes”: volver a pegar el documento.
- Cachos solo si no cabe: cacho 1 sustituye todo; no dejar un spec inválido a mitad.
- Completo habitual: lote write (hash + payload + punto) + generate, vía multi o ./write.sh.
- Alternativa editor: mkdir / touch / code, luego el texto; después integridad.
- Parcial (avisando “no sustituyas el fichero”): primero el recorte, luego code.
- Encabezados sin numeración.
- Directorios en tablas (una columna por nivel).
- Comandos: Tipo A–Z, comando A–Z dentro del tipo.
- Si el nuevo texto es más corto que el del repo: avisar. No resumir sin consultar.
- Breadcrumb: campaña, grupo, bloque x/y, paso, %, contexto.
- Si se salta un número de paso: explicar por qué en el mismo mensaje.
- No usar «corrida». CHANGELOG: no dejar «Sin publicar» al humano.
- Psicología: acompañar; prohibido dañar, desestabilizar o engañar.
- Asimov (docs/INCENTIVOS.md): cita + nota de aplicación; no autocommit; no apagar tests.

## Estado real del repositorio
1. Pedir `synccheck` cuando haya duda.
2. Leer por SHA (`git show origin/main:archivo` o raw con SHA).
3. No diagnosticar solo con `.../main/` en CDN.
4. Si Poetry, README, CHANGELOG y comandos no cuadran: hotfix antes del siguiente bloque.

Producto de referencia al escribir esto: **0.2.7 / árbol 0.2.8**. Comandos `a11y`, `docs`, `synccheck`, `docgen`.

## Antes de tocar código
1. Leer el repo real (SHA).
2. Impacto SEC / SSS / ICD / SRS / A11Y / INCENTIVOS.
3. STYLE_GUIDE e imports.
4. Plan por fases; campaña en docs/plans/.
5. No desactivar tests ni seguridad.
6. VERSIONING (¿bump? ¿tag?).
7. Comando nuevo: código + help + man + README + SSS + CHANGELOG.
8. No abrir DepManager ni política geo real (solo dirección).
9. No crear un .py de más de 120 líneas: partir en submódulos.

## Integridad de emergencia
`./arreglar_integridad.sh` solo si MOS no arranca por hashes. Aviso 30 s con barra. Reescribe el manifiesto al contenido actual del clone y lanza `./mos2.sh` con `MOS_INTEGRIDAD=recargar`.
El alias `mos2` no existe dentro de un script no interactivo.
No es uso diario. No usarlo si no se reconocen los cambios.

## Versionado
| Cambio | Poetry | Tag |
|--------|--------|-----|
| Runtime / comandos / scripts | Bump X.Y.Z | vX.Y.Z |
| Solo docs | No bump | vX.Y.Z-docs o vX.Y.Z-docs.N |

## Plataforma
- Poetry: un candidato solo si `--version` se puede ejecutar.
- windows/git-bash: `py -m poetry`.
- windows/wsl: clone en FS Linux; rechazo bajo `/mnt/<letra>/`.
- Lanzador portable: `./mos2.sh`, no el alias `mos2` desde scripts.

## Accesibilidad
docs/A11Y.md es mandatoria. Conflicto con SEC: procedimiento escrito.

## Cierre de grupo
docs/INTERACTION_REVIEW.md: interacción + deuda + campañas futuras + auditoría.

## Checklist de cada mensaje de trabajo
1. ¿Breadcrumb?
2. ¿Un paso / un fichero (o lote write+generate)?
3. ¿Fichero entero (JSON si es docs)?
4. ¿Tablas ya hechas?
5. ¿He vuelto a pegar en vez de remitir?
6. ¿SHA o synccheck si hablo del remoto?
7. ¿A11Y / SEC / INCENTIVOS / contrato intactos?
8. ¿He evitado ingest de rutinario?
9. ¿El id está en docs/docgen/index.json?
10. ¿Tope 120 si toco código?

## Autoridad
Este documento manda sobre el estilo de asistencia.
Si choca con SEC, SSS, A11Y o INCENTIVOS, prevalecen esas normas y luego se actualiza este archivo.