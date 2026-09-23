# 00 – Overview de especificaciones (ECSS-light)

**Versión del documento:** 1.7  
**Baseline de referencia:** v0.2.7 (árbol hacia v0.2.8)  
**Estado:** Normativo  
**Documento relacionado:** docs/METHODOLOGY.md, docs/ENVIRONMENTS.md, docs/VERSIONING.md, docs/A11Y.md, CHANGELOG.md, AGENTS.md, docs/INCENTIVOS.md, docs/INTERACTION_REVIEW.md, docs/DEUDA_Y_CAMPANAS.md

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
| docs/ | specs/ | 08-APPS.md | APPS | Apps locales, ámbitos y mini-moslib |
| docs/ | specs/ | 09-TASKS.md | TASKS | Tareas e hilos locales, worker de sesión |
| docs/ | specs/ | 10-IA-ROUTER.md | IA-ROUTER | Enrutador de modelos (off por defecto) |
| docs/ | specs/ | 11-INTEGRIDAD.md | INTEGRIDAD | Manifiesto, sello y arranque |

Documentos de soporte fuera de `specs/`:

| Nivel 1 | Nivel 2 | Función |
|---------|---------|---------|
| AGENTS.md | | Entrada corta para agentes IA |
| CHANGELOG.md | | Historial de cambios por release |
| docs/ | A11Y.md | Política de accesibilidad |
| docs/ | a11y/ | Declaración e informe A11Y |
| docs/ | AI_ONBOARDING.md | Protocolo de trabajo para IA |
| docs/ | HUMAN_ONBOARDING.md | Arranque para personas |
| docs/ | INCENTIVOS.md | Dirección de trabajo (vectores y roles) |
| docs/ | INTERACTION_REVIEW.md | Cierre de interacción y deuda |
| docs/ | DEUDA_Y_CAMPANAS.md | Deuda y campañas previstas |
| docs/ | DEVELOPER_GUIDE.md | Flujo práctico de desarrollo |
| docs/ | VERSIONING.md | Versiones, tags y Poetry |
| docs/ | METHODOLOGY.md | Método de trabajo y proceso |
| docs/ | ENVIRONMENTS.md | Perfiles de entorno, Poetry y contexto de sesión |
| docs/ | STYLE_GUIDE.md | Normas de estilo de código |
| docs/ | USER_MANUAL.md | Manual de usuario formal |
| docs/ | IA_WRITE.md | Lotes write/multi para IA |
| docs/ | man/ | Páginas man por comando |
| docs/ | plans/ | Planes de campaña |

---

## Precedencia normativa
De mayor a menor autoridad técnica:

1. A11Y de interfaz (perfiles soportados) junto con `04-SEC`, `01-SSS` y `11-INTEGRIDAD`
2. `03-ICD` (contratos e interfaces)
3. `02-SRS` (requisitos software)
4. `05-SDD` (diseño) y specs de capacidad `08-APPS`, `09-TASKS`, `10-IA-ROUTER`
5. Código fuente
6. `USER_MANUAL`, páginas `man`, README

Regla:

- El código debe cumplir SEC, SSS, ICD, SRS, A11Y e integridad.
- Si A11Y y SEC chocan, se aplica el procedimiento de SEC y A11Y.md. No hay excepción silenciosa.
- Si un cambio de código exige alterar una norma, primero se actualiza la spec y después el código.
- Tags y bump de Poetry: `docs/VERSIONING.md`.
- Relato de releases: `CHANGELOG.md`.
- Dirección de trabajo para IA: `docs/INCENTIVOS.md`.

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

La seguridad tiene documento propio (`04-SEC`). La accesibilidad tiene política y declaración propias (`docs/A11Y.md`, `docs/a11y/`). La integridad tiene `11-INTEGRIDAD`.

08, 09 y 10 no sustituyen a SSS/SRS/ICD: detallan capacidades ya reservadas o exigidas en el núcleo ECSS-light.

---

## Cómo se usa este set en el desarrollo
### Para implementar una feature

1. Comprobar impacto en SSS / SEC / ICD / SRS / A11Y / integridad (y ENVIRONMENTS si afecta a perfiles o Poetry).
2. Si cambia arquitectura, actualizar SDD. Si toca apps, tareas o iarouter, actualizar 08, 09 o 10.
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
9. ¿Hay que registrar integridad?

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
| APP | Apps |
| TASK | Tareas e hilos |
| IA | Enrutador de IA |
| INT | Integridad |

Ejemplo: `REQ-SEC-001`

Cada requisito debe ser verificable por test, inspección o demostración.

---

## Baseline
La baseline documental de partida de este marco es **v0.2.1**.  
Producto de referencia actual: **v0.2.7**.  
Árbol hacia **v0.2.8** (entrada en CHANGELOG; tag de producto pendiente de pruebas humanas).

`07-SRelD` describe la baseline.  
`CHANGELOG.md` resume las evoluciones.  
`docs/a11y/DECLARACION.md` e `informe.md` describen el cumplimiento A11Y adaptado a CLI.

Esta versión 1.6 del Overview no borra el relato de 1.5: actualiza el mapa (11-INTEGRIDAD) y mantiene la baseline de producto.

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

Cualquier alta, baja o renombrado de documentos del set ECSS-light (o de soporte como ENVIRONMENTS, VERSIONING, CHANGELOG, A11Y, INCENTIVOS, INTERACTION_REVIEW, DEUDA, planes u onboarding) debe reflejarse aquí.