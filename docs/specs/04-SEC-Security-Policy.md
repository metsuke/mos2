# 04 – SEC · Política de seguridad

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.4 (texto 1.1 conservado); producto v0.2.7 / árbol v0.2.8  
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

### Prohibido

1. Importar cualquier paquete de terceros no estándar
2. Usar imports relativos en comandos
3. Eludir la validación cargando código dinámico no autorizado
4. Usar `eval` o `exec` sobre entrada externa o para cargar lógica arbitraria

Criterio: AST, primer segmento stdlib o moslib → permitido; resto → prohibido.

---

## Momentos de validación

Runtime: validar antes de cargar; si falla, no execute(), mensaje `[SEGURIDAD]`.
Arranque: inventario sistema + usuario actual; ilegal → no hay sesión.
Ambas capas obligatorias.

---

## Comportamiento de rechazo

```text
[SEGURIDAD] Comando '<nombre>' rechazado:
  - Import prohibido: import <modulo>
```

Texto lineal, no solo color. Determinista.

---

## Responsabilidades por componente

moslib/core/security.py AST; cmd_loader.py valida antes de cargar; shell.py tests de arranque; tests/test_security.py y test_all_commands_security.py.

---

## Espacio de usuario y confianza

No es código de confianza del producto. Siempre se valida. Puede bloquear arranque local.

---

## Límites de esta política

No cubre integridad del anfitrión, secretos fuera de MetsuOS, atacante que escribe moslib, binarios externos, bugs de stdlib/Python, RGPD.

---

## Requisitos derivados

REQ-SEC-001 a REQ-SEC-006 y REQ-A11Y-002.

---

## Verificación

Tests unitarios e inventario; demo de rechazo; arranque bloqueado y recuperado; mensaje usable.

---

## Cambios de política

Exigen actualizar este documento, tests, justificación y revisión SSS/ICD/A11Y. Sin flags para saltar seguridad.

---

## Ampliación normativa 1.2 (producto 0.2.7 / árbol 0.2.8)

Este apartado no relaja la política 1.1.

### Alcance añadido

| Ámbito | ¿Aplica? | Notas |
|--------|----------|-------|
| Comandos de app | Sí | Misma puerta AST |
| Almacén de claves IA en .mos | Sí | No git; no volcar valores |

### minimoslib

Un comando de app puede importar su mini-moslib **solo** si la validación recibe el `app_dir` de esa app. Fuera de ese directorio, el import es ilegal.

### Secretos de IA

`.mos/config/.ia_wrap` e `ia_keys.json`: no versionar, 0600, HMAC. status no lista valores. HTTP solo desde moslib.core.

### LAN y puente

share no abre puertos por sí solo. publicar es explícito. Puente :17337 off por defecto; no sirve `.mos`.

### Tests añadidos

test_security_minimoslib.py, test_ia_keys.py, test_ia_router.py.

---

## Autoridad

`04-SEC` es documento de máxima prioridad técnica junto con SSS y A11Y.

En caso de conflicto con conveniencia, prevalece esta política.

En caso de conflicto con un perfil A11Y soportado, se aplica «Relación con accesibilidad».
