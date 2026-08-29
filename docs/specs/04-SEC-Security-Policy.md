# 04 – SEC · Política de seguridad

**Versión del documento:** 1.1  
**Baseline de referencia:** v0.2.4  
**Estado:** Normativo  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/03-ICD-Interfaces-and-Command-Contract.md, docs/A11Y.md, docs/a11y/DECLARACION.md, docs/STYLE_GUIDE.md

---

## Propósito

Este documento define la política de seguridad de MetsuOS relativa a la carga y ejecución de comandos.

La seguridad aquí no pretende cubrir todo el espectro de ciberseguridad de un sistema operativo real. Se centra en una norma férrea del producto:

> Ningún comando puede importar código fuera de la biblioteca estándar de Python y de moslib.

---

## Alcance

Aplica a:

| Ámbito | ¿Aplica? | Notas |
|--------|----------|-------|
| Comandos de sistema en moslib/commands/ | Sí | Validación obligatoria |
| Comandos de usuario en rootfs/home/<usuario>/.mos/commands/ | Sí | Validación obligatoria |
| Módulos de moslib/core/ | Sí, como código de confianza del producto | Sujetos a estilo y revisión |
| tests/ | Parcial | Pueden importar pytest y utilidades de test |
| Scripts de instalación del anfitrión | Fuera de esta política de comandos | Se gestionan aparte |

---

## Objetivos de seguridad

1. Impedir que un comando cargue dependencias Python arbitrarias.
2. Mantener el modelo de extensión bajo control de mosLib.
3. Detectar violaciones antes de ejecutar el comando.
4. Detectar violaciones existentes en el arranque del sistema.
5. Dar mensajes de rechazo claros, auditables y usables (prefijo estable y pista de acción).

---

## Relación con accesibilidad

La accesibilidad de interfaz es mandatoria (`docs/A11Y.md`, SSS).

Si un control de esta política y un perfil A11Y soportado chocan:

1. No se excluye el perfil.
2. No se desactiva la validación AST ni se permite un import ilegal “por A11Y”.
3. Se busca una mitigación que conserve el control (mensaje más claro, mismo rechazo).
4. Si aun así hay que recortar SEC, el recorte se escribe aquí, en A11Y y en SRelD. Nunca en silencio.

### Excepciones A11Y vigentes

Ninguna. Rechazar imports ilegales no impide usar teclado ni lector de terminal. El mensaje `[SEGURIDAD]` debe ser texto lineal comprensible.

---

## Política de imports

### Permitido

Un comando puede importar únicamente:

1. Módulos de la biblioteca estándar de Python
2. El paquete `moslib` y sus submódulos

Ejemplos permitidos:

- import os
- import sys
- from pathlib import Path
- import moslib
- from moslib.core.user import get_username

### Prohibido

Está prohibido:

1. Importar cualquier paquete de terceros no estándar
2. Usar imports relativos en comandos (`from . import ...`, `from ..x import ...`)
3. Eludir la validación cargando código dinámico no autorizado
4. Usar `eval` o `exec` sobre entrada externa o para cargar lógica arbitraria

Ejemplos prohibidos:

- import requests
- import numpy
- from flask import Flask
- from . import utils

### Criterio de decisión

La validación se basa en análisis estático del código fuente mediante AST, sin ejecutar el comando.

Para un nombre de módulo:

- se toma el segmento de primer nivel
- si pertenece a la stdlib → permitido
- si es `moslib` o empieza por `moslib.` → permitido
- en cualquier otro caso → prohibido

---

## Momentos de validación

### Validación en runtime (carga de comando)

Cada vez que el sistema va a cargar un comando, debe validar el archivo antes de ejecutarlo.

Si la validación falla:

1. El comando no se carga
2. Se muestra un rechazo explícito con prefijo `[SEGURIDAD]`
3. Se listan los errores detectados
4. El shell no ejecuta `execute()`

### Validación en arranque

Al iniciar MOSh, la batería de tests debe incluir comprobaciones de seguridad sobre:

- todos los comandos de sistema
- todos los comandos del usuario actual

Si cualquier comando existente viola la política, el arranque debe fallar y el sistema no iniciará la sesión interactiva.

