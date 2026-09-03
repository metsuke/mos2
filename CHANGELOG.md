# Changelog de MetsuOS

Los cambios relevantes se listan aquí. El formato sigue la idea de Keep a Changelog y la política de `docs/VERSIONING.md`.

## 0.2.6 — 2026-09-03

### Añadido

- Specs 08-APPS, 09-TASKS, 10-IA-ROUTER y reserva en SSS 1.4
- Comando apps (install/list/show/remove local, puerta SEC)
- Comandos tareas y hilos (GTD local, tick clase sistema)
- Comando iarouter y fachada moslib.core.ia_router (off por defecto)

## 0.2.5-docs.2 — 2026-08-31

### Documentación

- Plan de campaña 06 (incentivos, desarrollo en MOS2, datos)
- docs/INCENTIVOS.md (vectores, roles, Asimov + psicología; sin karma)
- Enlaces en AGENTS, AI_ONBOARDING, HUMAN_ONBOARDING, README, DEUDA_Y_CAMPANAS

## 0.2.5 — 2026-08-30

### Añadido

- Comando a11y (tests marcados a11y + informe en docs/a11y/)
- Comando docs (docs/ y README, CHANGELOG, AGENTS, LICENSE)
- Comando synccheck (HEAD local vs origin/main)
- Política A11Y, declaración estilo UE/ES adaptada a CLI
- test regenera el informe A11Y
- docs/INTERACTION_REVIEW.md

### Cambiado

- Mensajes de arranque y de test en texto, sin emoji como única señal

## 0.2.4 — 2026-08-28

### Añadido

- Comando update: sincroniza tags locales con origin (fetch --tags --prune --prune-tags)

### Documentación

- man de update
- Campaña 05: esta pieza sale del Cierre I (renombre de tags -docs), no del bloque A11Y

## Notas de etiquetas

Los tags `v0.2.3-docs` y `v0.2.4-docs` se renombraron a `v0.2.2-docs.2` y `v0.2.2-docs.3` (docs sobre el producto 0.2.2). El producto actual es `v0.2.5`.

## 0.2.3 — 2026-08-28

### Corregido

- Poetry en Git Bash / Unix: un candidato solo se usa si `--version` se puede ejecutar
- `.gitattributes`: LF en scripts y textos (función de Git, no de un forge)

### Documentación

- ENVIRONMENTS alineado con el orden real de resolución
- Planes de campaña en docs/plans/

## 0.2.4-docs — 2026-08-28

### Documentación

- CHANGELOG.md como relato de releases
- VERSIONING y DEVELOPER_GUIDE alineados con CHANGELOG
- Test de formato SemVer de la versión Poetry

## 0.2.3-docs — 2026-08-27

### Documentación

- Onboarding para IA (`AGENTS.md`, `docs/AI_ONBOARDING.md`)
- Onboarding humano y guía de desarrollador
- Política de versionado (`docs/VERSIONING.md`)
- Enlaces en README, METHODOLOGY y OVERVIEW
- Hotfix: `SCRIPT_DIR` antes del guard WSL `/mnt` (incluido en la rama de onboarding)

## 0.2.2 — 2026-08-25

### Añadido

- `docs/ENVIRONMENTS.md` (perfiles, Poetry, contexto de sesión)
- Guard WSL: rechazo de clones bajo `/mnt/<letra>/`

### Corregido

- Resolución portable de Poetry en `mos2.sh` e `install.sh`
- En Git Bash, prioridad de `py -m poetry` frente a `poetry.exe` (Permission denied)

### Documentación

- Manual, methodology y specs alineados con entornos multiplataforma

## 0.2.1

### Añadido

- Tests unitarios y de seguridad; arranque bloqueante
- Comando `update` con ramas backup locales
- Comando `man` y páginas en `docs/man/`
- Marco ECSS-light, STYLE_GUIDE y USER_MANUAL (evolución inmediata sobre la baseline)

### Seguridad

- Validación AST de imports en comandos de sistema y de usuario
- Inventario de seguridad en arranque

## 0.2.0-alpha-user-space

### Añadido

- Espacio personal por usuario del sistema anfitrión
- Comandos `user_*` e invocación corta sin conflicto
- Protección de comandos de sistema