# Metodología de MetsuOS (MOS2)

**Versión del documento:** 1.3  
**Baseline de referencia:** v0.2.4  
**Estado:** Normativo

---

## Propósito

Este documento define **cómo se desarrolla, documenta y evoluciona MetsuOS**.

Su objetivo es:

- Evitar reinventar decisiones ya tomadas.
- Impedir que cambios futuros rompan funcionalidad existente.
- Unificar el trabajo entre el desarrollador humano y la asistencia por IA.
- Dar trazabilidad entre requisitos, diseño, código y pruebas.

Si existe conflicto entre este documento y el código, **se resuelve actualizando el código o la especificación de forma explícita**. No se improvisan excepciones silenciosas.

---

## Qué es MetsuOS (marco de referencia)

MetsuOS (MOS2) es un sistema operativo **simulado y modular** escrito en Python.

Características estructurales no negociables:

- Shell interactivo propio: **MOSh**.
- Núcleo en `moslib/`.
- Sistema de archivos simulado en `rootfs/`.
- Espacio personal por usuario del sistema anfitrión.
- Comandos como módulos Python independientes.
- **Todo pasa por mosLib**.
- No se permiten instalaciones arbitrarias de paquetes Python en comandos.
- Seguridad de imports obligatoria (solo biblioteca estándar + `moslib`).
- Accesibilidad de interfaz mandatoria (`docs/A11Y.md`).
- Agnóstico de plataforma (linux/native, macos/native, windows/git-bash, windows/wsl).

MetsuOS **no** pretende ser un kernel real ni un sustituto completo de un sistema operativo nativo. Es un entorno controlado, extensible y auditable.

---

## Por qué ECSS-light

La metodología de especificación se inspira en **ECSS-E-ST-40** (ingeniería de software de la ESA), adaptada a la escala de un proyecto alpha modular.

Se adopta de ECSS:

- Separación entre *qué* (requisitos) y *cómo* (diseño).
- Documentos con propósito claro y precedencia.
- Requisitos numerados y verificables.
- Control de interfaces.
- Baseline de release.

Se descarta de ECSS:

- La burocracia completa de un programa espacial.
- Documentación no mantenible para el tamaño actual del proyecto.

El resultado se denomina **ECSS-light** y vive en `docs/specs/`.

---

## Mapa de documentación

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| AGENTS.md | | | Entrada corta para agentes IA |
| CHANGELOG.md | | | Historial de releases |
| docs/ | | | Documentación del proyecto |
| | A11Y.md | | Política de accesibilidad |
| | a11y/ | | Declaración e informe A11Y |
| | AI_ONBOARDING.md | | Protocolo de trabajo para IA |
| | HUMAN_ONBOARDING.md | | Arranque para personas |
| | DEVELOPER_GUIDE.md | | Flujo práctico de desarrollo |
| | VERSIONING.md | | Versiones, tags y Poetry |
| | METHODOLOGY.md | | Este documento (normativo de proceso) |
| | ENVIRONMENTS.md | | Perfiles de entorno, Poetry y contexto de sesión |
| | STYLE_GUIDE.md | | Normas de código |
| | USER_MANUAL.md | | Manual de usuario formal |
| | plans/ | | Planes de campaña |
| | specs/ | | Especificaciones ECSS-light |
| | | 00-OVERVIEW.md | Mapa y reglas de las specs |
| | | 01-SSS-System-Specification.md | Especificación de sistema |
| | | 02-SRS-Software-Requirements.md | Requisitos software |
| | | 03-ICD-Interfaces-and-Command-Contract.md | Interfaces y contrato de comandos |
| | | 04-SEC-Security-Policy.md | Política de seguridad |
| | | 05-SDD-Architecture-and-Design.md | Arquitectura y diseño |
| | | 06-TEST-Verification-and-Validation.md | Verificación y validación |
| | | 07-SRelD-Release-Baseline.md | Baseline de release |
| | man/ | | Páginas man por comando |

### Precedencia

1. A11Y de interfaz (perfiles soportados) junto con normas de seguridad (`04-SEC`) y sistema (`01-SSS`).
2. Contrato de comandos e interfaces (`03-ICD`).
3. Requisitos software (`02-SRS`).
4. Diseño (`05-SDD`).
5. Código.
6. README y textos auxiliares.

El código debe cumplir las especificaciones. Si una mejora exige cambiar una norma, **primero se actualiza la spec** y después el código.

Si A11Y y SEC chocan, se sigue el procedimiento de `docs/A11Y.md` y `04-SEC`.

Versionado de producto y tags: `docs/VERSIONING.md`.

---

