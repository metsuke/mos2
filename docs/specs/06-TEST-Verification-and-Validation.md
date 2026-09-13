# 06 – TEST · Verificación y validación

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.7 / árbol v0.2.8  
**Estado:** Normativo

Principios: Must verificable por test tiene test; arranque bloqueante; SEC en runtime y arranque; no desactivar tests para merge; A11Y habitual.

Batería actual: test_security.py, test_all_commands_security.py, test_system_commands_security.py, test_security_minimoslib.py, test_cmd_loader.py, test_cmd_loader_apps.py, test_cmd_loader_prefixes.py, test_apps.py, test_tasks.py, test_ia_router.py, test_ia_router_remotos.py, test_ia_keys.py, test_user.py, test_shell_basic.py, test_style_commands_contract.py, test_style_core_modules.py, test_style_no_forbidden_patterns.py, test_version_metadata.py, test_man_command.py, test_a11y_baseline.py.

Casos nuevos: minimoslib solo con app_dir; iarouter enabled=false sin HTTP; claves no en claro.

Paso: pytest verde + arranque OK. Fallo: test rojo, comando ilegal, contrato roto, saltarse arranque.

Sin cobertura mínima obligatoria ni CI de forge obligatoria. Sí batería local bloqueante.
