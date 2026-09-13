# 06 – TEST · Verificación y validación

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.4 (texto 1.1 conservado); producto v0.2.7 / árbol v0.2.8  
**Estado:** Normativo  
**Documentos relacionados:** docs/specs/02-SRS-Software-Requirements.md, docs/specs/04-SEC-Security-Policy.md, docs/A11Y.md, docs/STYLE_GUIDE.md, docs/METHODOLOGY.md

---

## Propósito

Este documento define cómo se verifica y valida MetsuOS.

Objetivos:

- demostrar que el sistema cumple los requisitos Must
- impedir el arranque sobre una base rota
- hacer de los tests una parte normal del producto, no solo del desarrollo
- verificar accesibilidad automática y regenerar el informe A11Y

---

## Principios

1. Si un requisito Must es verificable por test, debe existir un test.
2. Los tests de arranque son puerta de calidad del sistema.
3. La seguridad se verifica tanto en runtime como en arranque.
4. Un cambio no está terminado hasta que la batería relevante pasa.
5. No se desactivan tests para forzar un merge.
6. Los tests A11Y forman parte del proceso habitual (desarrollo y producción).

---

## Alcance de la verificación

| Área | Qué se verifica |
|------|-----------------|
| Seguridad | Política de imports y rechazo de comandos ilegales |
| Usuario | Resolución de usuario, rutas y espacio .mos |
| Loader | Resolución de nombres, carga y rechazo seguro |
| Contrato de comandos | execute/help en comandos de sistema |
| Estilo crítico | Docstrings de core, ausencia de eval/exec indebidos |
| Arranque | Ejecución de pytest y bloqueo si hay fallos |
| Documentación operativa | Existencia de man/manual/specs cuando el requisito lo exige |
| Accesibilidad | Prefijos, help, no solo-color, declaración, informe, comandos a11y y docs |

---

## Organización de tests

| Nivel 1 | Nivel 2 | Función |
|---------|---------|---------|
| tests/ | conftest.py | Path de proyecto y fixtures comunes |
| tests/ | test_security.py | Casos unitarios de política de imports |
| tests/ | test_all_commands_security.py | Inventario real sistema + usuario actual |
| tests/ | test_system_commands_security.py | Seguridad y contrato básico de comandos de sistema |
| tests/ | test_cmd_loader.py | Carga, resolución y rechazo en loader |
| tests/ | test_user.py | Usuario y espacio personal |
| tests/ | test_shell_basic.py | Propiedades básicas de shell/usuario |
| tests/ | test_style_commands_contract.py | Contrato execute/help |
| tests/ | test_style_core_modules.py | Docstrings de módulos core |
| tests/ | test_style_no_forbidden_patterns.py | Patrones prohibidos |
| tests/ | test_version_metadata.py | Formato SemVer de Poetry |
| tests/ | test_a11y_*.py | Tests marcados a11y |

---

## Niveles de prueba

### Unitarias

Validan funciones y módulos aislados: security.analyze_imports, user path helpers, contrato de comandos, estilo crítico, generación / lectura del informe A11Y.

### Integración ligera

CommandManager + security; shell startup tests runner; inventario de comandos reales; comando a11y + escritura de informe.

### Demostración manual

prompt y exit; man; docs; a11y; update con y sin cambios locales; bloqueo de arranque con user_*.py ilegal.

---

## Tests de arranque

Al iniciar MOSh: se ejecuta la batería; si return code != 0, error claro y accionable; no hay REPL; el proceso termina con error.

Mínimo: seguridad de sistema y del usuario actual; contrato execute/help; humo de usuario; patrones prohibidos. Si la batería incluye a11y, se regenera el informe.

Mensaje de fallo: arranque bloqueado; revisar tests o comandos ilegales; `poetry run pytest`; no solo color.

---

## Verificación de seguridad

