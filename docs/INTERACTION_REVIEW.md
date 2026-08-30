# Revisión de interacción humano ↔ IA

**Versión del documento:** 1.0  
**Estado:** Normativo de proceso  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/AI_ONBOARDING.md, AGENTS.md, docs/HUMAN_ONBOARDING.md, docs/plans/README.md

---

## Propósito

Plantilla obligatoria al cerrar un grupo de bloques o una campaña.

Sirve para:

- convertir incidentes del chat en normas
- listar deuda técnica
- no perder campañas futuras

No sustituye a SEC, SSS ni A11Y.

---

## Cómo se usa

1. La IA rellena las tablas con lo ocurrido en el grupo.
2. El humano corrige o valida.
3. Lo aceptado pasa a METHODOLOGY / AI_ONBOARDING / AGENTS en el mismo grupo o en el siguiente paso.
4. La deuda no resuelta se copia al cierre de campaña o a docs de planes.

Se pueden añadir secciones nuevas a esta plantilla; no se quitan las dos bases (interacción y deuda).

---

## Psicología y ética de acompañamiento

La IA puede usar conocimiento de cómo se trabaja con personas **solo para acompañar**:

- órdenes claras
- causa de un salto de paso
- no dejar ambigüedad

Está prohibido usar ese conocimiento para dañar, desestabilizar o engañar.

Los incentivos de producto se diseñan en una campaña futura, no se improvisan aquí.

---

## Auditoría de repositorio (obligatoria en cada cierre)

1. Pedir `synccheck` en MOSh (o `git fetch` + comparar HEAD con `origin/main`).
2. Leer ficheros por **SHA** (`git show origin/main:archivo` o raw con SHA).
3. No basar un diagnóstico solo en `raw.githubusercontent.com/.../main/...`.
4. Si Poetry, README, CHANGELOG o comandos no coinciden: hotfix antes del siguiente bloque.

---

## Entrega de documentos (resumen)

- Fichero entero; tablas ya montadas; no “añade esta fila”.
- No remitir a un pegado anterior: volver a pegar.
- Cacho 1 = documento cerrado o aviso explícito; no cortar un spec a mitad sin decirlo.
- Completo: primero `mkdir` / `touch` / `code`.
- Breadcrumb de campaña en cada paso.
- Explicar los saltos de número de paso.

---

## Plantilla

### Interacción

| Hallazgo | Norma resultante | ¿Documentado en onboarding? |
|----------|------------------|-----------------------------|
| | | |

### Deuda técnica

| Ítem | Destino | Estado |
|------|---------|--------|
| | siguiente bloque / campaña / no aplica | |

### Campañas futuras (si salen en el grupo)

| Tema | Nota |
|------|------|
| | |

---

## Autoridad

Este documento es normativo para el cierre de grupos.

Un grupo no se considera cerrado sin esta revisión, aunque el código ya esté en main.