### Relación entre ambas

| Momento | Qué cubre | Efecto si falla |
|---------|-----------|-----------------|
| Runtime | El comando concreto que se intenta usar | Rechazo de ese comando |
| Arranque | Inventario actual de comandos sistema + usuario actual | Bloqueo total de arranque |

Ambas capas son obligatorias. Una no sustituye a la otra.

---

## Comportamiento de rechazo

Mensaje mínimo esperado en runtime:

```text
[SEGURIDAD] Comando '<nombre>' rechazado:
  - Import prohibido: import <modulo>
```

El texto debe indicar qué ha pasado. No debe basarse solo en color ANSI.

Después, el shell puede indicar que el comando no está disponible o no fue encontrado.

El rechazo debe ser determinista: el mismo archivo ilegal produce el mismo resultado.

---

## Responsabilidades por componente

| Nivel 1 | Nivel 2 | Nivel 3 | Responsabilidad de seguridad |
|---------|---------|---------|------------------------------|
| moslib/ | core/ | security.py | Análisis AST y API de validación |
| moslib/ | core/ | cmd_loader.py | Invocar validación antes de cargar |
| moslib/ | core/ | shell.py | Ejecutar tests de arranque y bloquear si fallan |
| tests/ | | test_security.py | Casos unitarios de política |
| tests/ | | test_all_commands_security.py | Inventario real de comandos |
| moslib/ | commands/ | * | Cumplir la política en su código fuente |

---

## Espacio de usuario y confianza

El espacio de usuario es controlado por el propio usuario del sistema anfitrión.

Por tanto:

- no se considera código de confianza del producto
- siempre se valida
- puede impedir el arranque local si contiene comandos ilegales

Esto es intencional: protege el modelo de seguridad del sistema frente a extensiones inseguras del propio usuario.

---

## Límites de esta política

Esta política NO cubre por sí sola:

1. Integridad del filesystem del anfitrión
2. Secretos del usuario fuera de MetsuOS
3. Ataques con capacidad de modificar `moslib/` sin pasar por el proceso de desarrollo
4. Ejecución de binarios externos invocados por wrappers no contemplados
5. Vulnerabilidades de la stdlib o del intérprete Python
6. Protección de datos personales (RGPD / LOPDGDD): campaña futura, no este documento

Su alcance es el control de extensión por comandos dentro del modelo MetsuOS.

---

## Requisitos de seguridad derivados

Los siguientes requisitos son normativos y deben aparecer también en el SRS:

- REQ-SEC-001: Todo comando se valida por AST antes de cargarse
- REQ-SEC-002: Solo se permiten imports de stdlib y moslib
- REQ-SEC-003: Los imports relativos en comandos están prohibidos
- REQ-SEC-004: El rechazo debe mostrar motivo claro
- REQ-SEC-005: El arranque debe fallar si existe cualquier comando ilegal en sistema o en el usuario actual
- REQ-SEC-006: No se permite desactivar la seguridad en modo normal de operación
- REQ-A11Y-002: Conflicto A11Y/SEC documentado; no exclusión de perfil

---

## Verificación

La política se verifica por:

1. Tests unitarios de `security.py`
2. Tests de inventario de comandos
3. Pruebas manuales de rechazo con un comando de usuario ilegal
4. Arranque bloqueado mientras exista el comando ilegal
5. Arranque correcto tras eliminar o corregir el comando ilegal
6. Inspección de que el mensaje de rechazo es texto usable

---

## Cambios de política

Cualquier relajación o ampliación de esta política requiere:

1. Actualización de este documento
2. Actualización de tests
3. Justificación en metodología o release notes de la baseline
4. Revisión de impacto sobre SSS, ICD y A11Y

No se admiten flags ocultos para “saltar seguridad” en operación normal.

---

## Autoridad

`04-SEC` es documento de máxima prioridad técnica junto con las normas no negociables del SSS y la política A11Y.

En caso de conflicto con conveniencia de implementación, prevalece esta política.

En caso de conflicto con un perfil A11Y soportado, se aplica la sección «Relación con accesibilidad» de este mismo documento.