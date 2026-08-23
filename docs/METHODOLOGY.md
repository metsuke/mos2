# Metodología de MetsuOS (MOS2)

**Versión del documento:** 1.0  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo

---

## 1. Propósito

Este documento define **cómo se desarrolla, documenta y evoluciona MetsuOS**.

Su objetivo es:

- Evitar reinventar decisiones ya tomadas.
- Impedir que cambios futuros rompan funcionalidad existente.
- Unificar el trabajo entre el desarrollador humano y la asistencia por IA.
- Dar trazabilidad entre requisitos, diseño, código y pruebas.

Si existe conflicto entre este documento y el código, **se resuelve actualizando el código o la especificación de forma explícita**. No se improvisan excepciones silenciosas.

---

## 2. Qué es MetsuOS (marco de referencia)

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
- Agnóstico de plataforma (Linux, macOS, Windows/Git Bash).

MetsuOS **no** pretende ser un kernel real ni un sustituto completo de un sistema operativo nativo. Es un entorno controlado, extensible y auditable.

---

## 3. Por qué ECSS-light

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

## 4. Mapa de documentación

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| docs/ | | | Documentación del proyecto |
| | METHODOLOGY.md | | Este documento (normativo de proceso) |
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
| | | clear.md | Manual de clear |
| | | echo.md | Manual de echo |
| | | help.md | Manual de help |
| | | man.md | Manual de man |
| | | sysinfo.md | Manual de sysinfo |
| | | test.md | Manual de test |
| | | update.md | Manual de update |
| | | uptime.md | Manual de uptime |
| | | version.md | Manual de version |

### Precedencia

1. Normas de seguridad (`04-SEC`) y sistema (`01-SSS`).
2. Contrato de comandos e interfaces (`03-ICD`).
3. Requisitos software (`02-SRS`).
4. Diseño (`05-SDD`).
5. Código.
6. README y textos auxiliares.

El código debe cumplir las especificaciones. Si una mejora exige cambiar una norma, **primero se actualiza la spec** y después el código.

---

## 5. Método de trabajo (humano + IA)

### 5.1 Principios

- **No romper** lo que ya funciona.
- **Planes por fases**, no cambios masivos sin control.
- **Commits atómicos** y mensajes claros.
- **Tests como puerta de calidad** (incluidos en el arranque del sistema).
- La IA propone plan y código; el humano ejecuta, prueba y decide.
- Toda feature nueva debe poder explicarse contra una spec o contra este documento.

### 5.2 Flujo estándar de una fase

1. Partir de `main` limpio y actualizado.
2. Crear rama `feature/<nombre-descriptivo>`.
3. Acordar un plan por fases.
4. Implementar **solo** la fase actual.
5. Ejecutar tests (`poetry run pytest` y/o arranque de MOSh).
6. Commit atómico.
7. Pasar a la siguiente fase.
8. Al terminar el conjunto: merge a `main`.

### 5.3 Ramas

- `main` → estable, siempre usable.
- `feature/...` → trabajo en curso.
- `backup/YYYYMMDD_HHMMSS` → generadas automáticamente por el comando `update` para preservar cambios locales antes de un reset forzado. Son locales, no se publican como producto.

### 5.4 Commits

Prefijos recomendados:

| Prefijo | Uso |
|---------|-----|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección |
| `docs:` | Documentación |
| `test:` | Tests |
| `refactor:` | Cambio interno sin cambiar comportamiento |
| `chore:` | Mantenimiento, tooling, limpieza |

Ejemplos:

docs: añadir METHODOLOGY.md
feat(commands): añadir comando man
test: validación de estilo y contrato de comandos
fix(security): rechazar imports relativos en comandos de usuario

### 5.5 Rol de la IA

La IA debe:

- Analizar el estado real del repositorio antes de proponer cambios.
- Entregar planes por fases con código listo para pegar.
- Respetar las normas férreas (seguridad, contrato de comandos, mosLib).
- No inventar features como si ya existieran.
- Advertir riesgos de regresión.
- Representar siempre las estructuras de directorios como tablas markdown, con una columna por nivel de directorio, para que sean fáciles de copiar y mantener.

