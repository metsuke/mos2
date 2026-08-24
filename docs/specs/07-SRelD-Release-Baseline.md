# 07 – SRelD · Baseline de release

**Versión del documento:** 1.0  
**Baseline descrita:** v0.2.1  
**Estado:** Normativo de referencia  
**Documentos relacionados:** docs/specs/00-OVERVIEW.md, docs/specs/01-SSS-System-Specification.md, docs/METHODOLOGY.md

---

## 1. Propósito

Este documento congela y describe la baseline de producto **v0.2.1**.

Sirve para:

- saber qué contiene exactamente esta versión de referencia
- comparar releases futuras sin ambigüedad
- evitar regresiones respecto a capacidades ya aceptadas

---

## 2. Identificación de la baseline

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
- Algunas piezas documentales/funcionales (manual, man, comando `man`) pueden integrarse inmediatamente después como evolución controlada sin reescribir el significado de v0.2.1.

---

## 3. Capacidades incluidas en v0.2.1

### 3.1 Núcleo

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

### 3.2 Comandos de sistema

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

### 3.3 Comandos de usuario

| Capacidad | Estado en baseline |
|-----------|--------------------|
| Archivos user_*.py | Incluida |
| Invocación con prefijo user_ | Incluida |
| Invocación corta sin conflicto | Incluida |
| Rechazo por imports ilegales | Incluida |

### 3.4 Actualización

| Capacidad | Estado en baseline |
|-----------|--------------------|
| update desde origin/main | Incluida |
| backup local automático | Incluida |
| poda de ramas backup | Incluida |
| mos2_forced_update.sh de emergencia | Incluido |

---

## 4. Estructura de producto de la baseline

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

## 5. Dependencias de la baseline

| Dependencia | Alcance | Notas |
|-------------|---------|-------|
| Python ^3.10 | runtime | Obligatorio |
| pytest | producto | Disponible también en instalación normal |
| pytest-cov | producto | Disponible; cobertura formal no aún obligatoria |
| Poetry | desarrollo/instalación | Gestión de entorno y deps |

No forman parte del modelo de comandos las dependencias arbitrarias de terceros.

---

## 6. Verificación asociada a la baseline

La baseline se considera coherente cuando:

1. `poetry run pytest` pasa
2. el arranque de MOSh pasa los tests de arranque
3. los comandos de sistema de la tabla 3.2 están disponibles
4. un comando de usuario con import ilegal es rechazado
5. un comando ilegal presente en el usuario actual bloquea arranque
6. `update` puede sincronizar con origin/main preservando cambios locales en backup

---

## 7. Limitaciones conocidas de v0.2.1

1. Fase Alpha: no es un sistema operativo completo.
2. No hay empaquetado multi-repo de usuario todavía operativo.
3. No hay CI externa obligatoria.
4. No hay métrica mínima obligatoria de cobertura.
5. El manual formal y el comando `man` se consolidan como evolución documental/funcional inmediata sobre esta baseline.
6. help puede requerir alineación continua con el loader y los comandos de usuario según evolucione la documentación.

---

## 8. Tags y referencias

| Referencia | Uso |
|------------|-----|
| v0.2.1 | Baseline funcional principal |
| v0.2.0-alpha-user-space | Baseline previa de espacio de usuario |
| main | Línea activa de integración |

---

## 9. Evolución posterior a esta baseline

Los siguientes elementos se tratan como continuación controlada del marco de calidad y documentación:

| Elemento | Tipo | Destino |
|----------|------|---------|
| docs/METHODOLOGY.md | proceso | Obligatorio |
| docs/STYLE_GUIDE.md | calidad | Obligatorio |
| docs/specs/* | ECSS-light | Obligatorio |
| docs/USER_MANUAL.md | usuario | Obligatorio |
| docs/man/* | ayuda extendida | Obligatorio |
| moslib/commands/man.py | comando | Obligatorio en la fase documental/funcional en curso |
| tests de estilo | calidad | Obligatorio |

Cuando esta evolución se integre en main, la siguiente baseline de release deberá actualizar este SRelD o crear una entrada de versión nueva.

---

## 10. Criterio de no regresión respecto a v0.2.1

Se considerará regresión respecto a esta baseline cualquier pérdida de:

1. arranque bloqueante por tests
2. seguridad de imports
3. espacio de usuario por usuario anfitrión
4. resolución de comandos de usuario sin pisar sistema
5. comando update con backup
6. disponibilidad de pytest en el producto

---

## 11. Autoridad

Este SRelD fija el significado de la baseline v0.2.1.

Las releases futuras deben declarar qué mantienen, qué añaden y qué cambian respecto a esta referencia.