# Guía de estilo de programación de MetsuOS (MOS2)

**Versión del documento:** 1.0  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo  
**Documento relacionado:** docs/METHODOLOGY.md

---

## 1. Propósito

Esta guía unifica la forma de escribir código en MetsuOS.

Objetivos:

- Código legible y predecible.
- Mismo estilo en núcleo (`moslib/core`) y comandos (`moslib/commands`).
- Compatibilidad con las normas férreas del sistema (seguridad, contrato de comandos, mosLib).
- Validación automática mediante tests.

Si el código contradice esta guía, se corrige el código o se actualiza esta guía de forma explícita.

---

## 2. Alcance

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

## 3. Principios generales

1. Claridad antes que cleverness.
2. Una responsabilidad por función/módulo.
3. Fallar de forma explícita y con mensaje útil.
4. No romper interfaces públicas sin actualizar specs y tests.
5. Todo comando del sistema es un módulo simple con contrato fijo.

---

## 4. Lenguaje y nombres

### 4.1 Idioma

- Identificadores de código (funciones, variables, módulos): **inglés**, `snake_case`.
- Docstrings orientadas a desarrollador: preferible **español** claro y breve.
- Mensajes mostrados al usuario en el shell: **español**.
- Nombres de comandos de sistema: **inglés** corto (`help`, `update`, `version`).
- Comandos de usuario: archivo `user_<nombre>.py`.

### 4.2 Naming

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

## 5. Imports

### 5.1 Regla de seguridad (obligatoria en comandos)

Solo se permiten:

- Biblioteca estándar de Python
- `moslib` y submódulos

Cualquier otro import está prohibido y debe ser rechazado por la validación AST.

### 5.2 Orden de imports

1. `__future__` si aplica
2. Stdlib
3. `moslib...`
4. Línea en blanco entre grupos si mejora legibilidad

Ejemplo:

from __future__ import annotations

import os
import sys
from pathlib import Path

from moslib.core.security import validate_command_file

### 5.3 Prohibido

- Imports de terceros en comandos y en código de ejecución de comandos
- `from module import *`
- Imports relativos en comandos de usuario (`from . import ...`)

---

## 6. Tipado

- Anotar firmas de funciones públicas.
- Usar `pathlib.Path` para rutas.
- Preferir `str | Path` cuando se acepten ambos.
- Se permite `from __future__ import annotations`.

Ejemplo:

def validate_command_file(file_path: str | Path) -> tuple[bool, list[str]]:
    ...

---

## 7. Docstrings

### 7.1 Módulo

Todo módulo de `moslib/core` y `moslib/commands` debe tener docstring de módulo describiendo su propósito.

### 7.2 Funciones públicas

Toda función pública relevante debe tener docstring breve:

- Qué hace
- Parámetros importantes (si no son obvios)
- Valor de retorno (si aplica)

### 7.3 Comandos

Además del docstring de módulo, todo comando debe implementar:

def help() -> str:
    ...

que devuelve el texto de ayuda de usuario.

---

## 8. Contrato de comandos (obligatorio)

Todo comando de sistema y de usuario debe exponer:

def execute(args):
    ...

def help():
    return "..."

Reglas:

- `execute` recibe una lista de argumentos ya partidos (`args`).
- `help()` devuelve `str`.
- No requiere registrar el comando en ningún índice manual: el cargador descubre archivos `.py`.
- Los comandos de usuario viven en archivos `user_*.py`.
- Un comando de usuario nunca puede sobrescribir un comando de sistema.

---

## 9. Rutas y ficheros

- Usar `pathlib.Path` en lugar de concatenar strings a mano.
- Resolver la raíz del proyecto de forma relativa al archivo actual cuando sea necesario.
- No asumir un cwd concreto salvo que el diseño lo documente.
- El espacio de usuario está en:

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Descripción |
|---------|---------|---------|---------|-------------|
| rootfs/ | home/ | `<usuario>/` | .mos/ | Espacio personal |

---

## 10. Errores y salida

- Mensajes de error comprensibles en español.
- Prefijos útiles cuando ayuden: `[SEGURIDAD]`, `[MetsuOS]`, `[update]`.
- No silenciar excepciones genéricas sin dejar rastro.
- En comandos, si una operación crítica falla, informar y salir con código distinto de cero cuando corresponda (`sys.exit`).

---

## 11. Seguridad de código

Prohibido en comandos y en rutas de ejecución de comandos:

- `eval(...)`
- `exec(...)`
- Ejecutar código arbitrario recibido del usuario
- Cargar módulos fuera de la política de imports
- Bypass de la validación de seguridad

La validación AST de imports es parte del sistema, no un adorno opcional.

---

## 12. Estructura recomendada de un comando

Orden típico de un archivo en `moslib/commands/`:

1. Docstring de módulo
2. Imports
3. Helpers privados (`_...`) si hacen falta
4. `execute(args)`
5. `help()`

Ejemplo mínimo:

def execute(args):
    print("hola")

def help():
    return "Uso: hola - Saluda"

---

## 13. Estructura recomendada de un módulo core

1. Docstring de módulo
2. Imports
3. Constantes
4. Funciones/clases públicas
5. Helpers privados

Las clases públicas (`CommandManager`, `MOSh`) mantienen métodos claros y responsabilidades limitadas.

---

## 14. Tests

- Todo cambio de comportamiento relevante lleva test.
- Los tests viven en `tests/` con nombres `test_*.py`.
- Se prueban al menos:
  - seguridad de imports
  - contrato de comandos
  - loader
  - usuario / espacio personal
  - estilo crítico
- El arranque de MOSh ejecuta la batería; si falla, no inicia el sistema.

Estilo en tests:

- Nombres de test descriptivos: `test_user_command_with_forbidden_import_is_rejected`
- Asserts claros
- Sin dependencias de red

---

## 15. Comentarios

- Comentar el porqué, no el qué obvio.
- Evitar comentarios decorativos o ruido.
- Si un bloque es complejo, explicar la intención en una o dos líneas.

---

## 16. Formato

- Indentación: 4 espacios.
- Evitar líneas extremadamente largas; priorizar legibilidad.
- Una sentencia lógica por línea en general.
- Mantener funciones razonablemente cortas.

No se impone un formateador automático obligatorio en esta baseline, pero el estilo manual debe ser consistente con esta guía. La validación crítica se hace por tests.

---

## 17. Validación automática de esta guía

Deben existir tests que comprueben, como mínimo:

1. Todo comando de sistema tiene `execute` y `help` callables.
2. `help()` de comandos de sistema devuelve `str`.
3. Los módulos core principales tienen docstring de módulo.
4. No aparecen patrones prohibidos graves (`eval`/`exec`) en comandos/core según la política definida.
5. La seguridad de imports sigue activa.

Si estos tests fallan, el cambio no es aceptable para `main`.

---

## 18. Excepciones

Cualquier excepción a esta guía debe:

1. Estar justificada.
2. Documentarse.
3. Actualizar esta guía o la spec correspondiente si deja de ser excepción puntual.

No existen excepciones silenciosas.

---

## 19. Checklist rápido antes de commit

1. ¿Imports legales?
2. ¿Contrato execute/help si es comando?
3. ¿Nombres y docstrings coherentes?
4. ¿Mensajes de usuario en español?
5. ¿Tests actualizados/pasan?
6. ¿He tocado una norma férrea sin actualizar specs?

Si algo falla, no se considera terminado.,0