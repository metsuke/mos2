# Planes de campaña de MetsuOS

**Versión del documento:** 1.2  
**Estado:** Normativo de proceso  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/VERSIONING.md, docs/AI_ONBOARDING.md, CHANGELOG.md

---

## Propósito

Cada campaña de trabajo tiene un plan escrito **antes** de implementar (salvo las reconstruidas a posteriori).

Sirve para humanos y agentes IA: qué se acordó, cuándo, y en qué orden si ese día hubo más de una.

---

## Nombre de archivo

```text
YYYY-MM-DD-NN-slug.md
```

| Pieza | Significado |
|-------|-------------|
| YYYY-MM-DD | Día en que se escribió o arrancó el plan |
| NN | Orden dentro de ese día (01, 02, …). No es un id global |
| slug | Título corto en humano |

El número de campañas del proyecto se ve contando ficheros y este índice. No hay contador global en el nombre.

---

## Índice

| Fecha | NN del día | Archivo | Estado |
|-------|------------|---------|--------|
| 2026-08-12 | 01 | 2026-08-12-01-espacio-usuario.md | Cerrada |
| 2026-08-16 | 01 | 2026-08-16-01-tests-seguridad-update.md | Cerrada |
| 2026-08-20 | 01 | 2026-08-20-01-ecss-man-manual.md | Cerrada |
| 2026-08-25 | 01 | 2026-08-25-01-entornos-onboarding-versionado.md | Cerrada |
| 2026-08-28 | 01 | 2026-08-28-01-higiene-a11y-cierre.md | Diseñada |

Fechas de las cerradas: aproximadas al trabajo real; cada plan lo indica si es reconstrucción.

---

## Ciclo

1. Diseñar la campaña en el chat.
2. Crear el plan en esta carpeta **antes** del primer cambio de código.
3. Ejecutar por bloques/pasos (un archivo o paso cada vez).
4. Si el plan cambia, actualizar el fichero.
5. Al cerrar: estado, tags, bump Poetry sí/no.

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