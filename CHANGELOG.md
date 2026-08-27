# Changelog de MetsuOS

Los cambios relevantes se listan aquí. El formato sigue la idea de Keep a Changelog y la política de `docs/VERSIONING.md`.

## Sin publicar

Cambios en `main` posteriores al último tag, si los hay.

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