El humano debe:

- Ejecutar los pasos.
- Verificar en máquina real.
- Rechazar o corregir lo que no encaje.
- Hacer los commits y merges.

### 5.6 Regla de no regresión

Antes de mergear a `main`:

1. `poetry run pytest` en verde.
2. Arranque de MOSh sin bloqueo por tests.
3. Comandos críticos smoke-test: `help`, `version`, `test`, y si aplica el comando nuevo.
4. No desactivar seguridad ni tests de arranque para hacer pasar un cambio.

### 5.7 Actualización del repositorio local

- Preferir el comando de sistema `update` (backup automático + sincronización con `origin/main`).
- `mos2_forced_update.sh` solo como recurso de emergencia.
- Las ramas `backup/*` se conservan como red de seguridad local (máximo controlado por el propio comando `update`).

---

## 6. Ciclo de vida de una funcionalidad

Idea
  → impacto en SSS / SRS / SEC / ICD (si aplica)
  → diseño breve (SDD si cambia arquitectura)
  → implementación en rama feature
  → tests (unitarios, seguridad, estilo, contrato)
  → documentación (USER_MANUAL / man / README si aplica)
  → merge a main
  → mención en SRelD en la siguiente baseline

No se implementa una feature solo en código si rompe una norma documentada.

---

## 7. Seguridad y calidad como parte del proceso

- La validación de imports es obligatoria en carga de comandos.
- La batería de tests se ejecuta al arrancar MOSh.
- Si falla cualquier test de arranque, el sistema no inicia.
- Los comandos de usuario también están sujetos a seguridad y, en arranque, a la revisión del usuario actual.

Estas reglas no son opcionales ni se diluyen por comodidad.

---

## 8. Documentos de usuario y páginas man

- Manual de usuario formal: docs/USER_MANUAL.md
- Páginas man por comando: docs/man/<comando>.md
- Comando de sistema man: lee esas páginas y las muestra en el shell.

Todo comando de sistema nuevo debería incorporar su página man en el mismo cambio (o en el inmediatamente siguiente de la misma fase documental/funcional).

---

## 9. Estilo de código

Las normas concretas de escritura de código están en docs/STYLE_GUIDE.md.

Este documento metodológico obliga a:

- Respetar la guía de estilo.
- Mantener tests que verifiquen el contrato de comandos y normas críticas.
- No introducir excepciones ad hoc sin actualizar la guía.

---

## 10. Representación de estructuras de directorios

Norma obligatoria para toda la documentación de MetsuOS (y para la asistencia por IA):

Las estructuras de directorios siempre se representan como tablas markdown, con una columna por nivel de directorio/archivo, más una columna final de descripción.

Ejemplo correcto:

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| moslib/ | | | Núcleo del sistema |
| | core/ | | Componentes principales |
| | | shell.py | Shell principal (MOSh) |
| | commands/ | | Comandos del sistema |

Está prohibido usar árboles ASCII como forma principal de documentar estructuras de directorios en los documentos normativos del proyecto.

---

## 11. Baseline y evolución

- La baseline funcional de partida de este marco documental es v0.2.1.
- Los cambios documentales y de proceso se integran sin reescribir la historia del producto.
- Cada release relevante actualiza docs/specs/07-SRelD-Release-Baseline.md.

---

## 12. Resumen operativo (checklist rápido)

Al trabajar en MetsuOS:

1. ¿Parto de main actualizado?
2. ¿Tengo rama feature/...?
3. ¿El cambio respeta SEC + SSS + ICD?
4. ¿Hay tests?
5. ¿El arranque sigue pasando?
6. ¿Documenté lo necesario (spec / man / manual / README)?
7. ¿Commit claro y atómico?
8. ¿Las estructuras de directorios están en forma de tabla?

Si alguna respuesta es no y el cambio es relevante, no se mergea.

---

## 13. Autoridad de este documento

METHODOLOGY.md es normativo para el proceso de desarrollo de MetsuOS.

Cualquier excepción debe documentarse explícitamente (preferiblemente en una actualización de este archivo o de la spec afectada), nunca como práctica silenciosa.