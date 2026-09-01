# Plan previo — macro apps, tareas, suite, RGPD, malla

**Fecha del plan:** 2026-09-01  
**Orden del día:** 01  
**Producto de partida:** 0.2.5  
**Estado:** Índice de campañas 07–10

---

## Propósito

Fijar el orden de trabajo para los próximos ~2 meses. Este archivo no implementa código. La campaña 07 se detalla en su propio plan cuando se abra.

El rumbo de producto no se discute aquí: MOS2 es el lugar donde ocurre el trabajo; apps en repos propios; moslib como fachada; enrutador de IA; tareas tipo GTD; suite de desarrollo; malla de instancias al final.

---

## Relación con la campaña 06

La 06 queda en **dirección documentada** (`docs/INCENTIVOS.md`) y en este índice.

No se implementan en la 06: comandos de suite, API Grok en runtime, ni RGPD de producto. Eso pasa a 07–09.

Plan 06 actualizado: `docs/plans/2026-08-31-01-incentivos-desarrollo-datos.md`.

---

## Orden de campañas

| Id | Nombre | Entra | No entra |
|----|--------|-------|----------|
| 07 | Soporte y funcionamiento | Modelo de app (repo propio, normas MOS2, mini-moslib, instalar/quitar, quién accede). Tareas: manuales = comandos; automáticas = segundo plano + vista tipo tele; stub de prioridad, root, Maslow. Enrutador de IA mínimo (un proveedor al inicio; parámetros de coste/proyecto en spec). Fachada moslib si hace falta red. | Suite completa; P2P; RGPD de producto; DepManager geo real |
| 08 | App de desarrollo | App en repo aparte: plan, paso, aceptar fichero, commit o pegado, handoff, cierre. IA solo por el enrutador. Núcleo + apps de sistema + apps de usuario. | Malla |
| 09 | Prueba RGPD | Usar la suite para lo mínimo de datos (`.mos`, no filtrar a API). Ensayo del método, no certificación. | P2P |
| 10 | Malla de instancias | P2P / Onion / scattering; las automáticas empiezan a usarla | — |

Fuera de este tramo (siguen en `docs/DEUDA_Y_CAMPANAS.md`): laboratorio de lectores, dual C+Python, MOS2 sin Python 3, DepManager / origen geográfico (campaña propia, delicada).

---

## Principios de escalado (mandatorios al detallar la 07)

- Comandos: `execute` / `help`; imports solo stdlib + moslib.
- Si hace falta red u otra lib: entra por fachada moslib, no a pelo en la app.
- Apps ≠ comandos sueltos del núcleo. Repo propio, specs propias, sujetas a las del sistema.
- Mini-moslib de app: funciones que aún no están en el núcleo; vía de subida al moslib central / PR cuando el autor lo decida.
- Tareas automáticas primero **locales**. La malla no se usa como muleta de la 07.
- Humano valida. Sin autocommit por IA salvo excepción explícita del humano.
- Estado de campaña de producto: versionado en el repo que corresponda. Privado en `.mos`.
- A11Y, SEC y el resto de normas férreas del SSS son mandatorias para humano e IA. Sin A11Y el cambio no se acepta ni el código se ejecuta.
- INCENTIVOS.md orienta (humano se inclina; IA cumple también los vectores). No convierte A11Y en opcional.
- Diseñar listas, colas y tipos de hilo como datos estables (nombres y campos que se puedan ampliar), no como un script ad hoc.

---

## Criterio para abrir la 07

Este plan previo y el 06 corregido están en `main`. Entonces se escribe el plan **detallado** de la 07 (denso, escalable) y se trabaja esa campaña sola.

---

## Criterio de cierre de este índice

El archivo existe, el 06 apunta aquí, DEUDA lista 07–10. No hay tag de producto.