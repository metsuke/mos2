# 09 – Tareas

**Versión del documento:** 1.1  
**Estado:** Normativo (implementado en producto 0.2.7)  
**Baseline:** v0.2.7  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/08-APPS.md, docs/A11Y.md, docs/INCENTIVOS.md, docs/man/tareas.md, docs/man/hilos.md

---

## Propósito

Definir el sistema de tareas de MetsuOS (manual y automático), inspirado en GTD y ampliable.

No describe la malla P2P ni la suite de desarrollo. Las automáticas de esta baseline son **locales**.

---

## Principio

- **Manual:** el usuario entra en un comando, resuelve, sale.
- **Automática:** segundo plano local durante la sesión MOSh; se consulta como canales (texto lineal).
- Apps y núcleo **encolan** aquí. No inventan colas propias.

Si A11Y o SEC fallan, estado `bloqueada_a11y_sec`: **no se ejecuta**.

Módulo: `moslib.core.tasks`. Comandos: `tareas`, `hilos`. Worker de segundo plano en la sesión. Tests: `tests/test_tasks.py`.

Campos estables: id, origen, modo, privilegio, clase, proyecto, prioridad, maslow, recurrencia, intervalo, estado, comando, creado/actualizado.

Clases: realtime, heavy, normal, sistema (se reencola al vaciar).

## Autoridad

Normativo para tareas. Choca con SEC/A11Y/SSS → ganan esas.