## Método de trabajo (humano + IA)

### Principios

- **No romper** lo que ya funciona.
- **Planes por fases**, no cambios masivos sin control.
- **Commits atómicos** y mensajes claros.
- **Tests como puerta de calidad** (incluidos en el arranque del sistema).
- La IA propone plan y código; el humano ejecuta, prueba y decide.
- Toda feature nueva debe poder explicarse contra una spec o contra este documento.
- Cada campaña amplia tiene plan en `docs/plans/YYYY-MM-DD-NN-slug.md` **antes** del código (salvo reconstrucciones).

### Contexto de sesión (multi-entorno)

Formato:

```text
Contexto: <sistema> / <entorno> / <rol>
```

Ejemplos: `macos/native/desarrollo`, `windows/git-bash/prueba`, `windows/wsl/ambos`.

Normas:

- Sin nombres de host ni rutas home personales en el repositorio público.
- La IA adapta comandos al contexto; si falta, pregunta.
- Detalle: `docs/ENVIRONMENTS.md`.

### Entrega de documentación por la IA

- Un archivo o sección completa en **un único bloque de texto** listo para copiar y pegar.
- Explicar en pocas líneas **qué ha cambiado** para validar leyendo.
- Evitar pedir al humano que reescriba tablas o párrafos largos a mano.
- Si una fase toca varias piezas, entregar **un paso cada vez**.
- **Encabezados sin numeración** (`## Título`, no `## 1. Título`).
- Si el archivo del repo aún tiene números, entregar el documento completo ya sin números.
- Si la versión nueva es más corta que la del repo (docs **o** código), comprobar que no se pierde contenido e informarlo. Prohibido resumir sin consultar.
- Si el documento no cabe en un mensaje, **cacho 1 sustituye todo el fichero**; los cachos siguientes se pegan **debajo**.
- Tablas de comandos del sistema: columna **Tipo** en orden alfabético; dentro de cada tipo, comandos en orden alfabético.
- Estructuras de directorios: tablas, una columna por nivel.
- Crear carpetas/ficheros: dar secuencia bash (`mkdir -p`, `touch`, editor).
- Cada paso de campaña lleva breadcrumb: campaña, grupo, bloque x/y, paso, progreso aproximado.
- Git, no funciones exclusivas de un forge.
- No usar la palabra «corrida»; decir «ejecución» o «pasada de tests».
- CHANGELOG: no dejar «Sin publicar» a criterio del humano.

Detalle operativo para agentes: `AGENTS.md` y `docs/AI_ONBOARDING.md`.

### Flujo estándar de una fase

1. Partir de `main` limpio y actualizado.
2. Crear rama `feature/<nombre-descriptivo>`.
3. Acordar un plan por fases (y escribirlo en `docs/plans/` si es campaña nueva).
4. Implementar **solo** la fase actual.
5. Ejecutar tests (`./mos2.sh` / `test`, o Poetry según entorno) y/o arranque de MOSh.
6. Commit atómico.
7. Pasar a la siguiente fase.
8. Al terminar el conjunto: merge a `main` y aplicar `docs/VERSIONING.md`.

### Ramas

- `main` → estable, siempre usable.
- `feature/...` → trabajo en curso.
- `backup/YYYYMMDD_HHMMSS` → generadas por el comando `update`; locales, no producto.

### Commits

| Prefijo | Uso |
|---------|-----|
| feat: | Nueva funcionalidad |
| fix: | Corrección |
| docs: | Documentación |
| test: | Tests |
| refactor: | Cambio interno sin cambiar comportamiento |
| chore: | Mantenimiento, tooling, limpieza |

### Rol de la IA

La IA debe:

- Analizar el estado real del repositorio antes de proponer cambios.
- Entregar planes por fases con código/docs listos para pegar.
- Respetar normas férreas (seguridad, contrato de comandos, mosLib, A11Y).
- Respetar `docs/ENVIRONMENTS.md`, `docs/VERSIONING.md` y el contexto de sesión.
- Entregar documentos en un solo bloque copiable; resumir el diff.
- No inventar features como si ya existieran.
- Advertir riesgos de regresión.
- Representar estructuras de directorios como tablas (una columna por nivel).
- No numerar encabezados de documentación.
- Poner breadcrumb de campaña en cada paso.

El humano debe:

- Ejecutar los pasos.
- Verificar en el perfil de entorno que corresponda.
- Rechazar o corregir lo que no encaje.
- Hacer los commits y merges.

### Regla de no regresión

Antes de mergear a `main`:

