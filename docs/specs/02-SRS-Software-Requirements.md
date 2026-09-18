# 02 – SRS · Requisitos software

**Versión del documento:** 1.4  
**Baseline de referencia:** v0.2.7 (árbol hacia v0.2.8)  
**Estado:** Normativo  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/A11Y.md, docs/a11y/DECLARACION.md, docs/ENVIRONMENTS.md, docs/specs/03-ICD-Interfaces-and-Command-Contract.md, docs/specs/04-SEC-Security-Policy.md, docs/specs/06-TEST-Verification-and-Validation.md, docs/specs/08-APPS.md, docs/specs/09-TASKS.md, docs/specs/10-IA-ROUTER.md

---

## Propósito
Este documento enumera los requisitos software de MetsuOS de forma numerada y verificable.

Cada requisito tiene:

- identificador
- enunciado normativo
- prioridad
- método de verificación

La v1.2 permanece Must. Esta v1.3 añade áreas APP, TASK, IA y comandos del árbol 0.2.7. No borra ni rebaja los Must anteriores.

---

## Convenciones
### Identificadores

Formato: `REQ-<AREA>-<NNN>`

| Área | Significado |
|------|-------------|
| SYS | Sistema / shell |
| CMD | Comandos |
| USER | Espacio de usuario |
| SEC | Seguridad |
| BOOT | Arranque |
| TEST | Pruebas |
| DOC | Documentación |
| UPD | Actualización |
| PLAT | Plataforma / entornos |
| A11Y | Accesibilidad |
| APP | Apps |
| TASK | Tareas e hilos |
| IA | Enrutador de IA |

### Prioridad

| Prioridad | Significado |
|-----------|-------------|
| Must | Obligatorio en la baseline |
| Should | Altamente deseable |
| May | Opcional |

### Verificación

| Método | Significado |
|--------|-------------|
| Test | Automatizado por pytest u otro test |
| Demo | Demostración manual |
| Inspection | Revisión de código o documentación |


---

## Requisitos de sistema y shell
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de comandos
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de resolución de nombres
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de espacio de usuario
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de seguridad
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de arranque
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de pruebas
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de actualización
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de documentación
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de plataforma
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de estilo y mantenibilidad
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de accesibilidad
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de pruebas A11Y
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de apps
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de tareas
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Requisitos de iarouter
### Sistema / shell

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must |  |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando exit debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must |  |

### Comandos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-CMD-001 | ICD |  |  |
| REQ-CMD-002 | Todo comando debe exponer help() callable | Must | Test |
| REQ-CMD-003 | help() debe devolver un str no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must |  |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must |  |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, man, version, sysinfo, uptime, echo, clear, test, update | Must |  |
| REQ-CMD-009 | El sistema debe proporcionar un comando man para mostrar documentación extendida desde docs/man/ | Must |  |
| REQ-CMD-010 | SSS |  |  |
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita user_nombre y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita nombre y no existe comando de sistema, puede resolverse a user_nombre | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |
| REQ-CMD-015 | Al cerrar la baseline 0.2.5 deben existir los comandos de sistema a11y y docs | Must |  |
| REQ-CMD-016 | Deben existir los comandos de sistema apps, tareas, hilos e iarouter | Must |  |
| REQ-CMD-017 | Debe existir el comando de sistema red (diagnóstico de red del anfitrión; no es P2P) | Must |  |
| REQ-CMD-018 | man debe poder mostrar el man de un comando de app si la app lo aporta | Must | Demo |
| REQ-CMD-019 | Un comando de app no puede sobrescribir un comando de sistema | Must | Test |
| REQ-CMD-020 | La prioridad de resolución debe ser: sistema > app sistema > app usuario > user_ | Must | Test |

### Espacio de usuario

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/usuario/.mos/ | Must |  |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/usuario/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must |  |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must |  |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must |  |
| REQ-USER-009 | El espacio personal debe poder albergar apps de ámbito usuario bajo .mos/apps/ | Must |  |

### Seguridad

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje [SEGURIDAD] y motivo | Must |  |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must |  |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must |  |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |
| REQ-SEC-009 | Un comando de app solo puede importar minimoslib de esa app y solo con app_dir de esa app | Must | Test |

### Arranque

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must |  |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a revisión de tests/comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

