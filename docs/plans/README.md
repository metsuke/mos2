# Planes de campaña de MetsuOS

**Versión del documento:** 1.6  
**Estado:** Normativo de proceso  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/VERSIONING.md, docs/AI_ONBOARDING.md, CHANGELOG.md

---

## Propósito
Cada campaña de trabajo tiene un plan escrito **antes** de implementar (salvo las reconstruidas a posteriori).

Sirve para humanos y agentes IA: qué se acordó, cuándo, y en qué orden si ese día hubo más de una.

La tabla del índice no se edita a mano. Sale de docs/docgen/plans/ (un JSON por plan) con `docgen plan` y `docgen generate plans-readme`.

---

## Nombre de archivo
```text
YYYY-MM-DD-NN-slug.md
```

| Pieza | Significado |
|-------|-------------|
| YYYY-MM-DD | Día en que se escribió o arrancó el plan |
| NN | Orden dentro de ese día (01, 02, …) |
| slug | Título corto |

No hay contador global en el nombre.

---

## Índice
| Fecha | NN del día | Archivo | Estado |
|-------|------------|---------|--------|
| 2026-08-12 | 01 | 2026-08-12-01-espacio-usuario.md | Cerrada |
| 2026-08-16 | 01 | 2026-08-16-01-tests-seguridad-update.md | Cerrada |
| 2026-08-20 | 01 | 2026-08-20-01-ecss-man-manual.md | Cerrada |
| 2026-08-25 | 01 | 2026-08-25-01-entornos-onboarding-versionado.md | Cerrada |
| 2026-08-28 | 01 | 2026-08-28-01-higiene-a11y-cierre.md | En curso (Grupo I y Cierre I hechos; Grupo II ampliado antes del Bloque 1.2) |
| 2026-08-31 | 01 | 2026-08-31-01-incentivos-desarrollo-datos.md | Cerrada en alcance. Bloques 2 y 3 de la redacción inicial retirados. |
| 2026-09-01 | 01 | 2026-09-01-01-macro-apps-tareas-suite-rgpd-malla.md | Índice de campañas 07–10 |
| 2026-09-01 | 02 | 2026-09-01-02-campana-07-soporte-apps-tareas-ia.md | A ejecutar |
| 2026-09-03 | 01 | 2026-09-03-01-campana-08-app-desarrollo.md | Diseñada |
| 2026-09-04 | 01 | 2026-09-04-01-07-fix-apps-reales.md | Obliga a pausar 8.2+ hasta cerrar esto |
| 2026-09-04 | 02 | 2026-09-04-02-07-completa.md | La 08 (suite) congelada hasta cierre de este plan. |
| 2026-09-07 | 01 | 2026-09-07-01-iarouter-modelos-lan.md | Diseñada |
| 2026-09-13 | 01 | 2026-09-13-01-iarouter-check-scopes.md | En curso |
| 2026-09-13 | 02 | 2026-09-13-02-sync-docs-028.md | Cerrada (docs aplicados en local; merge/tag a criterio humano) |
| 2026-09-14 | 01 | 2026-09-14-01-docgen.md | Cerrada en alcance de motor (pendiente pruebas humanas y bump) |
| 2026-09-18 | 01 | 2026-09-18-01-integridad-write.md | En curso |

## Ciclo
1. Diseñar la campaña en el chat.
2. Crear el plan **antes** del primer cambio de código.
3. `docgen plan add YYYY-MM-DD-NN-slug.md` (o write del JSON del plan + generate).
4. Ejecutar por bloques/pasos (`:s`).
5. `docgen plan set <id> Cerrada` y `docgen generate plans-readme` en el mismo lote.
6. Si el plan cambia, actualizar JSON y regenerar.

---

## Contenido mínimo de un plan
- Fecha y NN del día
- Objetivo y fuera de alcance
- Estado
- Producto al inicio y al cierre
- Bloques y pasos
- Tags
- Cierres de grupo (interacción + deuda) si aplica
- Nota si es reconstrucción

---

## Autoridad
No se inicia una campaña amplia sin su plan en esta carpeta.