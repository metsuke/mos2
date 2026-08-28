# Campaña: tests, seguridad de arranque y update

**Fecha del plan:** 2026-08-16  
**NN del día:** 01  
**Estado:** Cerrada  
**Origen:** Reconstrucción a posteriori

---

## Objetivo

Hacer obligatorios los tests unitarios y de seguridad en desarrollo y en producción, y poder actualizar el clone local desde `origin/main` sin perder trabajo local.

## Fuera de alcance

- CI externa
- Permitir imports fuera de stdlib + moslib
- Subir ramas `backup/*` a producción

---

## Qué se ejecutó (resumen)

- Validación AST de imports en comandos de sistema y de usuario
- Tests en `tests/` (seguridad, user, cmd_loader, contrato)
- Arranque de MOSh: si fallan los tests, no inicia
- El inventario de seguridad en arranque debe fallar si cualquier comando viola imports
- Comando `update`: backup local con fecha, pull forzado de `main`, máximo 10 ramas `backup/*`
- Tag de producto `v0.2.1`

---

## Producto

| Momento | Valor |
|---------|--------|
| Inicio | Tras espacio de usuario (`v0.2.0-alpha-user-space`) |
| Cierre | Poetry / tag `v0.2.1` |

## Tags

- `v0.2.1`

---

## Notas de reconstrucción

En el chat, `man`, specs y STYLE se solaparon justo después; esa documentación vive en la campaña `2026-08-20-01-ecss-man-manual.md`. Esta ficha cubre calidad, seguridad y `update`.