### Pruebas

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema test que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must |  |
| REQ-TEST-008 | Debe existir marca pytest a11y para aislar la validación de accesibilidad | Must | Test |
| REQ-TEST-009 | Los tests A11Y forman parte del proceso habitual (desarrollo y producción), no son opcionales de solo CI | Must | Inspection |
| REQ-TEST-010 | Debe existir cobertura de apps, prioridad de nombres y minimoslib | Must | Test |
| REQ-TEST-011 | Debe existir cobertura de tareas e iarouter | Must | Test |

### Documentación

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |
| REQ-DOC-008 | Debe existir docs/ENVIRONMENTS.md con perfiles de entorno y política de Poetry | Must | Inspection |
| REQ-DOC-009 | A11Y |  |  |
| REQ-DOC-010 | Debe existir docs/a11y/DECLARACION.md | Must | Inspection |
| REQ-DOC-011 | Debe existir docs/a11y/informe.md y docs/a11y/informe.json | Must | Inspection |

### Actualización

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando update para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must |  |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |
| REQ-UPD-006 | update debe alinear los tags locales con origin (alta y baja) | Must |  |
| REQ-UPD-007 | Tras update, los módulos ya cargados en la sesión no deben cambiar solos; debe existir update reiniciar o equivalente de salir y relanzar | Must |  |

### Plataforma / entornos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must |  |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar linux/native, macos/native, windows/git-bash y windows/wsl | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |
| REQ-PLAT-005 | Entornos |  |  |
| REQ-PLAT-006 | La documentación de entornos no debe depender de rutas absolutas de un usuario concreto | Must | Inspection |
| REQ-PLAT-007 | Un candidato Poetry solo debe usarse si --version se puede ejecutar | Must |  |

### Apps

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-APP-001 | Una app debe identificarse con app.json (id, nombre, versión, comandos) | Must |  |
| REQ-APP-002 | apps debe permitir list, show, install (ruta o repo git) y remove | Must |  |
| REQ-APP-003 | El ámbito de instalación debe ser usuario o sistema | Must | Test |
| REQ-APP-004 | Los comandos de app deben invocarse por nombre corto, id_cmd o app_id_cmd según el loader | Must | Test |
| REQ-APP-005 | Sin A11Y mínima el comando de app no se acepta ni se ejecuta | Must | Test |

### Tareas e hilos

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-TASK-001 | Debe existir un almacén local de tareas (manuales y automáticas) | Must | Test |
| REQ-TASK-002 | El comando tareas debe listar y gestionar tareas | Must |  |
| REQ-TASK-003 | El comando hilos debe mostrar vista por clase en texto lineal | Must | Demo |
| REQ-TASK-004 | Durante la sesión MOSh puede haber un worker que avance tareas automáticas | Should |  |
| REQ-TASK-005 | Tareas e hilos no son la malla P2P | Must | Inspection |

### Enrutador de IA

| Id | Texto | Prioridad | Verificación |
|----|-------|-----------|--------------|
| REQ-IA-001 | iarouter debe estar apagado por defecto | Must |  |
| REQ-IA-002 | No debe enviar a un modelo hasta usar / preguntar (u operación equivalente implementada) | Must |  |
| REQ-IA-003 | Debe poder detectar y usar proveedores locales Jan y GPT4All | Must |  |
| REQ-IA-004 | Debe poder usar Grok y OpenRouter cuando hay clave | Should | Demo |
| REQ-IA-005 | Las claves no deben listarse en status | Must |  |
| REQ-IA-006 | El puente HTTP de iarouter, si existe, no es P2P | Must | Inspection |

## Trazabilidad mínima
| Spec de origen | Requisitos principales |
|----------------|------------------------|
| SSS | REQ-SYS-*, REQ-USER-*, REQ-PLAT-*, REQ-CMD-010, REQ-CMD-016 a REQ-CMD-020, REQ-A11Y-001 |
| SEC | REQ-SEC-* |
| ICD | REQ-CMD-001 a REQ-CMD-020 |
| A11Y | REQ-A11Y-*, REQ-DOC-009 a REQ-DOC-011, REQ-TEST-008, REQ-TEST-009 |
| Metodología / calidad | REQ-BOOT-*, REQ-TEST-*, REQ-DOC-* |
| Operación | REQ-UPD-* |
| Entornos | REQ-PLAT-005, REQ-PLAT-006, REQ-PLAT-007, REQ-DOC-008 |
| APPS | REQ-APP-* |
| TASKS | REQ-TASK-* |
| IA-ROUTER | REQ-IA-* |

---

## Autoridad
Este SRS es normativo para la aceptación de cambios software.

Un cambio que viole un requisito Must no puede mergearse a main sin actualizar explícitamente este documento y su justificación.