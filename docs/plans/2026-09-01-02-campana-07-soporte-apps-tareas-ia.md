# Plan detallado — campaña 07 soporte (apps, tareas, IA)

**Fecha:** 2026-09-01  
**Orden del día:** 02  
**Producto de partida:** 0.2.5  
**Estado:** A ejecutar  
**Padre:** docs/plans/2026-09-01-01-macro-apps-tareas-suite-rgpd-malla.md

---

## Propósito

Dejar cimientos **escalables** para que la 08 (suite de desarrollo) no se construya sobre arena.

Tres frentes, en este orden interno:

1. Modelo de **app** (repo propio, normas MOS2, instalar/quitar, acceso).
2. **Tareas** GTD (manuales = comandos; automáticas = segundo plano local + vista tipo tele).
3. **Enrutador de IA mínimo** (un proveedor al inicio; políticas en config del sistema, no “lo decide el modelo”).

Sin A11Y / SEC el artefacto **no se acepta ni se ejecuta**.

---

## Fuera de la 07

Suite completa (08). RGPD de producto (09). Malla P2P/Onion (10). DepManager geo real. Dual C. Runtime sin Python 3.

---

## Normas que no se tocan

- Contrato `execute` / `help`; imports solo stdlib + moslib.
- Red u otra lib: fachada en moslib, nunca a pelo en la app.
- Humano valida. Sin autocommit por IA salvo excepción explícita.
- Estado de producto versionado; privado en `.mos`.
- Mini-moslib de app puede existir; subir al núcleo es proceso aparte (PR / campaña).

---

## Frente A — apps

### Qué es una app (estable)

| Campo | Contenido |
|-------|-----------|
| id | Nombre estable (slug) |
| repo | URL o ruta del repo propio |
| version | SemVer de la app |
| comandos | Módulos con execute/help |
| mini_moslib | Opcional; solo lo que el núcleo aún no da |
| acceso | Quién puede instalar/usar (spec; implementación mínima en 07) |
| docs | Specs y man propios, sujetos a A11Y/SEC/SSS del sistema |

No es un `.py` suelto en `moslib/commands/`. El núcleo **descubre** apps instaladas y carga sus comandos con la misma validación AST que el sistema.

### Hito A (07)

- Spec SSS/ICD/SRS: ciclo de vida install / list / remove.
- Un directorio de apps instaladas **fuera** del árbol versionado de producto o claramente separado (p. ej. bajo `.mos/apps/` o `rootfs/opt/apps/` — se elige en el primer bloque de código y no se cambia a la ligera).
- Comandos de sistema mínimos: listar apps, mostrar metadatos. Instalar desde path local basta; tienda remota no.
- Tests: app de prueba (fixture) carga; app con import ilegal no carga; app sin help no carga; fallo A11Y de la app = no se acepta (mismo listón que un comando de sistema).

---

## Frente B — tareas

### Modelo de datos (ampliable, no ad hoc)

| Campo | Uso |
|-------|-----|
| id | Estable |
| origen | sistema / app / usuario |
| modo | manual / automatica |
| privilegio | root / no-root |
| clase | realtime / heavy / normal / sistema |
| proyecto | slug |
| prioridad | entero o enum; factores de proyecto = spec, fórmula simple en 07 |
| maslow | solo tareas de usuario; enum 1–5 stub |
| recurrencia | una_vez / cada_n_minutos / cada_n_dias |
| estado | pendiente / en_curso / hecha / fallida / bloqueada_a11y_sec |
| comando | qué se invoca |

Pila: las listas alimentan una cola. Clase **sistema**: al vaciarse, se reencola.

### Manuales

Son **comandos** (entras, resuelves, sales). Ejemplo: validar un documento una vez. Recurrente manual: cada N días aparece otra vez.

El usuario las ve siempre.

### Automáticas

Segundo plano **local**. Intervalo dinámico (prioridad). Root: puede leer recursos/temperatura del anfitrión por fachada moslib (stdlib).

Vista **tele**: comando que lista hilos por tipo y estado (texto lineal, A11Y). No hace falta TUI rica en la 07.

### Hito B (07)

- Spec del modelo de datos.
- Persistencia en espacio sistema o `.mos` según origen (usuario → `.mos`; sistema → árbol de producto o var local no versionada — decidir en spec y no mezclar secretos).
- Comandos: `tareas` (listar/filtrar), entrar en una manual, `hilos` (vista tele).
- Un worker mínimo: si MOSh está abierto o vía proceso hijo documentado; si el shell sigue síncrono, el worker puede ser un comando `tareas tick` + nota de diseño para daemon posterior. **No** fingir P2P.
- Tests unitarios del modelo y de que una tarea bloqueada_a11y_sec no se ejecuta.

---

## Frente C — enrutador de IA mínimo

### Qué

Un módulo moslib (fachada) + comando de config/uso:

- Proveedor inicial: **uno** (Grok u OpenRouter; se fija en spec).
- Políticas en fichero de sistema/usuario: activado sí/no, techo de coste stub, proyecto asociado stub.
- La IA **no** guarda la política. La lee el sistema.
- Payload: mínimo. Prohibido `.mos` salvo whitelist explícita del humano.
- Si no hay red o no hay clave: error claro, sin crash.

### Hito C (07)

- Spec de la fachada (no todos los parámetros del diseño largo).
- Implementación: stdlib (`urllib`) detrás de moslib **o** “no implementado / desactivado” con la misma API para no pintar a la 08 en un rincón.
- Tests: no llama si política off; no incluye rutas `.mos` en el cuerpo por defecto.

---

## Orden de bloques dentro de la 07

| Bloque | Qué |
|--------|-----|
| 7.0 | Specs: SSS/SRS/ICD delta (app, tarea, router). A11Y como puerta de accept. |
| 7.1 | Código + tests Frente A (apps locales). |
| 7.2 | Código + tests Frente B (tareas + tele). |
| 7.3 | Código + tests Frente C (router mínimo). |
| 7.4 | man, README, CHANGELOG, tag de producto si hay runtime. |

No se abre 7.2 si 7.1 no carga una app de prueba con las mismas reglas SEC/A11Y que un comando de sistema.

---

## Criterio de cierre 07

- Hay spec de app y de tarea con campos estables.
- Se instala una app local de prueba y se desinstala.
- Hay lista de tareas manuales y una vista de hilos.
- Hay fachada de IA con política off por defecto.
- Tests verdes; arranque bloquea si SEC/A11Y de lo nuevo falla.
- 08 puede empezar sin rediseñar el modelo.

---

## Primer paso de ejecución (cuando digas)

Rama `feature/campana-07-soporte`. Bloque 7.0: delta de specs (empezar por SSS o un `docs/specs` de apps/tareas, lo que encaje sin romper ECSS-light).