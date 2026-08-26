# Política de versionado de MetsuOS

**Versión del documento:** 1.0  
**Estado:** Normativo  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/specs/07-SRelD-Release-Baseline.md, pyproject.toml

---

## Propósito

Define cómo se asignan versiones de producto, tags Git y la relación con Poetry (`pyproject.toml`), para que código, documentación y releases no se desincronizen.

---

## Fuente de verdad de la versión de producto

| Elemento | Rol |
|----------|-----|
| pyproject.toml → version | Versión de producto (Poetry) |
| Tag Git vX.Y.Z | Marca de release alineada con esa versión |
| Comando version en MOSh | Muestra info basada en Git (tags/historial) |
| docs/specs/07-SRelD | Describe baselines y evolución |

La versión en `pyproject.toml` debe coincidir con el tag de producto **funcional** correspondiente cuando se publica una release de código.

---

## SemVer adaptado (alpha)

Formato: `MAJOR.MINOR.PATCH` (ejemplo actual: `0.2.2`).

| Parte | Cuándo subirla |
|-------|----------------|
| MAJOR | Cambios incompatibles de contrato o seguridad que rompan uso previo de forma consciente |
| MINOR | Nueva capacidad usable (comandos, espacio de usuario, guards de plataforma, etc.) |
| PATCH | Correcciones, ajustes menores de scripts, hardening sin feature nueva |

En fase Alpha (`0.x.y`) la incompatibilidad ocasional es aceptable si queda documentada en SRelD y en el mensaje de release.

---

## Tipos de tag

| Tipo | Forma | ¿Bump Poetry? | Uso |
|------|-------|---------------|-----|
| Producto | vX.Y.Z | Sí | Código y/o comportamiento de runtime cambia |
| Solo docs | vX.Y.Z-docs | No | Documentación, onboarding, specs sin cambio de runtime |

Ejemplos:

- `v0.2.2` — Poetry portable, entornos, bump a 0.2.2
- `v0.2.3-docs` — onboarding/VERSIONING sin tocar pyproject

No crear tags de producto si solo cambió markdown.

---

## Cuándo actualizar pyproject.toml

Obligatorio actualizar `version` en `pyproject.toml` cuando:

1. Se mergea a `main` un cambio de **producto** (fix/feat de runtime, scripts de lanzamiento, comandos, seguridad, tests de arranque que cambien comportamiento).
2. Se va a crear el tag `vX.Y.Z` de esa release.

No actualizar Poetry cuando:

- Solo hay docs, onboarding, STYLE, METHODOLOGY, man pages sin comando nuevo.
- Solo hay commits `docs:` o `chore:` de mantenimiento documental.

La IA y el desarrollador deben, al cerrar una fase de producto, **incluir el bump** en el plan de merge y verificar que README/SRelD no queden con una versión incorrecta o falsa.

---

## Flujo de release de producto

1. Trabajar en `feature/...`.
2. Tests en verde; arranque de MOSh OK.
3. Actualizar docs/specs afectadas **antes o en el mismo merge**.
4. Bump en `pyproject.toml` al valor de la release.
5. Merge a `main`.
6. Tag anotado: `git tag -a vX.Y.Z -m "..."`.
7. `git push origin main` y `git push origin vX.Y.Z`.
8. Anotar la baseline en `07-SRelD` si el cambio lo merece.

---

## Flujo de release solo documentación

1. Rama `feature/...` solo docs.
2. Merge a `main` **sin** cambiar `pyproject.toml`.
3. Tag opcional: `vX.Y.Z-docs` (Z o el sufijo que deje claro que no es producto).
4. No exigir bump de Poetry.

---

## Sincronización con documentación

Al asignar un tag de producto, revisar y actualizar si aplica:

| Documento | Qué alinear |
|-----------|-------------|
| README.md | Línea de versión / estado |
| docs/specs/07-SRelD | Capacidades y tags de la release |
| docs/USER_MANUAL.md | Baseline de referencia del manual |
| docs/ENVIRONMENTS.md | Solo si el comportamiento de entorno cambió |

Al tag solo-docs, basta con que el contenido nuevo exista; no hace falta subir la versión de Poetry.

---

## Responsabilidad de la IA en el plan por fases

Cuando el plan cierre una capacidad de producto, la IA debe:

1. Decir explícitamente si hay **bump Poetry** y a qué versión.
2. Listar docs a tocar (SRelD, README, etc.).
3. Proponer el texto del tag.
4. No dejar `pyproject.toml` en una versión antigua tras mergear features de runtime.

Si la fase es solo documentación, debe decir: **sin bump Poetry** y sugerir tag `-docs` si se etiqueta.

---

## Estado actual de referencia

| Campo | Valor orientativo al escribir este doc |
|-------|----------------------------------------|
| Versión Poetry | 0.2.2 |
| Último tag de producto | v0.2.2 |
| Siguiente trabajo típico | Onboarding (candidato a tag -docs sin bump) |

Comprobar siempre el repo (`pyproject.toml` y `git tag`) antes de decidir el siguiente número.

---

## Autoridad

Este documento es normativo para versionado de producto y tags.

Ante duda entre “¿es producto o solo docs?”, priorizar: **si cambia el comportamiento al ejecutar mos2.sh / MOSh / comandos, es producto y lleva bump.**