# Metodología de MetsuOS (MOS2)

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.2  
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
| docs/ | | | Documentación del proyecto |
| | AI_ONBOARDING.md | | Protocolo de trabajo para IA |
| | HUMAN_ONBOARDING.md | | Arranque para personas |
| | DEVELOPER_GUIDE.md | | Flujo práctico de desarrollo |
| | VERSIONING.md | | Versiones, tags y Poetry |
| | METHODOLOGY.md | | Este documento (normativo de proceso) |
| | ENVIRONMENTS.md | | Perfiles de entorno, Poetry y contexto de sesión |
| | STYLE_GUIDE.md | | Normas de código |
| | USER_MANUAL.md | | Manual de usuario formal |
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

1. Normas de seguridad (`04-SEC`) y sistema (`01-SSS`).
2. Contrato de comandos e interfaces (`03-ICD`).
3. Requisitos software (`02-SRS`).
4. Diseño (`05-SDD`).
5. Código.
6. README y textos auxiliares.

El código debe cumplir las especificaciones. Si una mejora exige cambiar una norma, **primero se actualiza la spec** y después el código.

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
- Si la versión nueva es más corta que la del repo, comprobar que no se pierde norma e informarlo.
- Tablas de comandos del sistema: columna **Tipo** en orden alfabético; dentro de cada tipo, comandos en orden alfabético.
- Estructuras de directorios: tablas, una columna por nivel.

Detalle operativo para agentes: `AGENTS.md` y `docs/AI_ONBOARDING.md`.

### Flujo estándar de una fase

1. Partir de `main` limpio y actualizado.
2. Crear rama `feature/<nombre-descriptivo>`.
3. Acordar un plan por fases.
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
- Respetar normas férreas (seguridad, contrato de comandos, mosLib).
- Respetar `docs/ENVIRONMENTS.md`, `docs/VERSIONING.md` y el contexto de sesión.
- Entregar documentos en un solo bloque copiable; resumir el diff.
- No inventar features como si ya existieran.
- Advertir riesgos de regresión.
- Representar estructuras de directorios como tablas (una columna por nivel).
- No numerar encabezados de documentación.

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

- Preferir el comando de sistema `update`.
- `mos2_forced_update.sh` solo como emergencia.
- Las ramas `backup/*` son red de seguridad local.

---

## Ciclo de vida de una funcionalidad

Idea → impacto en SSS / SRS / SEC / ICD (si aplica) → diseño breve (SDD si cambia arquitectura) → implementación en rama feature → tests → documentación (USER_MANUAL / man / README / ENVIRONMENTS / onboarding si aplica) → merge a main → VERSIONING (bump/tag si es producto) → mención en SRelD si la baseline lo requiere.

No se implementa una feature solo en código si rompe una norma documentada.

---

## Seguridad y calidad como parte del proceso

- Validación de imports obligatoria en carga de comandos.
- Batería de tests al arrancar MOSh; si falla, no inicia.
- Comandos de usuario sujetos a seguridad y a revisión en arranque del usuario actual.

---

## Documentos de usuario, desarrollador e IA

- Manual: `docs/USER_MANUAL.md`
- Humano: `docs/HUMAN_ONBOARDING.md`
- Desarrollador: `docs/DEVELOPER_GUIDE.md`
- IA: `AGENTS.md` y `docs/AI_ONBOARDING.md`
- Entornos: `docs/ENVIRONMENTS.md`
- Versionado: `docs/VERSIONING.md`
- Páginas man: `docs/man/<comando>.md`
- Comando `man`: muestra esas páginas en el shell.

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
- Producto actual de referencia: v0.2.2.
- Evolución de entornos/Poetry portable y onboarding se documenta sin reescribir la historia del producto.
- Cada release relevante actualiza `docs/specs/07-SRelD-Release-Baseline.md`.

---

## Resumen operativo (checklist rápido)

1. ¿Parto de main actualizado?
2. ¿Tengo rama feature/...?
3. ¿Contexto de sesión declarado si hay multi-entorno?
4. ¿El cambio respeta SEC + SSS + ICD?
5. ¿Hay tests?
6. ¿El arranque sigue pasando?
7. ¿Documenté lo necesario?
8. ¿VERSIONING aplicado (bump o explícitamente no)?
9. ¿Commit claro y atómico?
10. ¿Estructuras de directorios en tabla?
11. ¿Encabezados de docs sin numeración?

Si alguna respuesta es no y el cambio es relevante, no se mergea.

---

## Autoridad de este documento

METHODOLOGY.md es normativo para el proceso de desarrollo de MetsuOS.

Cualquier excepción debe documentarse explícitamente, nunca como práctica silenciosa.