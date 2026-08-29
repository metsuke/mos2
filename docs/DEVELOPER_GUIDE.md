# Guía del desarrollador de MetsuOS

**Versión del documento:** 1.2  
**Estado:** Normativo de proceso  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/STYLE_GUIDE.md, docs/VERSIONING.md, docs/A11Y.md, CHANGELOG.md, docs/ENVIRONMENTS.md, docs/AI_ONBOARDING.md, docs/specs/00-OVERVIEW.md, docs/plans/README.md

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

---

## Contexto de sesión

```text
Contexto: <sistema> / <entorno> / <rol>
```

Detalle: docs/ENVIRONMENTS.md.

---

## Flujo de una feature

1. git checkout main && git pull origin main
2. git checkout -b feature/nombre-descriptivo
3. Acordar plan por fases (humano + IA); si es campaña, docs/plans/
4. Una fase cada vez
5. Tests / arranque
6. Commit atómico
7. Merge a main al cerrar el conjunto
8. Aplicar docs/VERSIONING.md y actualizar CHANGELOG.md

---

## Dónde tocar qué

| Si necesitas... | Toca principalmente... | No olvides... |
|-----------------|------------------------|---------------|
| Prompt o REPL | moslib/core/shell.py | tests de arranque |
| Resolución de comandos | moslib/core/cmd_loader.py | ICD + tests loader |
| Política de imports | moslib/core/security.py | SEC + tests security |
| Homes / migración | moslib/core/user.py | USER + tests user |
| Comando de sistema | moslib/commands/nombre.py | contrato, man, help, tests |
| Comando de usuario | rootfs/home/usuario/.mos/commands/user_*.py | prefijo user_ y seguridad |
| Poetry / WSL / Git Bash | mos2.sh, install.sh | ENVIRONMENTS |
| Accesibilidad | docs/A11Y.md, docs/a11y/, tests a11y | declaración e informe |
| Normas de producto | docs/specs/ | luego código |
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

---

## Tests

Obligatorios en desarrollo y en producción (arranque de MOSh).

```text
./mos2.sh
```

Dentro del shell:

```text
test
```

Si Poetry está operativo en el PATH:

```text
poetry run pytest
```

Si fallan los tests de arranque, el sistema no abre sesión.

En 0.2.5: `a11y` solo corre tests de accesibilidad y regenera docs/a11y/informe.md.

---

## Estilo

Normas en docs/STYLE_GUIDE.md. Hay tests que comprueban contrato y patrones prohibidos (eval/exec, etc.).

---

## Versionado (resumen)

| Cambio | pyproject.toml | Tag | CHANGELOG |
|--------|----------------|-----|-----------|
| Runtime / scripts / comandos / seguridad | Bump X.Y.Z | vX.Y.Z | Entrada de producto |
| Solo docs / onboarding | No bump | vX.Y.Z-docs o vX.Y.Z-docs.N | Entrada -docs |

Al cerrar producto: README, 07-SRelD y CHANGELOG si aplica.

Detalle: docs/VERSIONING.md.

---

## Documentación al cambiar algo

- Encabezados sin numeración
- Directorios en tablas (una columna por nivel)
- Comandos de sistema: columna Tipo A–Z y comandos A–Z dentro del tipo
- Página man para comando de sistema nuevo
- Si el doc o el código nuevo es más corto que el del repo, verificar que no se pierde contenido
- Entregar archivos completos listos para pegar; un paso cada vez
- Cacho 1 = sustituye todo el fichero; cachos siguientes = pegar debajo
- Breadcrumb de campaña en cada paso de trabajo con IA

---

## Trabajo con IA

La IA debe seguir docs/AI_ONBOARDING.md y AGENTS.md:

- un archivo por bloque copiable
- un paso cada vez
- leer el repo antes de afirmar el estado de un fichero
- no inventar features
- no resumir sin consultar
- Git, no el forge

---

## Checklist pre-merge

1. Tests en verde
2. Arranque de MOSh OK
3. SEC / SSS / ICD / A11Y respetados
4. Docs tocadas si cambió comportamiento o proceso
5. CHANGELOG actualizado si la fase cierra una release
6. VERSIONING aplicado (bump o explícitamente no)
7. Commit claro

---

## Autoridad

Esta guía no sustituye a SEC, SSS, A11Y ni STYLE_GUIDE. Si hay conflicto, prevalecen las specs de seguridad, sistema y accesibilidad.