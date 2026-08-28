# Campaña: ECSS-light, estilo, man y manual

**Fecha del plan:** 2026-08-20  
**NN del día:** 01  
**Estado:** Cerrada  
**Origen:** Reconstrucción a posteriori

---

## Objetivo

Fijar especificaciones para no reinventar el sistema, unificar estilo de código y dar manual de usuario más páginas `man` por comando.

## Fuera de alcance

- Burocracia ECSS completa de un programa espacial
- Cambiar el contrato de comandos
- GUI

---

## Qué se ejecutó (resumen)

- `docs/METHODOLOGY.md` (método humano + IA, ramas, commits)
- `docs/STYLE_GUIDE.md` y tests de normas críticas
- `docs/specs/` ECSS-light: OVERVIEW, SSS, SRS, ICD, SEC, SDD, TEST, SRelD
- `docs/USER_MANUAL.md`
- Comando `man` y `docs/man/<comando>.md`
- Tablas de directorios (una columna por nivel)
- Encabezados de documentación sin numeración (decisión de mantenimiento)

---

## Producto

| Momento | Valor |
|---------|--------|
| Inicio | `v0.2.1` ya en código de calidad |
| Cierre | Misma línea de producto 0.2.1; docs sobre esa baseline |

## Tags

- No hay tag solo-docs propio de esta ficha (el trabajo quedó en `main` sobre `v0.2.1`)

---

## Notas de reconstrucción

El marco documental y `man` se hicieron en fases numeradas en el chat. Esta ficha agrupa ese bloque; no lista cada fase 4.x.