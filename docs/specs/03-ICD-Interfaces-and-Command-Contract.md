# 03 – ICD · Interfaces y contrato de comandos

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.7 / árbol 0.2.8  
**Estado:** Normativo

## Contrato

Todo comando (sistema, app o usuario): execute(args) y help() → str no vacío. Imports: stdlib + moslib (+ minimoslib de esa app).

## Ubicación

Sistema: moslib/commands/<nombre>.py  
App fuente: apps/<id>/commands/  
App usuario: .mos/apps/  
Usuario: .mos/commands/user_*.py

## Resolución

1 sistema → 2 app sistema → 3 app usuario → 4 user_completo → 5 user_corto. También id_cmd y app_id_cmd.

## Interfaces

Shell ↔ cmd_loader.get_command. Loader ↔ security.validate_command_file. user.py: username, homes, ensure_user_space. Entrada: rootfs/bin/mos.py.

help / man / docs (lista blanca). a11y escribe informe. update: backup, fetch, tags, reset origin/main, poda; update reiniciar.

Apps: moslib.core.apps + comando apps.  
Tareas: moslib.core.tasks + tareas/hilos + worker de sesión.  
IA: ia_router, ia_keys, secreto, ia_share, ia_bridge, ia_check + comando iarouter. Off por defecto. Sin preguntar no hay envío.  
red: diagnóstico de anfitrión.

## Invariantes

Sin loader no hay execute. SEC activa. user_corto no gana a sistema ni a app con prioridad. docs no sale de lista blanca. Color no es única señal. iarouter enabled=false ⇒ sin red.

Verificación: contrato, loader, apps, SEC, minimoslib, ia_router, ia_keys, A11Y, docs.
