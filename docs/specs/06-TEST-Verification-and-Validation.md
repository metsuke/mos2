# 06 – TEST · Verificación y validación

**Versión del documento:** 1.1  
**Baseline de referencia:** v0.2.4  
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
| tests/ | test_a11y_*.py | Tests marcados a11y (se añaden en Bloque 3) |

---

## Niveles de prueba

### Unitarias

Validan funciones y módulos aislados:

- security.analyze_imports
- user path helpers
- contrato de comandos
- estilo crítico
- generación / lectura del informe A11Y

### Integración ligera

Validan colaboración entre piezas:

- CommandManager + security
- shell startup tests runner
- inventario de comandos reales del workspace
- comando a11y + escritura de informe

### Demostración manual

Se usa cuando el requisito es interactivo:

- prompt y exit
- man <comando>
- docs <ruta>
- a11y
- update con y sin cambios locales
- bloqueo de arranque con un user_*.py ilegal

---

## Tests de arranque

### Comportamiento obligatorio

Al iniciar MOSh:

1. se ejecuta la batería de tests del proyecto
2. si return code != 0, se muestra error claro y accionable
3. el shell interactivo no arranca
4. el proceso termina con código de error

### Qué deben cubrir como mínimo

- seguridad de todos los comandos de sistema
- seguridad de los comandos del usuario actual
- contrato execute/help de comandos de sistema
- humo de usuario/espacio personal
- ausencia de patrones prohibidos críticos

Los tests A11Y, cuando existan, forman parte de la batería habitual. Si esa batería los incluye, el informe A11Y se regenera.

### Mensaje de fallo

Debe indicar:

- que el arranque ha sido bloqueado
- que hay que revisar tests o comandos ilegales
- la vía de diagnóstico (`poetry run pytest`)
- sin basarse solo en color

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

Para cada comando de sistema:

1. existe archivo .py en moslib/commands/
2. define execute callable
3. define help callable
4. help() devuelve str no vacío

Para comandos de usuario:

1. nombre de archivo user_*.py
2. también están sujetos a seguridad de imports
3. no pueden tapar un comando de sistema

---

## Verificación de accesibilidad

Marca pytest: `a11y`.

El comando de sistema `a11y` ejecuta solo esa marca y escribe:

| Nivel 1 | Nivel 2 | Nivel 3 | Función |
|---------|---------|---------|---------|
| docs/ | a11y/ | informe.md | Informe humano |
| docs/ | a11y/ | informe.json | Informe en datos |

Situación de cumplimiento:

| Valor | Criterio alpha |
|-------|----------------|
| plenamente conforme | Tests a11y obligatorios en verde y sin no conformidades abiertas |
| no conforme | Falla un test a11y de requisito obligatorio |
| parcialmente conforme | Tests de requisito pasan o aún no hay ejecución automática; hay excepciones o implantación incompleta |

Fuera de esta baseline (no se testea en laboratorio):

- GUI
- lectores de pantalla de escritorio
- sello WCAG / RD 1112/2018

Sí se testea: existencia de declaración e informe, help no vacío, prefijo de seguridad, comando docs cuando exista.

---

## Comando de sistema `test`

El comando `test` debe:

- lanzar pytest desde la raíz del proyecto
- aceptar argumentos adicionales de pytest si se pasan
- reportar éxito o fracaso de forma clara
- regenerar el informe A11Y si la batería incluye tests marcados a11y

No sustituye los tests de arranque: los complementa para uso explícito dentro del shell.

---

## Criterios de paso / fallo

### Paso

Una entrega se considera verificada cuando:

1. `poetry run pytest` termina en verde
2. el arranque de MOSh pasa los tests de arranque
3. los requisitos Must tocados por el cambio tienen evidencia de verificación
4. no se ha desactivado seguridad ni arranque bloqueante

### Fallo

Es fallo bloqueante:

1. cualquier test rojo de la batería principal
2. existencia de comando ilegal en sistema o usuario actual
3. ruptura del contrato execute/help en un comando de sistema
4. imposibilidad de arrancar por tests y “resolverlo” saltándolos

---

## Cómo añadir tests en una feature nueva

Checklist:

1. ¿Qué requisito SRS cubre este cambio?
2. ¿Hace falta test unitario nuevo o extender uno existente?
3. ¿Afecta seguridad? → cubrir caso legal e ilegal
4. ¿Añade comando de sistema? → contrato + man + inventario
5. ¿Cambia arranque/loader/user? → probar regresión de arranque
6. ¿Afecta A11Y? → marca a11y e informe
7. Ejecutar `poetry run pytest` antes del commit

---

## Evidencias de validación

| Tipo | Ejemplo |
|------|---------|
| Test automatizado | assertions en tests/ |
| Salida de arranque | banner de tests OK / bloqueo |
| Informe A11Y | docs/a11y/informe.md e informe.json |
| Demostración manual | secuencia de comandos y resultado |
| Inspección | presencia de archivos docs/ o estructura de dirs |

Para requisitos Must, preferir test automatizado siempre que sea razonable.

---

## Relación con la metodología

Según docs/METHODOLOGY.md:

- no hay merge a main con tests rojos
- la IA debe proponer tests junto con el código cuando el cambio lo requiera
- el humano valida en máquina real
- update/backup no eximen de verificar después de integrar cambios

---

## Limitaciones actuales

La baseline no exige todavía:

1. cobertura métrica mínima obligatoria de pytest-cov
2. CI externa en un forge
3. tests de rendimiento
4. tests end-to-end completos de todos los comandos interactivos
5. laboratorio de lectores de pantalla

Sí exige una batería local fiable y bloqueante en arranque.

---

## Autoridad

Este documento es normativo para la estrategia de verificación.

Cualquier cambio que debilite el arranque bloqueante o la validación de seguridad debe actualizar primero SEC, SRS y este documento TEST.

Cualquier cambio que debilite A11Y debe actualizar A11Y, SRS y este documento.