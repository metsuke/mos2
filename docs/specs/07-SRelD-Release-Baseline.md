# 07 – SRelD · Baseline de release

**Versión del documento:** 1.1  
**Baseline descrita:** v0.2.1 (más evolución posterior documentada)  
**Estado:** Normativo de referencia  
**Documentos relacionados:** docs/specs/00-OVERVIEW.md, docs/specs/01-SSS-System-Specification.md, docs/METHODOLOGY.md, docs/ENVIRONMENTS.md

---

## Propósito

Este documento congela y describe la baseline de producto **v0.2.1** y registra evoluciones controladas posteriores.

Sirve para:

- saber qué contiene exactamente la versión de referencia
- comparar releases futuras sin ambigüedad
- evitar regresiones respecto a capacidades ya aceptadas

---

## Identificación de la baseline

| Campo | Valor |
|-------|-------|
| Nombre de producto | MetsuOS / MOS2 |
| Versión de baseline | 0.2.1 |
| Tag de referencia | v0.2.1 |
| Tipo | Alpha funcional |
| Licencia | GPL-3.0 |
| Python mínimo | 3.10 |

Notas:

- Sobre esta baseline se inicia el marco documental completo en `docs/`.
- Piezas posteriores (man, entornos, Poetry portable) se listan como evolución sin reescribir el significado de v0.2.1.

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

### Comandos de sistema

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

### Actualización

| Capacidad | Estado en baseline |
|-----------|--------------------|
| update desde origin/main | Incluida |
| backup local automático | Incluida |
| poda de ramas backup | Incluida |
| mos2_forced_update.sh de emergencia | Incluido |

---

## Estructura de producto de la baseline

| Nivel 1 | Nivel 2 | Nivel 3 | Incluido en baseline |
|---------|---------|---------|----------------------|
| moslib/ | core/ | shell.py | Sí |
| moslib/ | core/ | cmd_loader.py | Sí |
| moslib/ | core/ | user.py | Sí |
| moslib/ | core/ | security.py | Sí |
| moslib/ | commands/ | clear.py | Sí |
| moslib/ | commands/ | echo.py | Sí |
| moslib/ | commands/ | help.py | Sí |
| moslib/ | commands/ | sysinfo.py | Sí |
| moslib/ | commands/ | test.py | Sí |
| moslib/ | commands/ | update.py | Sí |
| moslib/ | commands/ | uptime.py | Sí |
| moslib/ | commands/ | version.py | Sí |
| rootfs/ | bin/ | mos.py | Sí |
| rootfs/ | home/ | .gitignore | Sí |
| tests/ | | test_*.py | Sí |
| install.sh | | | Sí |
| mos2.sh | | | Sí |
| pyproject.toml | | | Sí |

---

## Dependencias de la baseline

| Dependencia | Alcance | Notas |
|-------------|---------|-------|
| Python ^3.10 | runtime | Obligatorio |
| pytest | producto | Disponible también en instalación normal |
| pytest-cov | producto | Disponible; cobertura formal no aún obligatoria |
| Poetry | desarrollo/instalación | Gestión de entorno y deps |

No forman parte del modelo de comandos las dependencias arbitrarias de terceros.

---

## Verificación asociada a la baseline

La baseline se considera coherente cuando:

1. la batería de tests pasa
2. el arranque de MOSh pasa los tests de arranque
3. los comandos de sistema de la baseline están disponibles
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

## Tags y referencias

| Referencia | Uso |
|------------|-----|
| v0.2.1 | Baseline funcional principal |
| v0.2.0-alpha-user-space | Baseline previa de espacio de usuario |
| v0.2.2 | Prevista: Poetry portable + docs/ENVIRONMENTS (fix de producto) |
| main | Línea activa de integración |

---

## Evolución posterior a esta baseline

| Elemento | Tipo | Destino |
|----------|------|---------|
| docs/METHODOLOGY.md | proceso | Obligatorio |
| docs/STYLE_GUIDE.md | calidad | Obligatorio |
| docs/specs/* | ECSS-light | Obligatorio |
| docs/USER_MANUAL.md | usuario | Obligatorio |
| docs/man/* | ayuda extendida | Obligatorio |
| moslib/commands/man.py | comando | Obligatorio |
| tests de estilo | calidad | Obligatorio |
| docs/ENVIRONMENTS.md | entornos | Obligatorio en evolución post-0.2.1 |
| mos2.sh / install.sh Poetry portable | fix plataforma | Obligatorio en evolución hacia v0.2.2 |
| Contexto de sesión genérico | proceso | Obligatorio (sin datos personales de máquina) |

Cuando la evolución de entornos/Poetry se integre en main con bump de producto, la release **v0.2.2** debe reflejarse en `pyproject.toml` y en este SRelD (o entrada de versión nueva).

---

## Criterio de no regresión respecto a v0.2.1

Se considerará regresión cualquier pérdida de:

1. arranque bloqueante por tests
2. seguridad de imports
3. espacio de usuario por usuario anfitrión
4. resolución de comandos de usuario sin pisar sistema
5. comando update con backup
6. disponibilidad de pytest en el producto

Tras v0.2.2, también: resolución portable de Poetry en lanzador/instalador según perfiles documentados.

---

## Autoridad

Este SRelD fija el significado de la baseline v0.2.1 y el registro de evoluciones posteriores.

Las releases futuras deben declarar qué mantienen, qué añaden y qué cambian respecto a esta referencia.