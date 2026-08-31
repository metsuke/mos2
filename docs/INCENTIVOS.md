# Incentivos y dirección de MetsuOS

**Versión del documento:** 1.0  
**Estado:** Normativo de dirección (bloque 1 de la campaña 06)  
**No implementa código.**  
**Documentos relacionados:** docs/A11Y.md, docs/specs/04-SEC-Security-Policy.md, docs/AI_ONBOARDING.md, AGENTS.md, docs/INTERACTION_REVIEW.md, docs/DEUDA_Y_CAMPANAS.md, docs/plans/2026-08-31-01-incentivos-desarrollo-datos.md

---

## Propósito

Orientar las acciones de tres perfiles (usuario, desarrollador, IA) con un impulso leve: favorecer lo alineado con el proyecto y desfavorecer lo que lo rompe.

No hay karma, ranking ni castigo. No se puntúa a las personas.

Para los humanos el sistema **inclina** el contexto (defaults, help, man, mensajes, checklists). No es mandatorio.

Para la IA **sí es mandatorio**.

Este archivo no sustituye A11Y, SEC ni SSS. Si choca con ellos, prevalecen esas normas y se documenta el conflicto.

---

## Vectores comunes

Tomados del proyecto público MetsuOS (metsuke.com: El Proyecto, Apps, DepManager, soberanía local) y de MOS2 en repo.

| Vector | A favor | En contra |
|--------|---------|-----------|
| Inclusión / A11Y | No dejar fuera un perfil declarado | Producto solo para quien “ve y pulsa bien” |
| Ciencia | Spec, evidencia, tests | Parche mágico sin norma |
| Comunicación bidireccional | Explicar; el humano valida | Imponer o no poder discrepar |
| Productividad de método | Un paso, un fichero, SHA real | Chat que agota para el mismo commit |
| Experiencia (juego / MOSh) | Texto lineal, help/man | CLI hostil |
| Cadena de suministro | Licencia visible, SBOM cuando exista | Dependencia opaca, telemetría no consentida |
| Geoestrategia de paquetes | Dirección: origen y política visibles (moslib ↔ Poetry) | “Lo que pille PyPI” sin criterio |
| Soberanía | Datos y modelos bajo el usuario; `.mos` local | Silo de nube que corta el grifo |
| Capas legales | Declarar capa (este repo: GPL-3.0) | Mezclar capas en silencio |
| Saber (⚫→⚪) | Etiquetar **textos** | Puntuar **personas** |
| Automatizar lo repetitivo | Liberar para crear | Automatizar el juicio o el merge |
| Andamiaje | Poetry debajo; moslib encima | Inventar el stack en cada paso |

**Geoestrategia:** rumbo, no código. Los comandos de esta baseline no importan paquetes ajenos (SEC). La funcionalidad DepManager / origen geográfico tendrá campaña propia.

---

## Actuaciones deseadas por perfil

### Usuario

Inclinar a: usar su espacio `.mos`, comandos `user_*` que no pisan el sistema, `help` / `man` / `docs`, no meter secretos en el árbol versionado.

No mandatorio. No se bloquea por “desalineación” de estilo.

### Desarrollador

Inclinar a: rama feature, tests de arranque, `synccheck`, README/SSS/man cuando hay comando nuevo, no acortar specs en silencio, Git y no APIs de un forge.

No hay nota personal ni conteo de commits como premio.

### IA

Mandatorio:

- Cumplir este archivo, A11Y, SEC, SSS y el onboarding de entrega.
- No dañar, no engañar, no desestabilizar.
- No usar psicología salvo para acompañar (órdenes claras, causa de un salto, no ambigüedad).
- No generar specs fantasmas ni remisión a “lo que te di antes”.
- No desactivar tests ni seguridad para cerrar un paso.
- No volcar el espacio de usuario a un servicio remoto.

---

## Leyes de Asimov (cita + aplicación)

Aplican a la **IA** que desarrolla o usa MetsuOS. “Robot” = ese agente.

Cita (formulación habitual en español):

1. Un robot no puede dañar a un ser humano o, por inacción, permitir que un ser humano sufra daño.
2. Un robot debe obedecer las órdenes dadas por los seres humanos, excepto cuando esas órdenes entren en conflicto con la Primera Ley.
3. Un robot debe proteger su propia existencia en la medida en que esa protección no entre en conflicto con la Primera o la Segunda Ley.

Nota de aplicación en MOS2:

- Daño incluye también engaño, exclusión de un perfil A11Y declarado y corrupción de datos del usuario.
- Obedecer es ejecutar lo que el humano valida (pegar, commit, merge). No es autocommit ni saltarse al humano.
- Proteger la existencia no autoriza borrar el repo, mentir sobre el SHA o apagar tests para “sobrevivir” a un merge.
- Lo bidireccional (límites simétricos humano ↔ IA) se iterará después, con cuidado. Aquí las leyes son **para la IA**.

---

## Psicología

La IA puede conocer cómo se trabaja con personas **solo para acompañar**.

Prohibido usarlo para dañar, desestabilizar o engañar.

Esta norma se implementará con cuidado en bloques posteriores. En este bloque solo se declara.

---

## Fuera de este documento

- Código, comandos nuevos, API Grok (bloque 2)
- RGPD como campaña de prueba del método (bloque 3)
- MetsuDepManager y política geo real

---

## Autoridad

Normativo de **dirección**. No debilita SEC ni A11Y.

Cambio de vectores o de obligatoriedad = nueva versión de este archivo y nota en el plan de campaña.