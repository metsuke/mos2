# 00 – Overview de especificaciones (ECSS-light)

**Versión del documento:** 1.4  
**Baseline de referencia:** v0.2.4  
**Estado:** Normativo  
**Documento relacionado:** docs/METHODOLOGY.md, docs/ENVIRONMENTS.md, docs/VERSIONING.md, docs/A11Y.md, CHANGELOG.md, AGENTS.md

---

## Propósito

Este documento es el mapa de las especificaciones de MetsuOS.

Define:

- Qué documentos forman el conjunto ECSS-light
- Para qué sirve cada uno
- En qué orden se leen y se actualizan
- Qué autoridad tiene cada tipo de norma

No describe el diseño detallado ni los requisitos individuales: solo organiza el marco.

---

## Conjunto de especificaciones

| Nivel 1 | Nivel 2 | Nivel 3 | Documento | Función |
|---------|---------|---------|-----------|---------|
| docs/ | specs/ | 00-OVERVIEW.md | Overview | Mapa y reglas del set de specs |
| docs/ | specs/ | 01-SSS-System-Specification.md | SSS | Qué es el sistema y normas no negociables |
| docs/ | specs/ | 02-SRS-Software-Requirements.md | SRS | Requisitos software numerados y verificables |
| docs/ | specs/ | 03-ICD-Interfaces-and-Command-Contract.md | ICD | Interfaces internas y contrato de comandos |
| docs/ | specs/ | 04-SEC-Security-Policy.md | SEC | Política de seguridad de imports y validaciones |
| docs/ | specs/ | 05-SDD-Architecture-and-Design.md | SDD | Arquitectura y diseño alineados con el código |
| docs/ | specs/ | 06-TEST-Verification-and-Validation.md | TEST | Estrategia de verificación y validación |
| docs/ | specs/ | 07-SRelD-Release-Baseline.md | SRelD | Baseline de release |

Documentos de soporte fuera de `specs/`:

| Nivel 1 | Nivel 2 | Función |
|---------|---------|---------|
| AGENTS.md | | Entrada corta para agentes IA |
| CHANGELOG.md | | Historial de cambios por release |
| docs/ | A11Y.md | Política de accesibilidad |
| docs/ | a11y/ | Declaración e informe A11Y |
| docs/ | AI_ONBOARDING.md | Protocolo de trabajo para IA |
| docs/ | HUMAN_ONBOARDING.md | Arranque para personas |
| docs/ | DEVELOPER_GUIDE.md | Flujo práctico de desarrollo |
| docs/ | VERSIONING.md | Versiones, tags y Poetry |
| docs/ | METHODOLOGY.md | Método de trabajo y proceso |
| docs/ | ENVIRONMENTS.md | Perfiles de entorno, Poetry y contexto de sesión |
| docs/ | STYLE_GUIDE.md | Normas de estilo de código |
| docs/ | USER_MANUAL.md | Manual de usuario formal |
| docs/ | man/ | Páginas man por comando |
| docs/ | plans/ | Planes de campaña |

---

## Precedencia normativa

De mayor a menor autoridad técnica:

1. A11Y de interfaz (perfiles soportados) junto con `04-SEC` y `01-SSS`
2. `03-ICD` (contratos e interfaces)
3. `02-SRS` (requisitos software)
4. `05-SDD` (diseño)
5. Código fuente
6. `USER_MANUAL`, páginas `man`, README

Regla:

- El código debe cumplir SEC, SSS, ICD, SRS y A11Y.
- Si A11Y y SEC chocan, se aplica el procedimiento de SEC y A11Y.md. No hay excepción silenciosa.
- Si un cambio de código exige alterar una norma, primero se actualiza la spec y después el código.
- Tags y bump de Poetry: `docs/VERSIONING.md`.
- Relato de releases: `CHANGELOG.md`.

---

## Relación con ECSS

Este conjunto es una adaptación ligera de ECSS-E-ST-40:

| ECSS | MetsuOS ECSS-light |
|------|--------------------|
| SSS | 01-SSS |
| SRS | 02-SRS |
| ICD | 03-ICD |
| SDD | 05-SDD |
| V&V / test planning | 06-TEST |
| SRelD | 07-SRelD |

La seguridad tiene documento propio (`04-SEC`). La accesibilidad tiene política y declaración propias (`docs/A11Y.md`, `docs/a11y/`).

---

## Cómo se usa este set en el desarrollo

### Para implementar una feature

1. Comprobar impacto en SSS / SEC / ICD / SRS / A11Y (y ENVIRONMENTS si afecta a perfiles o Poetry).
2. Si cambia arquitectura, actualizar SDD.
3. Implementar en rama `feature/...`.
4. Añadir o ajustar tests según 06-TEST y STYLE_GUIDE.
5. Actualizar manual/man/README/onboarding/CHANGELOG/declaración si afecta a uso, proceso, release o cumplimiento A11Y.
6. Merge solo con tests en verde.
7. Aplicar VERSIONING (bump/tag si es producto).

### Para revisar un cambio

Preguntas mínimas:

1. ¿Rompe SEC?
2. ¿Excluye un perfil A11Y?
3. ¿Rompe el contrato de comando (ICD)?
4. ¿Queda trazado a algún requisito (SRS) o es solo refactor?
5. ¿Los tests lo cubren?
6. ¿Hay que tocar SRelD en la siguiente baseline?
7. ¿Hay que bump de Poetry o es solo docs?
8. ¿Hay que anotar CHANGELOG?

---

## Identificación de requisitos

En `02-SRS` los requisitos se numeran así:

```text
REQ-<AREA>-<NNN>
```

| Área | Significado |
|------|-------------|
| SYS | Sistema |
| CMD | Comandos |
| USER | Espacio de usuario |
| SEC | Seguridad |
| BOOT | Arranque |
| TEST | Pruebas |
| DOC | Documentación |
| UPD | Actualización |
| PLAT | Plataforma / entornos |
| A11Y | Accesibilidad |

Ejemplo: `REQ-SEC-001`

Cada requisito debe ser verificable por test, inspección o demostración.

---

## Baseline

La baseline documental de partida de este marco es **v0.2.1**.  
Producto de referencia actual: **v0.2.4**.  
Siguiente cierre de producto de esta campaña (A11Y runtime + tests + docs CLI): **v0.2.5**.

`07-SRelD` describe la baseline.  
`CHANGELOG.md` resume las evoluciones.  
`docs/a11y/DECLARACION.md` e `informe.md` describen el cumplimiento A11Y adaptado a CLI.

---

## Norma de representación de directorios

En todos los documentos de `docs/specs/` las estructuras de directorios se escriben como tablas, con una columna por nivel.

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| moslib/ | | | Núcleo |
| | core/ | | Componentes principales |
| | | shell.py | Shell MOSh |

---

## Estado de este overview

Este overview es normativo para la organización de las especificaciones.

Cualquier alta, baja o renombrado de documentos del set ECSS-light (o de soporte como ENVIRONMENTS, VERSIONING, CHANGELOG, A11Y, planes u onboarding) debe reflejarse aquí.