| Caso | Resultado esperado |
|------|--------------------|
| import os / pathlib / moslib | permitido |
| import requests / numpy / jander | rechazado |
| from . import x | rechazado |
| comando ilegal en runtime | no se ejecuta + mensaje [SEGURIDAD] |
| comando ilegal presente al arranque | arranque bloqueado |

---

## Verificación del contrato de comandos

Sistema: .py en moslib/commands/, execute callable, help callable, help() str no vacío.
Usuario: user_*.py, misma SEC, no tapar sistema.

---

## Verificación de accesibilidad

Marca pytest: `a11y`. Comando `a11y` escribe docs/a11y/informe.md e informe.json.

| Valor | Criterio alpha |
|-------|----------------|
| plenamente conforme | Tests a11y obligatorios en verde y sin no conformidades abiertas |
| no conforme | Falla un test a11y de requisito obligatorio |
| parcialmente conforme | Tests de requisito pasan o aún no hay ejecución automática; hay excepciones o implantación incompleta |

Fuera de laboratorio: GUI, lectores de escritorio, sello WCAG / RD 1112/2018.

---

## Comando de sistema `test`

Lanza pytest desde la raíz; acepta args de pytest; reporta claro; regenera informe A11Y si hay marca a11y. No sustituye los tests de arranque.

---

## Criterios de paso / fallo

Paso: pytest verde; arranque OK; Must tocados con evidencia; SEC y arranque activos.

Fallo bloqueante: test rojo; comando ilegal; contrato roto; saltarse arranque.

---

## Cómo añadir tests en una feature nueva

1. ¿Qué requisito SRS cubre?
2. ¿Test nuevo o extensión?
3. ¿SEC? casos legal e ilegal
4. ¿Comando de sistema? contrato + man + inventario
5. ¿Arranque/loader/user? regresión
6. ¿A11Y? marca e informe
7. `poetry run pytest` antes del commit

---

## Evidencias de validación

Test automatizado; salida de arranque; informe A11Y; demo manual; inspección de docs.

---

## Relación con la metodología

No merge a main con tests rojos. La IA propone tests con el código. El humano valida en máquina real. update/backup no eximen de verificar.

---

## Limitaciones actuales

No exige todavía: cobertura mínima obligatoria, CI de forge, rendimiento, E2E de todos los interactivos, laboratorio de lectores. Sí batería local bloqueante.

---

## Ampliación normativa 1.2 (producto 0.2.7 / árbol 0.2.8)

Este apartado no debilita el arranque bloqueante ni SEC.

### Ficheros de tests añadidos al árbol

| Nivel 1 | Nivel 2 | Función |
|---------|---------|---------|
| tests/ | test_security_minimoslib.py | mini-moslib acotado |
| tests/ | test_cmd_loader_apps.py | Carga de apps |
| tests/ | test_cmd_loader_prefixes.py | Prefijos id_cmd |
| tests/ | test_apps.py | Ciclo install/list/remove |
| tests/ | test_tasks.py | Tareas y reencolado |
| tests/ | test_ia_router.py | Off por defecto y fachada |
| tests/ | test_ia_router_remotos.py | Grok / OpenRouter |
| tests/ | test_ia_keys.py | Almacén y no claro |
| tests/ | test_man_command.py | Comando man |
| tests/ | test_a11y_baseline.py | Marca a11y |

### Casos añadidos

| Caso | Resultado esperado |
|------|--------------------|
| minimoslib fuera de app_dir | rechazado |
| minimoslib con app_dir de esa app | permitido según SEC |
| iarouter enabled=false | cero HTTP |
| clave en claro en ia_keys.json | fallo de test |

---

## Autoridad

Este documento es normativo para la estrategia de verificación.

Cualquier cambio que debilite el arranque bloqueante o la validación de seguridad debe actualizar primero SEC, SRS y este documento TEST.

Cualquier cambio que debilite A11Y debe actualizar A11Y, SRS y este documento.
