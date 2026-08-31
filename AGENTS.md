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
- Crear ficheros: mkdir -p / touch / editor
- Estado del repo: comando synccheck y lectura por SHA
- Psicología: acompañar; no dañar, desestabilizar ni engañar

## Contexto de sesión

```text
Contexto: <sistema> / <entorno> / <rol>
```

Si falta y hace falta para paths o Poetry, preguntar.

## Versiones

Cambio de runtime → bump en pyproject.toml + tag vX.Y.Z.  
Solo docs → sin bump; tag vX.Y.Z-docs o vX.Y.Z-docs.N.  
Detalle: docs/VERSIONING.md.

Producto de referencia: 0.2.5. Comandos a11y, docs, synccheck.

## Qué no hacer

- No inventar features ausentes en código o specs
- No desactivar seguridad ni tests para hacer pasar un cambio
- No excluir un perfil A11Y por comodidad
- No asumir Mac, Git Bash o WSL sin contexto declarado
- No diagnosticar el remoto solo con raw .../main/
- No abrir DepManager ni política geo de paquetes en esta baseline (solo dirección)