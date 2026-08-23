# 02 – SRS · Requisitos software

**Versión del documento:** 1.0  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/03-ICD-Interfaces-and-Command-Contract.md, docs/specs/04-SEC-Security-Policy.md, docs/specs/06-TEST-Verification-and-Validation.md

---

## 1. Propósito

Este documento enumera los requisitos software de MetsuOS de forma numerada y verificable.

Cada requisito tiene:

- identificador
- enunciado normativo
- prioridad
- método de verificación

---

## 2. Convenciones

### 2.1 Identificadores

Formato: REQ-<AREA>-<NNN>

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
| PLAT | Plataforma |

### 2.2 Prioridad

| Prioridad | Significado |
|-----------|-------------|
| Must | Obligatorio en la baseline |
| Should | Altamente deseable |
| May | Opcional |

### 2.3 Verificación

| Método | Significado |
|--------|-------------|
| Test | Automatizado por pytest u otro test |
| Demo | Demostración manual |
| Inspection | Revisión de código o documentación |

---

## 3. Requisitos de sistema y shell

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-SYS-001 | MOSh debe proporcionar un bucle interactivo de lectura y ejecución de comandos | Must | Demo / Test |
| REQ-SYS-002 | El prompt debe incluir el nombre de usuario del sistema anfitrión | Must | Demo |
| REQ-SYS-003 | El comando `exit` debe terminar la sesión interactiva | Must | Demo |
| REQ-SYS-004 | Una línea vacía no debe provocar error | Must | Demo |
| REQ-SYS-005 | Un comando inexistente debe producir un mensaje de error claro | Must | Demo |
| REQ-SYS-006 | La lógica de negocio del shell debe residir en moslib, no en scripts auxiliares del anfitrión | Must | Inspection |
| REQ-SYS-007 | El punto de entrada rootfs/bin/mos.py debe limitarse a arrancar el shell | Must | Inspection |

---

## 4. Requisitos de comandos

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-CMD-001 | Todo comando debe exponer `execute(args)` callable | Must | Test |
| REQ-CMD-002 | Todo comando debe exponer `help()` callable | Must | Test |
| REQ-CMD-003 | `help()` debe devolver un `str` no vacío | Must | Test |
| REQ-CMD-004 | Los comandos de sistema deben vivir en moslib/commands/ | Must | Inspection |
| REQ-CMD-005 | El nombre de un comando de sistema debe coincidir con el nombre de archivo sin .py | Must | Inspection / Test |
| REQ-CMD-006 | Los comandos deben poder descubrirse sin registro manual centralizado | Must | Demo / Test |
| REQ-CMD-007 | El sistema debe soportar hot-reload basado en cambio de archivo cuando el loader lo recargue | Should | Demo |
| REQ-CMD-008 | La baseline debe incluir al menos: help, version, sysinfo, uptime, echo, clear, test, update | Must | Inspection / Demo |
| REQ-CMD-009 | El sistema debe proporcionar un comando `man` para mostrar documentación extendida desde docs/man/ | Must | Demo / Test |
| REQ-CMD-010 | Un comando de usuario no puede sobrescribir un comando de sistema | Must | Test |

---

## 5. Requisitos de resolución de nombres

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-CMD-011 | Si existe comando de sistema con el nombre solicitado, debe usarse ese | Must | Test |
| REQ-CMD-012 | Si se solicita `user_<nombre>` y existe el archivo correspondiente de usuario, debe usarse ese | Must | Test |
| REQ-CMD-013 | Si se solicita `<nombre>` y no existe comando de sistema, puede resolverse a `user_<nombre>` | Must | Test |
| REQ-CMD-014 | La resolución de nombre corto de usuario nunca tiene prioridad sobre un comando de sistema | Must | Test |

---

## 6. Requisitos de espacio de usuario

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-USER-001 | El sistema debe resolver el usuario real del sistema anfitrión | Must | Test |
| REQ-USER-002 | El espacio personal debe ubicarse en rootfs/home/<usuario>/.mos/ | Must | Test / Inspection |
| REQ-USER-003 | ensure_user_space debe crear commands, data, config, packages y repos si no existen | Must | Test |
| REQ-USER-004 | Los comandos de usuario deben residir en rootfs/home/<usuario>/.mos/commands/ | Must | Inspection |
| REQ-USER-005 | Los archivos de comando de usuario deben nombrarse user_*.py | Must | Test / Inspection |
| REQ-USER-006 | El contenido de rootfs/home/ no debe versionarse como producto | Must | Inspection |
| REQ-USER-007 | Si existe home legacy y no existe el nuevo, el sistema debe migrar automáticamente | Must | Demo / Test |
| REQ-USER-008 | El espacio de usuario debe crearse en el arranque del shell si falta | Must | Demo / Test |

---

