# 00 – Overview de especificaciones (ECSS-light)

**Versión del documento:** 1.1  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo  
**Documento relacionado:** docs/METHODOLOGY.md, docs/ENVIRONMENTS.md

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
| docs/ | specs/ | 07-SRelD-Release-Baseline.md | SRelD | Baseline de release (v0.2.1 y siguientes) |

Documentos de soporte fuera de `specs/`:

| Nivel 1 | Nivel 2 | Función |
|---------|---------|---------|
| docs/ | METHODOLOGY.md | Método de trabajo y proceso |
| docs/ | ENVIRONMENTS.md | Perfiles de entorno, Poetry y contexto de sesión |
| docs/ | STYLE_GUIDE.md | Normas de estilo de código |
| docs/ | USER_MANUAL.md | Manual de usuario formal |
| docs/ | man/ | Páginas man por comando |

---

## Precedencia normativa

De mayor a menor autoridad técnica:

1. `04-SEC` y `01-SSS` (seguridad y normas de sistema)
2. `03-ICD` (contratos e interfaces)
3. `02-SRS` (requisitos software)
4. `05-SDD` (diseño)
5. Código fuente
6. `USER_MANUAL`, páginas `man`, README

Regla:

- El código debe cumplir SEC, SSS, ICD y SRS.
- Si un cambio de código exige alterar una norma, primero se actualiza la spec y después el código.
- No se aceptan excepciones silenciosas.

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

Adicionalmente, MetsuOS eleva la seguridad a documento propio (`04-SEC`) por ser norma férrea del sistema.

---

## Cómo se usa este set en el desarrollo

### Para implementar una feature

1. Comprobar impacto en SSS / SEC / ICD / SRS (y ENVIRONMENTS si afecta a perfiles o Poetry).
2. Si cambia arquitectura, actualizar SDD.
3. Implementar en rama `feature/...`.
4. Añadir o ajustar tests según 06-TEST y STYLE_GUIDE.
5. Actualizar manual/man/README si afecta a uso.
6. Merge solo con tests en verde.

### Para revisar un cambio

Preguntas mínimas:

1. ¿Rompe SEC?
2. ¿Rompe el contrato de comando (ICD)?
3. ¿Queda trazado a algún requisito (SRS) o es solo refactor?
4. ¿Los tests lo cubren?
5. ¿Hay que tocar SRelD en la siguiente baseline?

---

## Identificación de requisitos

En `02-SRS` los requisitos se numeran así:

```text
REQ-<AREA>-<NNN>
```

Áreas habituales:

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

Ejemplo: `REQ-SEC-001`

Cada requisito debe ser verificable por test, inspección o demostración.

---

## Baseline

La baseline documental y funcional de partida de este marco es **v0.2.1**.

`07-SRelD` describe qué contiene esa baseline y registra evoluciones posteriores (incluidos entornos/Poetry portable).

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

Cualquier alta, baja o renombrado de documentos del set ECSS-light (o de soporte como ENVIRONMENTS) debe reflejarse aquí.