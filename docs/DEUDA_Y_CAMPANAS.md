# Deuda técnica y campañas futuras previstas

**Versión del documento:** 1.8
**Estado:** Inventario
**Producto:** código LAN/puente/check usable en win, wsl y mac; cierre documental en curso
**SHA de código de referencia:** f2c512d

---

## Propósito

No perder lo aplazado. No es spec. Mandan SEC, SSS, A11Y e INCENTIVOS.

---

## Lectura de dirección (metsuke.com, 2026-09-11)

No es spec. Sirve para no perder el vector.

- En la web pública el lenguaje contextual se llama MCL (MetsuOS Context Language). En esta conversación el humano lo nombra MPL (Metsu Programming Language). Unificar nombre en una sola campaña; hasta entonces: MPL/MCL.
- MCL/MPL: el contexto es de primera clase (capa / layer). Un mismo comportamiento cambia según entorno, hardware, usuario, temperatura, carga, modo. No un bosque de if sueltos.
- mosTaskManager + mosRTManager + mosAutomationManager en apps.html: colas, dependencias, tiempo real, automatización. Lo que hay en MOS2 (tareas/hilos) es el germen; no está listo como base de la app de desarrollo.
- NPL (Napalm) es otra línea (ciencia probabilística). No mezclarla con MPL/MCL en la misma campaña.
- Skills: cada microtarea es código normal con contrato (execute/help, moslib). La IA solo elige y llama. No genera la acción.

---

## Deuda abierta

| Ítem | Destino |
|------|---------|
| Rama habitual de pruebas (p. ej. devtest) y `update` con parámetro de rama/origen, no solo origin/main | Calidad / comando update |
| `update` debe dejar el código nuevo cargado sin depender de que el humano recuerde salir y entrar de MOSh | Calidad / update |
| Worker de tareas solo vive con la sesión MOSh | Campaña hilos/tareas |
| Laboratorio de lectores de pantalla | Futura |
| Conteo fino passed/failed en a11y.py | Calidad |
| VERSIONING.md docs.N | Este cierre docs |
| Geo / DepManager | Campaña propia |
| Dual Python + C | Futura (encaja con backends MCL) |
| MOS2 sin Python 3 | Futura |
| Comillas en la línea de MOSh | Calidad |
| Formatos de salida en pantalla (tablas + párrafos) | Campaña propia |
| Alias de sistema `ia` para `iarouter` | Calidad / iarouter |
| Alias de usuario (crear, listar, editar, borrar) | Campaña propia |
| Documento de reglas éticas de enfrentamiento cibernético | Campaña de seguridad futura |
| Inventario de red ofensivo / laboratorio defensivo | Tras ese documento |
| WSL2 no usa la misma ruta que Mac hacia la IP LAN de Windows; documentar mirrored networking | ENVIRONMENTS + man iarouter |
| La IA no debe leer raw `.../main/archivo` (CDN miente). Obligatorio SHA o `synccheck` | AI_ONBOARDING |
| Política jan_url no debe guardar la IP LAN propia ni el puente local (bucle) | Hecho en código; falta test |
| GPT4All no debe resolverse por el puerto 17337 | Hecho en código; falta test |
| Specs ESA, USER_MANUAL y README desfasados respecto a check/puente/WSL | Este cierre documental |
| App de desarrollo (08) no se abre hasta cerrar docs + campaña de uso de tareas/hilos + atomización/skills + arranque MPL/MCL | Orden férreo |

---

## Orden de campañas a partir de ahora (férreo)

| Orden | Id | Tema | Estado |
|-------|----|------|--------|
| 0 | — | Cierre documental (specs ESA, man, manual, README, CHANGELOG, onboarding) | En curso, 20 pasos |
| 1 | — | Usar de verdad tareas e hilos ya existentes: pruebas, fallos, arreglo mínimo para que el worker no sea de usar y tirar | Prevista al cerrar docs |
| 2 | — | Atomización máxima: cada microtarea es código con contrato; la IA solo despacha llamadas (skills). Sin esto no hay app de desarrollo | Prevista; previa a 08 |
| 3 | — | MPL/MCL: lenguaje y runtime de contexto (capas). Incluye política automática de carga según temperatura y recursos en hilos RT | Prevista; previa a 08 |
| 4 | 08 | App de desarrollo | Bloqueada hasta 0–3 |
| 5 | 09 | RGPD con la suite | Tras 08 |
| 6 | 10 | Malla de instancias | Tras 09 |
| — | 05 | Higiene, A11Y | Cerrada |
| — | 06 | INCENTIVOS | Cerrada en alcance |
| — | 07 | Apps, tareas, iarouter base | Cerrada en 0.2.7 (germen) |
| — | mini | iarouter modelos/claves/LAN/share/puente | Código usable; docs en paso 0 |

No se “empieza la app un poco”. Si 1–3 no están, 08 reproduce este chat dentro de MOS2.

---

## Campaña prevista: tareas e hilos (post-docs)

Objetivo: que `tareas` y `hilos` dejen de ser código de escaparate.

- Ejecutar en win, wsl y mac listas manuales y automáticas reales.
- Documentar qué se rompe (worker atado a la sesión MOSh, sin persistencia de pila, sin tele, sin root vs no-root usable).
- Arreglo mínimo para poder vivir con ellas días, no un demo.
- Hilos RT: leer temperatura y recursos del anfitrión (solo datos lícitos del SO) y **bajar o pausar** trabajo pesado si la máquina se calienta o se queda sin aire. Eso es COP aplicada: contexto `alta_temperatura` / `poca_cpu` activa otra capa de planificación. No hace falta el compilador MPL todavía; sí hace falta el sensor + la política en el planificador actual.
- Criterio de salida: un humano puede encargar una tarea manual, ver un hilo automático y no perder el trabajo al salir de MOSh, o queda escrito por qué aún no y qué se parchea antes de skills.

## Campaña prevista: atomización y skills (previa a 08)

- Toda campaña futura se parte en microtareas que quepan en un comando o función moslib con `execute`/`help`.
- Cada skill es código revisable, testeable, con A11Y y SEC. La IA no implementa la skill en el momento; solo la invoca.
- Equivale a no dejar que la IA “escriba el commit a ciegas”: el humano autoriza; el código hace el gesto.
- Sin catálogo de skills no se construye la app de desarrollo.

## Campaña prevista: MPL/MCL (previa a 08)

- Nombre a unificar con el humano (MPL vs MCL de metsuke.com).
- Spec + plan propios. No meter un compilador entero en la misma tanda que el arreglo de hilos.
- Dirección ya conocida: layers, activación por contexto, backends (Python primero; C después encaja con la deuda dual).
- Primer contexto operativo a honrar en hilos: térmico y de recursos. Luego entorno (win/wsl/mac/nix), luego proyecto/prioridad.

---

## Mini iarouter (estado)

| Ítem | Estado |
|------|--------|
| M0–M7 código (modelos, claves, LAN, share, publicar, puente, check) | Hecho y probado win+wsl+mac |
| M8 spec/man/USER_MANUAL/README/CHANGELOG/ESA | Este cierre (paso 0) |

Flujo que debe quedar escrito:

- Quien comparte (win con Jan): `iarouter puente on`, `iarouter publicar`, MOSh abierto, red Privada.
- Quien consume (mac o wsl): `iarouter check`, guardar solo URL ajena, `iarouter usar jan`, `iarouter preguntar`.
- Quien ya tiene Jan local: 127.0.0.1, nunca la IP LAN propia ni :17337 de sí mismo.

---

## Cómo se actualiza

Al cierre: hecho / se mantiene / se mueve a docs/plans/.