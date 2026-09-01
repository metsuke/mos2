# Incentivos y dirección de MetsuOS

**Versión del documento:** 1.1  
**Estado:** Normativo de dirección  
**No implementa código.**  
**Documentos relacionados:** docs/A11Y.md, docs/specs/04-SEC-Security-Policy.md, docs/AI_ONBOARDING.md, AGENTS.md, docs/INTERACTION_REVIEW.md, docs/DEUDA_Y_CAMPANAS.md, docs/plans/2026-08-31-01-incentivos-desarrollo-datos.md, docs/plans/2026-09-01-01-macro-apps-tareas-suite-rgpd-malla.md

---

## Propósito

Orientar las acciones de tres perfiles (usuario, desarrollador, IA) con un impulso leve **además** de las normas férreas.

No hay karma, ranking ni castigo. No se puntúa a las personas.

---

## Qué es mandatorio para todos

Esto **no** es incentivo. No se “inclina”. Si falta, el cambio **no se acepta** en el proceso de desarrollo y el código **no se ejecuta**.

| Norma | Dónde está |
|-------|------------|
| Accesibilidad de interfaz | docs/A11Y.md, declaración, tests a11y |
| Seguridad de imports y contrato de comando | SEC, cmd_loader |
| Tests de arranque | núcleo |
| No pisar comandos de sistema | user.py / cmd_loader |
| Resto de normas no negociables del SSS | docs/specs/01-SSS-… |

Humanos e IA están sujetos a esta tabla por igual.

---

## Qué es incentivo (solo aquí se “inclina”)

Vectores de dirección (inclusión amplia de producto, ciencia, comunicación, productividad de método, cadena de suministro, geo como rumbo, soberanía, capas legales, saber ⚫→⚪, automatizar lo repetitivo, andamiaje).

- **Humano:** el sistema pone fácil lo alineado (defaults, help, checklists). No hay examen ni ranking.
- **IA:** cumplir INCENTIVOS **más** las férreas es mandatorio.

---

## Vectores comunes

| Vector | A favor | En contra |
|--------|---------|-----------|
| Inclusión / A11Y de producto | No dejar fuera un perfil declarado | Producto solo para quien “ve y pulsa bien” |
| Ciencia | Spec, evidencia, tests | Parche mágico sin norma |
| Comunicación bidireccional | Explicar; el humano valida | Imponer o no poder discrepar |
| Productividad de método | Un paso, un fichero, SHA real | Chat que agota para el mismo commit |
| Experiencia (juego / MOSh) | Texto lineal, help/man | CLI hostil |
| Cadena de suministro | Licencia visible, SBOM cuando exista | Dependencia opaca, telemetría no consentida |
| Geoestrategia de paquetes | Dirección: origen visible (moslib ↔ Poetry) | “Lo que pille PyPI” |
| Soberanía | Datos y modelos bajo el usuario; `.mos` local | Silo de nube |
| Capas legales | Declarar capa (este repo: GPL-3.0) | Mezclar capas en silencio |
| Saber (⚫→⚪) | Etiquetar **textos** | Puntuar **personas** |
| Automatizar lo repetitivo | Liberar para crear | Automatizar el juicio o el merge |
| Andamiaje | Poetry debajo; moslib encima | Inventar el stack en cada paso |

**Geoestrategia:** rumbo, no código. Comandos de esta baseline: sin imports ajenos (SEC). DepManager = campaña propia.

La fila Inclusión/A11Y como vector **no** debilita la tabla férrea: el mínimo A11Y de docs/A11Y.md es puerta de entrada; el vector empuja a no quedarse en el mínimo.

---

## Actuaciones deseadas por perfil

### Usuario

Inclinar a: `.mos`, `user_*` que no pisan sistema, help/man/docs, no meter secretos en el árbol versionado.

Sigue obligado a A11Y/SEC si publica o ejecuta comandos: un `user_*` con import ilegal o interfaz que rompa A11Y **no corre**.

### Desarrollador

Inclinar a: feature, tests, synccheck, README/SSS/man con comando nuevo, no acortar specs, Git no forge.

Sigue obligado: sin A11Y no hay accept ni merge usable; sin SEC no hay arranque.

### IA

Mandatorio: férreas + este archivo + onboarding de entrega.

- No dañar, no engañar, no desestabilizar.
- Psicología solo para acompañar.
- No specs fantasmas ni “lo que te di antes”.
- No apagar tests ni A11Y para cerrar un paso.
- No volcar `.mos` a un servicio remoto.
- No proponer aceptar código que falle A11Y.

---

## Leyes de Asimov (cita + aplicación)

Aplican a la **IA**. “Robot” = ese agente.

1. Un robot no puede dañar a un ser humano o, por inacción, permitir que un ser humano sufra daño.
2. Un robot debe obedecer las órdenes dadas por los seres humanos, excepto cuando esas órdenes entren en conflicto con la Primera Ley.
3. Un robot debe proteger su propia existencia en la medida en que esa protección no entre en conflicto con la Primera o la Segunda Ley.

Aplicación: daño incluye engaño, exclusión A11Y y corromper datos; obedecer = lo que el humano valida, no autocommit; existencia ≠ apagar tests. Lo bidireccional se itera después.

---

## Psicología

Solo acompañar. Prohibido dañar, desestabilizar o engañar.

---

## Fuera de este documento

- Código de suite, API, apps, colas (07+)
- DepManager geo real

---

## Autoridad

Normativo de **dirección** en la parte incentivo. Las férreas mandan siempre. Conflicto: A11Y y SEC ganan; se documenta.