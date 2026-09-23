# Deuda técnica y campañas futuras previstas

**Versión del documento:** 1.10  
**Estado:** Inventario  
**Producto:** LAN/puente/check usable; write/multi/integridad/tope 120 en código; cierre documental en curso

---

## Propósito
No perder lo aplazado. No es spec. Mandan SEC, SSS, A11Y e INCENTIVOS.

---

## Lectura de dirección (metsuke.com, 2026-09-11)
No es spec. Sirve para no perder el vector.

- En la web pública el lenguaje contextual se llama MCL. En conversación a veces MPL. Unificar nombre en una campaña; hasta entonces: MPL/MCL.
- El contexto es de primera clase (capa). Un mismo comportamiento cambia según entorno, hardware, usuario, carga, modo.
- mosTaskManager + mosRTManager + mosAutomationManager: lo de MOS2 (tareas/hilos) es germen.
- NPL (Napalm) es otra línea. No mezclarla con MPL/MCL en la misma campaña.
- Skills: cada microtarea es código con contrato. La IA solo elige y llama.

---

## Hecho en esta línea (no reabrir como deuda ciega)
| Ítem | Nota |
|------|------|
| `update dev` + `dev publicar` / consolidar | Código; documentar en man update |
| Integridad dual + write/multi + codecs | Código; ritual en IA_WRITE |
| Tope 120 + `test 120` | Código |
| Menú `docs` por categoría + Nh | Código |
| Locale es_ES al arranque | Código |

---

## Deuda abierta
| Ítem | Destino |
|------|---------|
| `update` recarga módulos sin exit | Calidad / update |
| Worker de tareas solo vive con la sesión MOSh | Campaña hilos |
| Laboratorio de lectores de pantalla | Futura |
| Conteo fino passed/failed en a11y.py | Calidad |
| Geo / DepManager | Campaña propia |
| Dual Python + C | Futura |
| MOS2 sin Python 3 | Futura |
| Comillas en la línea de MOSh | Calidad |
| Formatos de salida (tablas + párrafos) | Campaña |
| Alias sistema `ia` → iarouter | Calidad |
| Alias de usuario CRUD | Campaña |
| Reglas éticas de enfrentamiento cibernético | Seguridad futura |
| Inventario ofensivo / lab defensivo | Tras ese documento |
| WSL2 vs IP LAN Windows (mirrored networking) | ENVIRONMENTS + man |
| Política jan_url no guardar IP propia | Código; falta test |
| GPT4All no por 17337 | Código; falta test |
| Specs ESA/README aún desfasados | Este cierre (specs + root) |
| App 08 bloqueada hasta docs + tareas + skills + MCL | Orden férreo |
| Chip UI `:s` en el producto Grok | Fuera de repo |

---

## Orden de campañas (férreo)
| Orden | Tema | Estado |
|-------|------|--------|
| 0 | Cierre documental | En curso (pages casi; faltan root + specs + mans) |
| 1 | Usar tareas e hilos de verdad | Prevista al cerrar docs |
| 2 | Atomización / skills | Prevista; previa a 08 |
| 3 | MPL/MCL | Prevista; previa a 08 |
| 4 | App de desarrollo (08) | Bloqueada hasta 0–3 |
| 5 | RGPD con la suite | Tras 08 |
| 6 | Malla | Tras 09 |

No se empieza la app “un poco”.

---

## Campaña prevista: tareas e hilos
Objetivo: que dejen de ser escaparate. Worker persistente o documentar por qué no. Sensor térmico/recursos lícito del SO. Criterio: encargar tarea, ver hilo, no perder trabajo al salir, o escrito por qué.

---

## Campaña prevista: atomización y skills
Microtareas = comando o función con execute/help. La IA no implementa la skill al vuelo; la invoca. Sin catálogo no hay app 08.

---

## Campaña prevista: MPL/MCL
Unificar nombre. Spec + plan propios. Layers y activación por contexto. Primer contexto: térmico y recursos. Luego entorno y proyecto.

---

## Mini iarouter (estado)
Código M0–M7 probado win+wsl+mac. Docs de spec/man siguen en el cierre.

Quien comparte: puente on, publicar, MOSh abierto, red privada. Quien consume: check, URL ajena, usar jan, preguntar. Jan local: 127.0.0.1, nunca IP LAN propia.

---

## Cómo se actualiza
Al cierre: hecho / se mantiene / se mueve a docs/plans/. Fuente: este JSON + `docgen generate deuda`.