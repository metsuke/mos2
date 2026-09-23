# Política de versionado de MetsuOS

**Versión del documento:** 1.3  
**Estado:** Normativo  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/specs/07-SRelD-Release-Baseline.md, CHANGELOG.md, pyproject.toml

---

## Propósito
Define cómo se asignan versiones de producto, tags Git y la relación con Poetry (`pyproject.toml`), para que código, documentación y releases no se desincronizen.

---

## Fuente de verdad de la versión de producto
| Elemento | Rol |
|----------|-----|
| pyproject.toml → version | Versión de producto (Poetry) |
| Tag Git vX.Y.Z | Marca de release alineada |
| CHANGELOG.md | Relato de cada release |
| Comando version en MOSh | Info Git |
| docs/specs/07-SRelD | Baselines |

La versión en `pyproject.toml` debe coincidir con el tag de producto funcional al publicar código.

---

## SemVer adaptado (alpha)
Formato `MAJOR.MINOR.PATCH`.

| Parte | Cuándo |
|-------|--------|
| MAJOR | Contrato o seguridad incompatible consciente |
| MINOR | Nueva capacidad usable |
| PATCH | Corrección o hardening sin feature |

En Alpha (`0.x.y`) la incompatibilidad ocasional se documenta en SRelD y CHANGELOG.

---

## Tipos de tag
| Tipo | Forma | ¿Bump Poetry? | Uso |
|------|-------|---------------|-----|
| Producto | vX.Y.Z | Sí | Runtime cambia |
| Solo docs | vX.Y.Z-docs | No | Docs sin cambio de runtime |

No crear tag de producto si solo cambió markdown.

---

## Cuándo actualizar pyproject.toml
Obligatorio al mergear a main un cambio de producto y al crear `vX.Y.Z`.

No actualizar Poetry en solo docs/onboarding/man sin comando nuevo.

Nunca avanzar producto directamente sobre `main`: rama feature + `dev`.

---

## Flujo de release de producto
1. Rama `feature/...` (`dev`).
2. Tests y arranque OK.
3. Docs (JSON + generate) en el mismo cierre.
4. CHANGELOG.
5. Bump pyproject.
6. Consolidar a main.
7. Tag anotado y push de tag.
8. Baseline en 07-SRelD si aplica.

---

## Flujo de release solo documentación
1. Rama solo docs.
2. CHANGELOG con `-docs` si se etiqueta.
3. Merge a main **sin** pyproject.
4. Tag opcional `vX.Y.Z-docs`.

Esta campaña de refundido es de este tipo mientras no cambie runtime.

---

## Sincronización con documentación
| Documento | Qué alinear |
|-----------|-------------|
| CHANGELOG.md | Entrada |
| README.md | Versión / estado |
| 07-SRelD | Capacidades |
| USER_MANUAL.md | Baseline |
| ENVIRONMENTS.md | Si cambió entorno |

---

## Responsabilidad de la IA
Al cerrar capacidad de producto: decir si hay bump y a qué versión; listar docs; texto del tag; no dejar Poetry viejo.

Si es solo docs: **sin bump Poetry**; CHANGELOG; tag `-docs` si se etiqueta.

---

## Estado actual de referencia
No copiar números de memoria. Antes del siguiente tag leer `pyproject.toml`, `git tag` y `CHANGELOG.md`.

---

## Autoridad
Normativo para versionado. Duda producto vs docs: si cambia mos2.sh / MOSh / comandos, es producto y lleva bump.