## 7. Requisitos de seguridad

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-SEC-001 | Todo comando debe validarse por AST antes de cargarse en operación normal | Must | Test |
| REQ-SEC-002 | Solo se permiten imports de la biblioteca estándar y de moslib | Must | Test |
| REQ-SEC-003 | Los imports relativos en comandos están prohibidos | Must | Test |
| REQ-SEC-004 | Un comando ilegal debe rechazarse con mensaje `[SEGURIDAD]` y motivo | Must | Test / Demo |
| REQ-SEC-005 | El arranque debe validar todos los comandos de sistema y los del usuario actual | Must | Test / Demo |
| REQ-SEC-006 | Si existe cualquier comando ilegal en ese inventario, el sistema no debe iniciar la sesión interactiva | Must | Demo / Test |
| REQ-SEC-007 | No debe existir un modo normal de operación con la seguridad desactivada | Must | Inspection |
| REQ-SEC-008 | Está prohibido usar eval/exec en core y comandos según la política de estilo/seguridad | Must | Test |

---

## 8. Requisitos de arranque

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-BOOT-001 | El arranque debe ejecutar la batería de tests del proyecto | Must | Demo / Test |
| REQ-BOOT-002 | Si los tests de arranque fallan, el proceso debe terminar sin abrir el shell interactivo | Must | Demo |
| REQ-BOOT-003 | El mensaje de fallo de arranque debe ser claro y orientar a `poetry run pytest` o revisión de comandos ilegales | Must | Demo |
| REQ-BOOT-004 | Si los tests pasan, el shell debe mostrar usuario y ruta del espacio personal | Must | Demo |

---

## 9. Requisitos de pruebas

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-TEST-001 | El proyecto debe disponer de tests automatizados en tests/ | Must | Inspection |
| REQ-TEST-002 | Debe existir cobertura de seguridad de imports | Must | Test |
| REQ-TEST-003 | Debe existir cobertura del loader de comandos | Must | Test |
| REQ-TEST-004 | Debe existir cobertura del módulo de usuario | Must | Test |
| REQ-TEST-005 | Debe existir cobertura del contrato execute/help de comandos de sistema | Must | Test |
| REQ-TEST-006 | Debe existir un comando de sistema `test` que lance la batería | Must | Demo |
| REQ-TEST-007 | pytest debe estar disponible en la instalación normal del producto | Must | Inspection / Demo |

---

## 10. Requisitos de actualización

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-UPD-001 | Debe existir un comando `update` para sincronizar con origin/main | Must | Demo |
| REQ-UPD-002 | Si hay cambios locales pendientes, update debe preservarlos en una rama backup/YYYYMMDD_HHMMSS | Must | Demo |
| REQ-UPD-003 | update debe forzar la sincronización de main con origin/main | Must | Demo |
| REQ-UPD-004 | update debe mantener un número máximo controlado de ramas backup locales | Must | Demo / Inspection |
| REQ-UPD-005 | Las ramas backup no se consideran artefactos de publicación del producto | Must | Inspection |

---

## 11. Requisitos de documentación

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-DOC-001 | Debe existir docs/METHODOLOGY.md | Must | Inspection |
| REQ-DOC-002 | Debe existir docs/STYLE_GUIDE.md | Must | Inspection |
| REQ-DOC-003 | Debe existir el set ECSS-light en docs/specs/ | Must | Inspection |
| REQ-DOC-004 | Debe existir un manual de usuario formal en docs/USER_MANUAL.md | Must | Inspection |
| REQ-DOC-005 | Debe existir una página man por comando de sistema en docs/man/ | Must | Inspection |
| REQ-DOC-006 | Las estructuras de directorios en documentación normativa deben representarse como tablas por niveles | Must | Inspection |
| REQ-DOC-007 | Todo comando de sistema nuevo debe documentarse en man en el mismo cambio o en el inmediato de la misma fase | Should | Inspection |

---

## 12. Requisitos de plataforma

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-PLAT-001 | El sistema debe poder ejecutarse con Python 3.10 o superior | Must | Demo |
| REQ-PLAT-002 | El sistema no debe depender de una única distribución Linux | Must | Inspection / Demo |
| REQ-PLAT-003 | La instalación y lanzamiento deben contemplar entornos Linux, macOS y Windows/Git Bash | Must | Demo |
| REQ-PLAT-004 | El arranque básico no debe requerir red | Must | Demo |

---

## 13. Requisitos de estilo y mantenibilidad

| ID | Requisito | Prioridad | Verificación |
|----|-----------|-----------|--------------|
| REQ-SYS-008 | El código de core y comandos debe cumplir docs/STYLE_GUIDE.md en las normas verificables por tests | Must | Test |
| REQ-SYS-009 | Los módulos core obligatorios deben tener docstring de módulo | Must | Test |
| REQ-SYS-010 | Los identificadores de código deben usar convenciones snake_case/PascalCase según STYLE_GUIDE | Should | Inspection |
| REQ-SYS-011 | Los mensajes de usuario del shell y comandos deben estar en español | Must | Inspection / Demo |

---

## 14. Trazabilidad mínima

| Spec de origen | Requisitos principales |
|----------------|------------------------|
| SSS | REQ-SYS-*, REQ-USER-*, REQ-PLAT-*, REQ-CMD-010 |
| SEC | REQ-SEC-* |
| ICD | REQ-CMD-001 a REQ-CMD-014 |
| Metodología / calidad | REQ-BOOT-*, REQ-TEST-*, REQ-DOC-* |
| Operación | REQ-UPD-* |

---

## 15. Autoridad

Este SRS es normativo para la aceptación de cambios software.

Un cambio que viole un requisito Must no puede mergearse a main sin actualizar explícitamente este documento y su justificación.