1. Tests en verde.
2. Arranque de MOSh sin bloqueo por tests.
3. Smoke-test: `help`, `version`, `test`, y el comando nuevo si aplica.
4. No desactivar seguridad ni tests de arranque para hacer pasar un cambio.

### Actualización del repositorio local

- Preferir el comando de sistema `update` (incluye alineación de tags con origin).
- `mos2_forced_update.sh` solo como emergencia.
- Las ramas `backup/*` son red de seguridad local.
- Solo Git; no APIs de un forge.

---

## Ciclo de vida de una funcionalidad

Idea → impacto en SSS / SRS / SEC / ICD / A11Y (si aplica) → diseño breve (SDD si cambia arquitectura) → implementación en rama feature → tests → documentación (USER_MANUAL / man / README / ENVIRONMENTS / onboarding / declaración A11Y si aplica) → merge a main → VERSIONING (bump/tag si es producto) → mención en SRelD si la baseline lo requiere.

No se implementa una feature solo en código si rompe una norma documentada.

---

## Seguridad, accesibilidad y calidad como parte del proceso

- Validación de imports obligatoria en carga de comandos.
- Batería de tests al arrancar MOSh; si falla, no inicia.
- Comandos de usuario sujetos a seguridad y a revisión en arranque del usuario actual.
- A11Y mandatoria; tests A11Y e informe cuando existan en 0.2.5.
- Conflicto A11Y/SEC: procedimiento escrito; no excepción silenciosa.

---

## Documentos de usuario, desarrollador e IA

- Manual: `docs/USER_MANUAL.md`
- Humano: `docs/HUMAN_ONBOARDING.md`
- Desarrollador: `docs/DEVELOPER_GUIDE.md`
- IA: `AGENTS.md` y `docs/AI_ONBOARDING.md`
- Entornos: `docs/ENVIRONMENTS.md`
- Versionado: `docs/VERSIONING.md`
- Accesibilidad: `docs/A11Y.md`, `docs/a11y/DECLARACION.md`, `docs/a11y/informe.md`
- Planes: `docs/plans/`
- Páginas man: `docs/man/<comando>.md`
- Comando `man`: muestra esas páginas en el shell.
- Comando `docs`: lista y muestra `docs/` (baseline 0.2.5).
- Comando `a11y`: validación A11Y e informe (baseline 0.2.5).

Todo comando de sistema nuevo debería incorporar su página man en el mismo cambio (o en el inmediato de la misma fase).

---

## Estilo de código

Las normas de escritura están en `docs/STYLE_GUIDE.md`.

Este documento obliga a respetar la guía, mantener tests de contrato/normas críticas y no introducir excepciones ad hoc sin actualizar la guía.

---

## Representación de estructuras de directorios

Las estructuras de directorios siempre se representan como tablas markdown, con una columna por nivel y una columna final de descripción.

Está prohibido usar árboles ASCII como forma principal en documentos normativos.

---

## Baseline y evolución

- Baseline funcional de partida de este marco: v0.2.1.
- Producto actual de referencia: v0.2.4.
- Cierre A11Y de esta campaña: v0.2.5 previsto.
- Cada release relevante actualiza `docs/specs/07-SRelD-Release-Baseline.md`.
- Tags solo-docs: `vX.Y.Z-docs` o `vX.Y.Z-docs.N` con la Poetry vigente (detalle fino de VERSIONING: deuda de cierre).

---

## Cierre de grupo de bloques

Al terminar un grupo de bloques de una campaña:

- Revisión de interacción humano↔IA (incidentes → normas).
- Deuda técnica (hecho / siguiente bloque / no aplica).
- Secciones nuevas si hacen falta.

Plantilla formal: Grupo III de la campaña 05 (`docs/INTERACTION_REVIEW.md`).

---

## Resumen operativo (checklist rápido)

1. ¿Parto de main actualizado?
2. ¿Tengo rama feature/...?
3. ¿Contexto de sesión declarado si hay multi-entorno?
4. ¿El cambio respeta SEC + SSS + ICD + A11Y?
5. ¿Hay tests?
6. ¿El arranque sigue pasando?
7. ¿Documenté lo necesario?
8. ¿VERSIONING aplicado (bump o explícitamente no)?
9. ¿Commit claro y atómico?
10. ¿Estructuras de directorios en tabla?
11. ¿Encabezados de docs sin numeración?
12. ¿Plan de campaña en docs/plans si aplica?

Si alguna respuesta es no y el cambio es relevante, no se mergea.

---

## Autoridad de este documento

METHODOLOGY.md es normativo para el proceso de desarrollo de MetsuOS.

Cualquier excepción debe documentarse explícitamente, nunca como práctica silenciosa.