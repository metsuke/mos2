# Guía del desarrollador de MetsuOS

**Versión del documento:** 1.4  
**Estado:** Normativo de proceso  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/STYLE_GUIDE.md, docs/VERSIONING.md, docs/A11Y.md, CHANGELOG.md, docs/ENVIRONMENTS.md, docs/AI_ONBOARDING.md, docs/IA_WRITE.md, docs/specs/00-OVERVIEW.md, docs/plans/README.md

---

## Propósito
Cómo contribuir código y documentación sin romper normas férreas ni desincronizar versiones.

El método general está en docs/METHODOLOGY.md. Aquí está el flujo práctico día a día.

---

## Requisitos de trabajo
- Python 3.10+
- Poetry
- Git
- Clone único por entorno (no mezclar /mnt/c y ~/mos2 en WSL)

Instalación:

```text
./install.sh
./mos2.sh
```

Edición con IA: `multi` dentro de MOS o `./write.sh` fuera.

---

## Contexto de sesión
```text
Contexto: <sistema> / <entorno> / <rol>
```

Detalle: docs/ENVIRONMENTS.md.

---

## Flujo de una feature
1. git checkout main && git pull origin main
2. Rama feature (comando `dev` / nunca trabajar sobre main)
3. Acordar plan por fases; si es campaña, docs/plans/
4. Una fase cada vez
5. Tests / arranque (`test`, `test 120`)
6. Commit atómico
7. Consolidar rama y volcar a main al cerrar el conjunto
8. Aplicar docs/VERSIONING.md y actualizar CHANGELOG.md

---

## Dónde tocar qué
| Si necesitas... | Toca principalmente... | No olvides... |
|-----------------|------------------------|---------------|
| Prompt o REPL | moslib/core/shell.py y hermanos | tests de arranque, historial |
| Resolución de comandos | moslib/core/cmd_loader.py | ICD + tests loader |
| Política de imports | moslib/core/security.py | SEC + tests security |
| Homes / migración | moslib/core/user.py | USER + tests user |
| Integridad | moslib/core/integridad*.py | sello + tests integridad |
| Docgen | moslib/core/docgen*.py + docs/docgen/ | index.json, generate |
| Comando de sistema | moslib/commands/nombre.py | contrato, man, help, ≤120 líneas |
| Comando de usuario | rootfs/home/usuario/.mos/commands/user_*.py | prefijo user_ y seguridad |
| Poetry / WSL / Git Bash | mos2.sh, install.sh | ENVIRONMENTS |
| Accesibilidad | docs/A11Y.md, docs/a11y/, tests a11y | declaración e informe |
| Normas de producto | docs/specs/ vía JSON docgen | luego código |
| Relato de una release | CHANGELOG.md | VERSIONING.md |
| Plan de campaña | docs/plans/ | README de planes |

---

## Contrato de comando
Todo comando de sistema o de usuario:

- execute(args) callable
- help() que devuelve str no vacío
- solo imports de stdlib y moslib
- nombre de sistema = archivo sin .py
- usuario: archivo user_*.py
- fichero ≤ 120 líneas; si no, fachada + submódulos en core

---

## Tests
Obligatorios en desarrollo y en producción (arranque de MOSh).

```text
./mos2.sh
test
test 120
```

Si Poetry está operativo:

```text
poetry run pytest
```

Si fallan los tests de arranque, el sistema no abre sesión. `test 120` lista tope; no tumba el sistema.

---

## Estilo
Normas en docs/STYLE_GUIDE.md. Tests de contrato y patrones prohibidos. Tope 120 líneas.

---

## Versionado (resumen)
| Cambio | pyproject.toml | Tag | CHANGELOG |
|--------|----------------|-----|-----------|
| Runtime / scripts / comandos / seguridad | Bump X.Y.Z | vX.Y.Z | Entrada de producto |
| Solo docs / onboarding | No bump | vX.Y.Z-docs o vX.Y.Z-docs.N | Entrada -docs |

Detalle: docs/VERSIONING.md.

---

## Documentación al cambiar algo
- Fuente: JSON en docs/docgen/. Pintar con `docgen generate <id>` en el mismo lote.
- Encabezados sin numeración
- Directorios en tablas
- Página man para comando nuevo
- Si el doc o el código nuevo es más corto, avisar
- Lote write + hash + payload + punto + generate; `:e` cierra
- Cacho 1 sustituye el fichero; siguientes debajo
- Breadcrumb: tarea x/y + %; bloque; campaña; planeado

---

## Trabajo con IA
Seguir docs/AI_ONBOARDING.md, AGENTS.md y docs/IA_WRITE.md.

- un JSON/código por lote write
- un paso cada vez (`:s` = siguiente)
- leer el repo por SHA antes de afirmar estado
- no inventar features ni resumir sin consultar
- Git, no el forge
- no ingest rutinario ni arreglar_integridad diario

---

## Checklist pre-merge
1. Tests en verde
2. Arranque de MOSh OK (sin recargar integridad)
3. SEC / SSS / ICD / A11Y respetados
4. Docs (JSON + generate) si cambió comportamiento
5. CHANGELOG si cierra release
6. VERSIONING aplicado
7. Commit claro
8. test 120 sin pendientes o con plan

---

## Autoridad
Esta guía no sustituye a SEC, SSS, A11Y ni STYLE_GUIDE. Si hay conflicto, prevalecen las specs de seguridad, sistema y accesibilidad.