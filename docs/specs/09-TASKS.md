# 09 – Tareas

**Versión del documento:** 1.0  
**Estado:** Normativo (campaña 07, frente B)  
**Baseline:** v0.2.5  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/08-APPS.md, docs/A11Y.md, docs/INCENTIVOS.md, docs/plans/2026-09-01-02-campana-07-soporte-apps-tareas-ia.md

---

## Propósito

Definir el sistema de tareas de MetsuOS (manual y automático), inspirado en GTD y ampliable.

No describe la malla P2P (10) ni la suite de desarrollo (08). Las automáticas de la 07 son **locales**.

---

## Principio

- **Manual:** el usuario entra en un comando, resuelve, sale.
- **Automática:** segundo plano local; se consulta como “canales” (texto lineal).
- Apps y núcleo **encolan** aquí. No inventan colas propias.

Si A11Y o SEC fallan, estado `bloqueada_a11y_sec`: **no se ejecuta**.

---

## Campos estables

| Campo | Obligatorio | Valores / notas |
|-------|-------------|-----------------|
| id | sí | estable |
| origen | sí | sistema / app / usuario |
| modo | sí | manual / automatica |
| privilegio | sí | root / no-root |
| clase | sí | realtime / heavy / normal / sistema |
| proyecto | no | slug |
| prioridad | sí | entero ≥ 0; 0 = más urgente en 07 |
| maslow | no | 1–5; solo origen usuario; stub |
| recurrencia | sí | una_vez / cada_n_minutos / cada_n_dias |
| intervalo | no | N según recurrencia |
| estado | sí | pendiente / en_curso / hecha / fallida / bloqueada_a11y_sec |
| comando | sí | qué invocar |
| creado / actualizado | sí | timestamps |

No renombrar estos campos. Se pueden añadir otros en v1.1+.

---

## Clases y privilegio

| Clase | Uso |
|-------|-----|
| realtime | Poca latencia; no bloquear con trabajo heavy |
| heavy | Largo o mucha CPU/RAM |
| normal | Resto |
| sistema | Al vaciar la pila de esa clase, se **reencola** |

Root: puede usar fachada moslib para recursos/temperatura del anfitrión (stdlib). No-root: no.

Intervalo de automáticas: en 07, función simple de `prioridad` (documentar la fórmula en ICD). No hace falta la fórmula final de producto.

---

## Persistencia

| origen | Dónde |
|--------|--------|
| usuario | `.mos/` (no versionar como producto) |
| app | datos de esa app, no el árbol público del núcleo salvo que la app sea de sistema |
| sistema | almacén de sistema local; no secretos en git |

---

## Comandos (07)

| Comando (nombre a fijar en ICD) | Función |
|---------------------------------|---------|
| listar / filtrar | siempre las manuales del usuario; automáticas bajo filtro |
| entrar en manual | ejecutar el comando asociado |
| hilos (tele) | por tipo: estado, clase, privilegio; texto lineal, no solo color |
| tick | avanzar automáticas si aún no hay daemon |

Shell síncrono: `tick` o proceso hijo documentado. No fingir red ni P2P.

---

## Recurrencia

- `una_vez`: al `hecha`, no vuelve.
- `cada_n_dias`: manual recurrente; reaparece.
- `cada_n_minutos`: automática; N ajustable por prioridad en ICD.

---

## Criterios de aceptación del frente B

1. Este spec publicado.
2. Se crea una manual `una_vez`, se lista, se entra, pasa a `hecha`.
3. Una automática `sistema` se reencola al vaciar (test unitario o tick).
4. `bloqueada_a11y_sec` no invoca `comando`.
5. Vista hilos usable con teclado y lector de terminal.

---

## Autoridad

Normativo para tareas. Choca con SEC/A11Y/SSS → ganan esas.