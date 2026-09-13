# Manual de usuario de MetsuOS (MOS2)

**Versión del documento:** 1.2  
**Baseline:** v0.2.7 (árbol hacia 0.2.8)

Instalación: clonar metsuke/mos2, `./install.sh`, arranque `./mos2.sh`. Ver ENVIRONMENTS.md.

Al arrancar corren los tests; si fallan no hay sesión.

Comandos de sistema: a11y, apps, docs, help, man, synccheck, test, update, sysinfo, uptime, version, iarouter, red, exit, hilos, tareas, clear, echo.

iarouter está off por defecto. No envía hasta `usar` / `preguntar`. Las claves no se listan.

Apps: `apps list|show|install|remove`. Prioridad: sistema > app sistema > app usuario > user_.

Tras `update`, los módulos de la sesión no cambian solos: `update reiniciar` o salir y volver a entrar.

Detalle por comando: `man <comando>`. Specs: `docs specs/00-OVERVIEW.md`.
