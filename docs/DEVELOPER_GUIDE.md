# Guía del desarrollador de MetsuOS

**Versión del documento:** 1.1  
**Estado:** Normativo de proceso  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/STYLE_GUIDE.md, docs/VERSIONING.md, CHANGELOG.md, docs/ENVIRONMENTS.md, docs/AI_ONBOARDING.md, docs/specs/00-OVERVIEW.md

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
3. Acordar plan por fases (humano + IA)
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
| Normas de producto | docs/specs/ | luego código |
| Relato de una release | CHANGELOG.md | VERSIONING.md |

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

---

## Estilo

Normas en docs/STYLE_GUIDE.md. Hay tests que comprueban contrato y patrones prohibidos (eval/exec, etc.).

---

## Versionado (resumen)

| Cambio | pyproject.toml | Tag | CHANGELOG |
|--------|----------------|-----|-----------|
| Runtime / scripts / comandos / seguridad | Bump X.Y.Z | vX.Y.Z | Entrada de producto |
| Solo docs / onboarding | No bump | vX.Y.Z-docs opcional | Entrada -docs |

Al cerrar producto: README, 07-SRelD y CHANGELOG si aplica.

Detalle: docs/VERSIONING.md.

---

## Documentación al cambiar algo

- Encabezados sin numeración
- Directorios en tablas (una columna por nivel)
- Comandos de sistema: columna Tipo A–Z y comandos A–Z dentro del tipo
- Página man para comando de sistema nuevo
- Si el doc nuevo es más corto que el del repo, verificar que no se pierde norma
- Entregar archivos completos listos para pegar; un paso cada vez

---

## Trabajo con IA

La IA debe seguir docs/AI_ONBOARDING.md y AGENTS.md:

- un archivo por bloque copiable
- un paso cada vez
- leer el repo antes de afirmar el estado de un fichero
- no inventar features

---

## Checklist pre-merge

1. Tests en verde
2. Arranque de MOSh OK
3. SEC / SSS / ICD respetados
4. Docs tocadas si cambió comportamiento o proceso
5. CHANGELOG actualizado si la fase cierra una release
6. VERSIONING aplicado (bump o explícitamente no)
7. Commit claro

---

## Autoridad

Esta guía no sustituye a SEC, SSS ni STYLE_GUIDE. Si hay conflicto, prevalecen las specs de seguridad y sistema.