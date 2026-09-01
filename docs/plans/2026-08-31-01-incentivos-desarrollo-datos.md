# Plan de campaña 06 — incentivos, desarrollo en MOS2, datos

**Fecha del plan:** 2026-08-31  
**Orden del día:** 01  
**Producto de partida:** 0.2.5  
**Estado:** En curso (bloque 1)

---

## Propósito

1. Documentar una filosofía de trabajo (vectores + actuaciones por rol) sin karma ni castigo.
2. Más adelante, meter el proceso de campaña dentro de MOS2, con API Grok bajo política.
3. Probar ese método integrando protección de datos (RGPD / LOPDGDD).

No se implementa DepManager ni geoestrategia de paquetes en esta campaña. Eso es dirección y tendrá campaña propia (moslib ↔ Poetry).

---

## Decisiones ya tomadas

| Tema | Decisión |
|------|----------|
| Forma | Tres bloques, no tres fases sueltas |
| Karma / ranking | No |
| Humanos (solo incentivos) | El sistema inclina; no es examen |
| Normas férreas (A11Y, SEC, SSS) | Mandatorias para humano e IA |
| IA | Férreas + INCENTIVOS |
| Asimov | Cita de las tres leyes + nota de aplicación; solo para la IA |
| Psicología | Acompañar; prohibido dañar, desestabilizar o engañar; iterar con cuidado |
| Geo de paquetes | Dirección en INCENTIVOS; no código |
| Código en bloque 1 | Ninguno |

---

## Bloques

### Bloque 1 — documento

- docs/INCENTIVOS.md
- Enlaces en AGENTS.md, AI_ONBOARDING, DEUDA_Y_CAMPANAS, README (tabla de docs)
- Cierre I de interacción

### Bloque 2 — desarrollo en MOS2

- Comandos de campaña (plantillas, paso, handoff, cierre)
- Atomizar documentos generables (plantilla, no spec fantasma)
- API Grok: dato mínimo, sin volcar `.mos`, humano valida
- Tag de producto solo si hay runtime

### Bloque 3 — prueba con protección de datos

- Usar el loop del bloque 2
- Specs y mensajes de dato personal / espacio usuario
- No certificación legal en esta pasada

---

## Fuera de esta campaña

- Laboratorio de lectores de pantalla
- Dual Python + C
- MOS2 sin Python 3
- MetsuDepManager / política geo real sobre Poetry

---

## Criterio de cierre del bloque 1

INCENTIVOS.md en main, enlazado, sin ganchos de código nuevos, synccheck alineado.