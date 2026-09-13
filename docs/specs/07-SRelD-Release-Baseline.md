# 07 – SRelD · Baseline de release

**Versión del documento:** 1.2  
**Baseline histórica:** v0.2.1  
**Producto en main:** v0.2.7  
**Siguiente tag de producto:** v0.2.8 (pendiente de pruebas humanas)  
**Estado:** Normativo de referencia

Congela v0.2.1 (MOSh, loader, SEC AST, espacio usuario, tests de arranque, comandos help/version/sysinfo/uptime/echo/clear/test/update/exit).

Evolución: 0.2.2 Poetry/ENVIRONMENTS; 0.2.3 Git Bash; 0.2.4 tags; 0.2.5 a11y/docs/synccheck; 0.2.6 specs 08-10 y comandos apps/tareas/hilos/iarouter; 0.2.7 apps reales, worker, proveedores; 0.2.8 árbol modelos/clave/LAN/share/puente/update reiniciar.

Comandos actuales: a11y, apps, docs, help, man, synccheck, test, update, sysinfo, uptime, version, iarouter, red, exit, hilos, tareas, clear, echo.

Núcleo añadido: apps, tasks, ia_router, ia_keys, secreto, ia_share, ia_bridge, ia_check, entorno; apps/dev.

No regresión 0.2.1 + Poetry portable + SEC de apps + iarouter off por defecto.

Limitaciones: Alpha; sin CI obligatoria; 0.2.8 sin tag hasta pruebas humanas; check scopes es otro plan; sin malla P2P ni DepManager geo.
