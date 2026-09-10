# Deuda técnica y campañas futuras previstas

**Versión del documento:** 1.7  
**Estado:** Inventario  
**Producto:** 0.2.7 (mini iarouter en curso hacia 0.2.8)

---

## Propósito

No perder lo aplazado. No es spec. Mandan SEC, SSS, A11Y e INCENTIVOS.

---

## Deuda abierta

| Ítem | Destino |
|------|---------|
| Rama habitual de pruebas (p. ej. devtest) y `update` con parámetro de rama/origen, no solo origin/main | Calidad / comando update |
| Worker de tareas solo vive con la sesión MOSh | 10 / campaña propia |
| Laboratorio de lectores de pantalla | Futura |
| Conteo fino passed/failed en a11y.py | Calidad |
| VERSIONING.md docs.N | Cierre docs |
| Geo / DepManager | Campaña propia |
| Dual Python + C | Futura |
| MOS2 sin Python 3 | Futura |
| Suite de desarrollo (aceptar/commit/handoff) | 08 (después de esta mini) |
| Comillas en la línea de MOSh | Calidad / 08 |
| Formatos de salida en pantalla | Campaña propia |
| Documento de reglas éticas de enfrentamiento cibernético (defensa si hay ataque directo; no ofensiva) | Campaña de seguridad futura |
| Inventario de red ofensivo / laboratorio defensivo | Tras ese documento |

Hasta que exista `devtest` + `update <rama>`, el código de prueba entre máquinas se publica por **main** y se trae con `update`.

## Cerrada en 0.2.7

| Ítem |
|------|
| Apps, prefijos, minimoslib, worker de sesión |
| iarouter base detectar/usar/preguntar |

## Mini iarouter (esta campaña)

| Ítem | Estado |
|------|--------|
| M0 plan | Hecho |
| M1 modelos | Hecho |
| M2 claves + secreto | Hecho |
| M3 grok/openrouter listar | Hecho (tests mock) |
| M4 LAN Jan/GPT4All | Hecho en código |
| M5 share | Hecho |
| M6 publicar | Hecho |
| M7 puente | Hecho |
| M8 spec/man/CHANGELOG 0.2.8 | En curso |

---

## Campañas

| Id | Tema | Estado |
|----|------|--------|
| 05 | Higiene, A11Y | Cerrada |
| 06 | INCENTIVOS | Cerrada en alcance |
| 07 | Apps, tareas, iarouter base | Cerrada en 0.2.7 |
| — | Mini iarouter modelos/claves/LAN/share/puente | En curso (plan 2026-09-07-01) |
| 08 | App de desarrollo | Después de la mini |
| 09 | Prueba RGPD con la suite | Prevista |
| 10 | Malla de instancias | Prevista |
| — | Formatos de salida en pantalla | Prevista |

---

## Cómo se actualiza

Al cierre: hecho / se mantiene / se mueve a docs/plans/.