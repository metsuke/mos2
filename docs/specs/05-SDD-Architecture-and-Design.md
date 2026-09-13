# 05 – SDD · Arquitectura y diseño

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.7 / árbol v0.2.8  
**Estado:** Normativo descriptivo alineado con el código

Capas: lanzamiento (mos2.sh, install.sh, rootfs/bin/mos.py); shell; núcleo (user, security, cmd_loader, apps, tasks, entorno, ia_*); comandos de sistema; apps; usuario; tests; docs.

Núcleo añadido tras 0.2.1: apps.py, tasks.py, entorno.py, ia_router.py, ia_keys.py, secreto.py, ia_share.py, ia_bridge.py, ia_check.py. App versionada: apps/dev.

Prioridad de carga: sistema > app sistema > app usuario > user_.

Flujo comando: línea → get_command → validate_command_file → execute.

Flujo iarouter: status/detectar; usar/clave/modelo; preguntar→complete; share ≠ publicar; puente on|off|status.

update: backup + origin/main + tags; update reiniciar porque la sesión no sustituye módulos sola.

Decisiones: apps fuera de moslib/commands; minimoslib acotado; iarouter off por defecto; puente no es P2P; worker de tareas en sesión.

Fuera de diseño: tienda remota, malla P2P, DepManager geo, GUI, sandbox OS, cliente web de X.
