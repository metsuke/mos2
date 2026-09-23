# Guía de estilo de programación de MetsuOS (MOS2)

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.7 / árbol 0.2.8  
**Estado:** Normativo  
**Documento relacionado:** docs/METHODOLOGY.md, docs/AI_ONBOARDING.md

---

## Propósito
Esta guía unifica la forma de escribir código en MetsuOS.

Objetivos:

- Código legible y predecible.
- Mismo estilo en núcleo (`moslib/core`) y comandos (`moslib/commands`).
- Compatibilidad con las normas férreas del sistema (seguridad, contrato de comandos, mosLib).
- Validación automática mediante tests.

Si el código contradice esta guía, se corrige el código o se actualiza esta guía de forma explícita.

---

## Alcance
Aplica a:

| Nivel 1 | Nivel 2 | Nivel 3 | Aplica |
|---------|---------|---------|--------|
| moslib/ | core/ | *.py | Sí |
| moslib/ | commands/ | *.py | Sí |
| rootfs/ | bin/ | mos.py | Sí |
| tests/ | | test_*.py | Sí, con matices de tests |
| docs/ | | | No (es documentación) |

Los comandos de usuario en `rootfs/home/<usuario>/.mos/commands/` también deben respetar el contrato de comando y la política de seguridad de imports. El resto de reglas de estilo se recomiendan, pero la seguridad y el contrato son obligatorios.

---

## Principios generales
1. Claridad antes que cleverness.
2. Una responsabilidad por función/módulo.
3. Fallar de forma explícita y con mensaje útil.
4. No romper interfaces públicas sin actualizar specs y tests.
5. Todo comando del sistema es un módulo simple con contrato fijo.
6. Ningún fichero de código del sistema supera 120 líneas; si lo hace, se parte.

---

## Lenguaje y nombres
### Idioma

- Identificadores de código (funciones, variables, módulos): **inglés**, `snake_case`.
- Docstrings orientadas a desarrollador: preferible **español** claro y breve.
- Mensajes mostrados al usuario en el shell: **español**.
- Nombres de comandos de sistema: **inglés** corto (`help`, `update`, `version`).
- Comandos de usuario: archivo `user_<nombre>.py`.

### Naming

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Módulos / archivos | snake_case | cmd_loader.py |
| Funciones y métodos | snake_case | get_username |
| Funciones internas | _snake_case | _run_startup_tests |
| Constantes | UPPER_SNAKE_CASE | STDLIB_MODULES |
| Clases | PascalCase | CommandManager, MOSh |
| Variables locales | snake_case | project_root |

Nombres descriptivos. Evitar abreviaturas oscuras.

---

## Imports
### Regla de seguridad (obligatoria en comandos)

Solo se permiten:

- Biblioteca estándar de Python
- `moslib` y submódulos

Cualquier otro import está prohibido y debe ser rechazado por la validación AST.

### Orden de imports

1. `__future__` si aplica
2. Stdlib
3. `moslib...`
4. Línea en blanco entre grupos si mejora legibilidad

### Prohibido

- Imports de terceros en comandos y en código de ejecución de comandos
- `from module import *`
- Imports relativos en comandos de usuario (`from . import ...`)

---

## Tipado
- Anotar firmas de funciones públicas.
- Usar `pathlib.Path` para rutas.
- Preferir `str | Path` cuando se acepten ambos.
- Se permite `from __future__ import annotations`.

---

## Docstrings
Todo módulo de `moslib/core` y `moslib/commands` debe tener docstring de módulo.
Toda función pública relevante: qué hace, parámetros no obvios, retorno.
Todo comando implementa `help() -> str`.

---

## Contrato de comandos (obligatorio)
Todo comando de sistema y de usuario debe exponer `execute(args)` y `help() -> str`.

- `execute` recibe argumentos ya partidos.
- El cargador descubre archivos `.py`; no hay índice manual de comandos.
- Usuario: `user_*.py`. Nunca pisa un comando de sistema.
- Helpers de un comando no son comandos: no viven en `commands/` si no tienen execute/help.

---

## Rutas y ficheros
- Usar `pathlib.Path`.
- No asumir un cwd concreto salvo que el diseño lo documente.

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Descripción |
|---------|---------|---------|---------|-------------|
| rootfs/ | home/ | `<usuario>/` | .mos/ | Espacio personal |

---

## Errores y salida
- Mensajes de error en español.
- Prefijos útiles: `[SEGURIDAD]`, `[MetsuOS]`, `[update]`, `[integridad]`, `[multi]`, `[docgen]`.
- No silenciar excepciones genéricas.
- En comandos, fallo crítico: informar y `sys.exit` distinto de cero cuando corresponda.

---

## Seguridad de código
Prohibido en comandos y rutas de ejecución:

- `eval(...)` / `exec(...)`
- Ejecutar código arbitrario recibido del usuario
- Cargar módulos fuera de la política de imports
- Bypass de la validación de seguridad

La validación AST de imports es parte del sistema.

---

## Estructura recomendada de un comando
1. Docstring de módulo
2. Imports
3. Helpers privados (`_...`)
4. `execute(args)`
5. `help()`
6. `sinopsis()` si el man se pinta desde código

Si el archivo supera 120 líneas, partir en submódulos core; el `.py` de `commands/` queda como fachada con execute/help.

---

## Estructura recomendada de un módulo core
1. Docstring de módulo
2. Imports
3. Constantes
4. Funciones/clases públicas
5. Helpers privados

Evitar imports circulares. Fachada corta + mapa/helpers en ficheros hermanos.

---

## Tests
- Todo cambio de comportamiento relevante lleva test.
- Viven en `tests/` como `test_*.py`.
- Arranque de MOSh ejecuta la batería; si falla, no inicia.
- `test 120` lista ficheros por encima del tope; no tumba el sistema.
- Sin dependencias de red. Nombres descriptivos.

---

## Comentarios
- Comentar el porqué, no el qué obvio.
- Evitar ruido.

---

## Formato
- Indentación: 4 espacios.
- Evitar líneas extremadamente largas.
- Una sentencia lógica por línea en general.
- **Tope: 120 líneas por fichero de código del sistema.**

No se impone formateador automático obligatorio en esta baseline. La validación crítica es por tests.

---

## Validación automática de esta guía
Tests mínimos:

1. Todo comando de sistema tiene `execute` y `help` callables.
2. `help()` devuelve `str`.
3. Módulos core principales con docstring.
4. Sin `eval`/`exec` en comandos/core.
5. Seguridad de imports activa.
6. Visibilidad del tope 120 (`test 120`).

Si fallan, el cambio no es aceptable para `main`.

---

## Excepciones
Toda excepción: justificada, documentada, y si deja de ser puntual se actualiza esta guía o la spec. No hay excepciones silenciosas.

---

## Checklist rápido antes de commit
1. ¿Imports legales?
2. ¿Contrato execute/help si es comando?
3. ¿Nombres y docstrings coherentes?
4. ¿Mensajes de usuario en español?
5. ¿Tests actualizados/pasan?
6. ¿He tocado una norma férrea sin actualizar specs?
7. ¿El .py tiene ≤ 120 líneas?
8. ¿Integridad coherente si toqué ficheros del repo?

Si algo falla, no se considera terminado.

---