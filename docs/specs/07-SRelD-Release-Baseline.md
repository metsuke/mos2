# 07 – SRelD · Baseline de release

**Versión del documento:** 1.2  
**Baseline descrita:** v0.2.1 (congelada) + producto actual v0.2.7 (árbol hacia v0.2.8)  
**Estado:** Normativo de referencia  
**Documentos relacionados:** docs/specs/00-OVERVIEW.md, docs/specs/01-SSS-System-Specification.md, docs/METHODOLOGY.md, docs/ENVIRONMENTS.md, docs/VERSIONING.md, CHANGELOG.md

---

## Propósito
Este documento congela y describe la baseline de producto **v0.2.1** y registra evoluciones controladas posteriores hasta **v0.2.7**.

Sirve para:

- saber qué contiene exactamente la versión de referencia
- comparar releases futuras sin ambigüedad
- evitar regresiones respecto a capacidades ya aceptadas

La v1.1 no se borra: v0.2.1 sigue siendo la referencia histórica.

---

## Identificación
| Campo | v0.2.1 | v0.2.7 |
|-------|--------|--------|
| Nombre | MetsuOS / MOS2 | MetsuOS / MOS2 |
| Tag | v0.2.1 | v0.2.7 (Poetry) |
| Tipo | Alpha funcional | Alpha funcional |
| Licencia | GPL-3.0 | GPL-3.0 |
| Python mínimo | 3.10 | 3.10 |
| Hacia | — | v0.2.8 (entrada CHANGELOG; tag producto pendiente de pruebas humanas) |

---

## Capacidades incluidas en v0.2.1
### Núcleo

| Capacidad | Estado en baseline |
|-----------|--------------------|
| Shell interactivo MOSh | Incluida |
| Carga dinámica de comandos | Incluida |
| Hot-reload por mtime | Incluida |
| Seguridad de imports por AST | Incluida |
| Validación de seguridad en runtime | Incluida |
| Tests de arranque bloqueantes | Incluida |
| Espacio de usuario por usuario anfitrión | Incluida |
| Migración automática de home legacy | Incluida |

### Comandos de sistema (v0.2.1)

| Comando | Estado en baseline |
|---------|--------------------|
| help | Incluido |
| version | Incluido |
| sysinfo | Incluido |
| uptime | Incluido |
| echo | Incluido |
| clear | Incluido |
| test | Incluido |
| update | Incluido |
| exit | Incluido (builtin del shell) |

### Comandos de usuario

| Capacidad | Estado en baseline |
|-----------|--------------------|
| Archivos user_*.py | Incluida |
| Invocación con prefijo user_ | Incluida |
| Invocación corta sin conflicto | Incluida |
| Rechazo por imports ilegales | Incluida |

### Actualización (v0.2.1)

| Capacidad | Estado en baseline |
|-----------|--------------------|
| update desde origin/main | Incluida |
| backup local automático | Incluida |
| poda de ramas backup | Incluida |
| mos2_forced_update.sh de emergencia | Incluido |


---

## Estructura de producto de v0.2.1
| Nivel 1 | Nivel 2 | Nivel 3 | Incluido |
|---------|---------|---------|----------|
| moslib/ | core/ | shell.py | Sí |
| moslib/ | core/ | cmd_loader.py | Sí |
| moslib/ | core/ | user.py | Sí |
| moslib/ | core/ | security.py | Sí |
| moslib/ | commands/ | clear.py help.py echo.py | Sí |
| moslib/ | commands/ | sysinfo.py test.py update.py | Sí |
| moslib/ | commands/ | uptime.py version.py | Sí |
| rootfs/ | bin/ | mos.py | Sí |
| rootfs/ | home/ | .gitignore | Sí |
| tests/ | | test_*.py | Sí |
| install.sh / mos2.sh / pyproject.toml | | | Sí |

---

## Dependencias
| Dependencia | Alcance | Notas |
|-------------|---------|-------|
| Python ^3.10 | runtime | Obligatorio |
| pytest | producto | Disponible también en instalación normal |
| pytest-cov | producto | Disponible; cobertura formal no aún obligatoria |
| Poetry | desarrollo/instalación | Gestión de entorno y deps |

No forman parte del modelo de comandos las dependencias arbitrarias de terceros.

---

## Verificación asociada a v0.2.1
1. la batería de tests pasa
2. el arranque de MOSh pasa los tests de arranque
3. los comandos de sistema de esa baseline están disponibles
4. un comando de usuario con import ilegal es rechazado
5. un comando ilegal presente en el usuario actual bloquea arranque
6. `update` puede sincronizar con origin/main preservando cambios locales en backup

---

## Limitaciones conocidas de v0.2.1
1. Fase Alpha: no es un sistema operativo completo.
2. No hay empaquetado multi-repo de usuario todavía operativo.
3. No hay CI externa obligatoria.
4. No hay métrica mínima obligatoria de cobertura.
5. El manual formal y el comando `man` se consolidan como evolución inmediata sobre esta baseline.
6. help puede requerir alineación continua con el loader y los comandos de usuario.

---

## Evolución posterior (resumen)
| Elemento | Destino |
|----------|---------|
| man, USER_MANUAL, ENVIRONMENTS, A11Y, docs, synccheck | Post-0.2.1 hasta 0.2.5 |
| Poetry portable en mos2.sh / install.sh | v0.2.2 |
| Apps, tareas, iarouter, red, update reiniciar | v0.2.7 / árbol hacia v0.2.8 |
| Specs 08, 09, 10 | v0.2.7 |

---

## Producto actual v0.2.7
Además de v0.2.1 y de la evolución 0.2.2–0.2.5, el árbol incluye:

| Capacidad | Estado |
|-----------|--------|
| moslib/core/apps.py + comando apps | Incluida |
| moslib/core/tasks.py + tareas / hilos | Incluida |
| moslib/core/ia_router.py + comando iarouter | Incluida (off por defecto) |
| comando red | Incluida (no es P2P) |
| update reiniciar | Incluida |
| minimoslib / app_dir | Incluida |
| Prioridad sistema > app sistema > app usuario > user_ | Incluida |


---

## Tags y referencias
| Referencia | Uso |
|------------|-----|
| v0.2.1 | Baseline funcional histórica |
| v0.2.0-alpha-user-space | Baseline previa de espacio de usuario |
| v0.2.2 | Poetry portable + ENVIRONMENTS |
| v0.2.5 | A11Y + docs + synccheck (cierre de esa campaña) |
| v0.2.7 | Poetry actual; apps, tareas, iarouter, red |
| v0.2.8 | Prevista en CHANGELOG; tag de producto pendiente de pruebas humanas |
| main | Línea activa de integración |

Detalle de relato: `CHANGELOG.md`. Tags y bump: `docs/VERSIONING.md`.

Esta campaña de sync docs **no** hace bump de Poetry ni tag de producto.

---

## Criterio de no regresión
Se considerará regresión cualquier pérdida de:

1. arranque bloqueante por tests
2. seguridad de imports
3. espacio de usuario por usuario anfitrión
4. resolución de comandos de usuario sin pisar sistema
5. comando update con backup
6. disponibilidad de pytest en el producto
7. resolución portable de Poetry (desde v0.2.2)
8. a11y / docs / declaración (desde v0.2.5)
9. apps / tareas / iarouter off por defecto / red (desde v0.2.7)

---

## Autoridad
Este SRelD fija el significado de la baseline v0.2.1 y el registro de evoluciones posteriores.

Las releases futuras deben declarar qué mantienen, qué añaden y qué cambian respecto a esta referencia.