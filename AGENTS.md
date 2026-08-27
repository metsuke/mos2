# AGENTS.md — Punto de entrada para IA (MetsuOS / MOS2)

Si eres un agente o modelo y te piden estudiar este repositorio, empieza aquí y sigue el orden de `docs/AI_ONBOARDING.md`.

## Lectura mínima

1. Este archivo
2. docs/AI_ONBOARDING.md
3. docs/METHODOLOGY.md
4. docs/ENVIRONMENTS.md
5. docs/VERSIONING.md
6. docs/STYLE_GUIDE.md
7. docs/specs/00-OVERVIEW.md
8. Código y resto de specs según la tarea

## Normas que no se improvisan

- Comandos: execute(args) y help() -> str
- Imports en comandos: solo biblioteca estándar y moslib
- El usuario no sobrescribe comandos de sistema (prefijo user_)
- Tests de arranque bloqueantes
- Sin rutas personales ni nombres de máquina en docs públicas
- Encabezados de documentación sin numeración
- Entregar archivos en un solo bloque copiable; un paso cada vez
- Directorios en tablas (una columna por nivel)
- Comandos de sistema en tablas: Tipo A–Z, comandos A–Z dentro del tipo

## Contexto de sesión

```text
Contexto: <sistema> / <entorno> / <rol>
```

Si falta y hace falta para paths o Poetry, preguntar.

## Versiones

Cambio de runtime → bump en pyproject.toml + tag vX.Y.Z.  
Solo docs → sin bump; tag opcional vX.Y.Z-docs.  
Detalle: docs/VERSIONING.md.

## Qué no hacer

- No inventar features ausentes en código o specs
- No desactivar seguridad ni tests para hacer pasar un cambio
- No asumir Mac, Git Bash o WSL sin contexto declarado