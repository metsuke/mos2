# Plan detallado — campaña 08 app de desarrollo

**Fecha:** 2026-09-03  
**Orden del día:** 01  
**Producto de partida:** 0.2.6  
**Padre:** docs/plans/2026-09-01-01-macro-apps-tareas-suite-rgpd-malla.md

---

## Propósito

Meter **este** método de trabajo dentro de MOS2: plantear un paso, el humano acepta, el cambio ocurre (escribir fichero y, si quiere, commit) **sin pegar a mano**, pudiendo seguir pegando si lo prefiere.

La suite es una **app** (repo propio), no comandos sueltos del núcleo. Usa apps, tareas e iarouter de la 07.

---

## Fuera de la 08

RGPD de producto (09). Malla P2P (10). DepManager geo. Autocommit por IA salvo excepción explícita. Daemon pesado de tareas.

---

## Qué entrega la app

| Comando (nombres ICD) | Función |
|------------------------|---------|
| campaña | Estado: id, bloque, paso, fichero |
| paso | Muestra breadcrumb + texto a aplicar |
| aceptar | Escribe el fichero (o el recorte) en el clone |
| commit | Prepara o ejecuta git add/commit **si el humano lo pide** |
| handoff | Texto con SHA + paso para otro chat |
| cierre | Tablas de INTERACTION_REVIEW / deuda |

IA: solo `moslib.core.ia_router.complete`, off por defecto; envío = acción explícita.

---

## Repo y carga

- Repo aparte (p. ej. metsuke/mos-devapp). En 08 puede vivir un árbol `apps/dev/` **dentro de mos2** solo como cuna; el destino es repo propio.
- `app.json` + `commands/` con execute/help.
- Instalar: `apps install <ruta>`.
- **Hueco 07:** cmd_loader aún no ejecuta comandos de `.mos/apps`. Bloque 8.0 = cargar esos comandos (sin pisar sistema; prefijo `app_dev_` o namespace). Sin esto la suite no se invoca.

---

## Flujo exacto (humano al volante)

1. `synccheck` alineado.
2. `campaña` / `paso`: qué fichero y qué contenido.
3. Humano lee. Opciones: `aceptar` (escribe disco) o copiar.
4. Opcional: `paso --preguntar` → iarouter (si enabled).
5. `commit` solo con confirmación. La IA no hace push.
6. `hecho` avanza estado (versionado en docs/plans o estado de la app).
7. Salto de número: hay que escribir la causa.
8. Sin A11Y/SEC: no accept, no ejecución.

---

## Bloques

| Bloque | Qué |
|--------|-----|
| 8.0 | cmd_loader carga comandos de apps instaladas |
| 8.1 | Esqueleto app (app.json, man, install local) |
| 8.2 | Estado + paso + aceptar (escribir fichero) |
| 8.3 | commit / handoff / cierre |
| 8.4 | Enganche iarouter (pregunta explícita) |
| 8.5 | Docs núcleo + tag si el loader cambia producto |

---

## Criterio de cierre

- Un comando de la app se invoca en MOSh.
- `aceptar` escribe un fichero de prueba y `commit` genera o ejecuta el git **solo** si se confirma.
- iarouter sigue off salvo config.
- 09 puede usar la suite sin rediseñar el modelo.

---

## Primer paso de ejecución

Rama `feature/campana-08-devapp`. Bloque **8.0**: extender `cmd_loader` + tests.