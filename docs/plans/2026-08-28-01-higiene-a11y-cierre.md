# Campaña: higiene de scripts, A11Y mandatoria y bucle de cierre

**Fecha del plan:** 2026-08-28  
**NN del día:** 01  
**Estado:** Diseñada (pendiente de ejecutar)  
**Origen:** Acordado en chat; este documento es la fuente operativa  
**Contexto de trabajo previsto:** macos / native / desarrollo (declarar cambios)

**Documentos relacionados:** docs/plans/README.md, docs/VERSIONING.md, docs/METHODOLOGY.md, docs/ENVIRONMENTS.md, docs/AI_ONBOARDING.md, CHANGELOG.md, docs/specs/*

---

## Objetivo

1. Higiene de plataforma: scripts `.sh` en LF; Poetry en Git Bash solo con un invocador que realmente ejecute.
2. Accesibilidad **mandatoria** en política, perfiles de usuario, requisitos ECSS-light, mensajes de runtime y tests.
3. Planes de campaña versionados en `docs/plans/` (ya iniciado).
4. Al cerrar cada grupo: revisión de **interacción** humano↔IA y **deuda técnica**, con plantilla extensible.

## Fuera de alcance

- Interfaz gráfica
- Certificación WCAG de sitio web
- CI en GitHub Actions u otra
- i18n (el producto sigue en español)
- CHANGELOG generado solo desde git
- Copiar o mover clones WSL automáticamente
- Debilitar la validación AST de imports “para facilitar A11Y” sin acta

---

## Normas que no se improvisan en esta campaña

- A11Y no es opcional. Si A11Y y seguridad chocan, **prevalece A11Y** para no excluir perfiles declarados. El recorte de SEC se debate, se escriben riesgos y mitigaciones en SEC + A11Y + SRelD. Nunca excepción silenciosa.
- Entrega IA: **un paso**; docs largos **archivo completo**; tablas **ya cerradas**; encabezados **sin números**; si el doc nuevo es más corto, avisar qué se ha comprobado.
- Leer el repo antes de afirmar el estado de un fichero.
- Contexto de sesión si hay paths/Poetry/git en otra máquina.
- Bloques de **esta** campaña se numeran desde 0.
- Producto al inicio: Poetry **0.2.2**. No bump en pasos solo-docs.

---

## Precedencia (recordatorio)

1. A11Y de interfaz (perfiles soportados)  
2. SEC / SSS  
3. ICD  
4. SRS  
5. SDD  
6. Código  
7. README / planes  

Un conflicto 1 vs 2 no salta el debate: se documenta y luego se implementa.

---

## Grupo I — Higiene de plataforma

**Rama:** `feature/script-hygiene-lf-poetry`  
**Bump:** 0.2.2 → **0.2.3**  
**Tag:** `v0.2.3`  
**CHANGELOG:** entrada de producto 0.2.3

### Bloque 0

**0.1 Rama**

```text
git checkout main
git pull origin main
git checkout -b feature/script-hygiene-lf-poetry
```

**0.2 `.gitattributes`** (archivo completo en el paso de ejecución)

- `*.sh text eol=lf`
- Lo mínimo más para no reintroducir CRLF en scripts
- No convertir a la fuerza todo el repo binario

**0.3 `mos2.sh` e `install.sh`**

Orden Windows/Git Bash:

1. `py -m poetry` si `py -m poetry --version` funciona
2. `python -m poetry` / `python3 -m poetry` igual
3. `poetry.exe` **solo** si `poetry.exe --version` funciona
4. `poetry` último

Unix (macOS/Linux/WSL): sin cambio de política salvo alinear comentarios.

**0.4 `docs/ENVIRONMENTS.md` entero**

- Mismo orden que el código
- CRLF / LF
- Guard WSL `/mnt` (ya existe; no contradecirlo)

**0.5 Release higiene**

- Entrada CHANGELOG `## 0.2.3`
- `pyproject.toml` version `0.2.3`
- README línea de versión si aplica

**0.6 Merge**

```text
git checkout main && git pull origin main
git merge feature/script-hygiene-lf-poetry
git push origin main
git tag -a v0.2.3 -m "v0.2.3: LF en scripts y Poetry ejecutable en Git Bash"
git push origin v0.2.3
git branch -d feature/script-hygiene-lf-poetry
git push origin --delete feature/script-hygiene-lf-poetry
```

**Pruebas mínimas:** macos `./mos2.sh`; Git Bash no debe elegir un `.exe` con Permission denied; WSL Linux FS arranca.

### Cierre I (obligatorio)

Plantilla (la IA propone, el humano valida):

| Sección | Pregunta |
|---------|----------|
| Interacción | ¿Algún paso poco explícito, tabla a medias, rama en el clone equivocado? |
| Deuda técnica | ¿Alias a otro clone, CRLF residual, tag -docs desfasado, poetry.exe sin probar --version en install y mos2? |

Salida: nada / commit `docs:` / ítem al siguiente bloque. No saltarse aunque el grupo “haya ido fino”.

---

## Grupo II — A11Y mandatoria

A11Y = WCAG 2.2 principios + EN 301 549 / ISO 9241-171 **adaptados a CLI**. No se afirma conformidad web.

### Perfiles a documentar en Bloque 1 (mínimo)

| Perfil | Qué debe cubrir MetsuOS |
|--------|-------------------------|
| Solo teclado | Ya es el modelo; atajos y salida predecibles |
| Lector de pantalla de terminal | Texto plano, prefijos, sin significado solo-color |
| Baja visión | No depender de contraste ANSI; mensajes largos útiles |
| Daltonismo | Color no es la única señal |
| Carga cognitiva | help/man, errores con siguiente acción |
| Sordera / sin audio | CLI no depende de sonido (declarar N/A explícito) |

### Bloque 1 — Política y specs

**Rama:** `feature/a11y-policy-docs`

| Paso | Entrega (documento **completo**) |
|------|----------------------------------|
| 1.1 | `docs/A11Y.md`: principios, perfiles, resolución, precedencia vs SEC, cómo registrar conflicto |
| 1.2 | SSS entero: A11Y férrea + perfiles |
| 1.3 | SRS entero: `REQ-A11Y-*` verificables |
| 1.4 | SEC entero y/o ICD entero si se tocan mensajes/prefijos/help/man |
| 1.5 | `06-TEST` criterio A11Y |
| 1.6 | OVERVIEW, METHODOLOGY, README, HUMAN/AI/DEV onboarding: enlaces (un archivo por mensaje) |

Sin bump si no hay runtime. Se puede no etiquetar y acumular en 0.2.4.

### Bloque 2 — Runtime

**Rama:** `feature/a11y-runtime-messages`

| Paso | Qué |
|------|-----|
| 2.1 | Inventario de prints: arranque, seguridad, help, man, test, update, launchers |
| 2.2 | Prefijos estables (`[SEGURIDAD]`, error/aviso); texto accionable |
| 2.3 | No usar solo ANSI/color como señal |
| 2.4 | Fallo de arranque y rechazo de comando: comprensibles para lector de terminal |

Cambio observable de producto → entra en bump **0.2.4** junto al bloque 3.

### Bloque 3 — Tests

**Rama:** `feature/a11y-tests` (o la misma que el 2 si se acuerda un solo merge)

| Paso | Qué |
|------|-----|
| 3.1 | Tests: help no vacío (ya hay); prefijos; mensaje de rechazo/arranque con pista |
| 3.2 | Documentar límites (no GUI) en A11Y.md / TEST |
| 3.3 | CHANGELOG 0.2.4, SRelD (perfiles de esta baseline), bump 0.2.4, merge, tag `v0.2.4` |

### Cierre II

- Interacción: ¿docs enteros? ¿un paso? ¿tablas cerradas?  
- Deuda: perfiles no testeables, man incompleto, color residual.  
- Actualizar A11Y.md / AI_ONBOARDING si cambia el método.

---

## Grupo III — Protocolo de interacción

**Rama:** `feature/interaction-review-protocol`  
**Tag:** `v0.2.5-docs`  
**Bump Poetry:** no

### Bloque 4

| Paso | Entrega |
|------|---------|
| 4.1 | `docs/INTERACTION_REVIEW.md`: plantilla (interacción + deuda + hueco para secciones nuevas) |
| 4.2 | METHODOLOGY entero: cierre de grupo obligatorio |
| 4.3 | AI_ONBOARDING + AGENTS: incidentes, docs largos enteros, tablas cerradas |
| 4.4 | HUMAN_ONBOARDING: cómo recibe el humano (pegar entero, un paso) |
| 4.5 | Merge + tag `v0.2.5-docs` |

### Cierre III

Comprobar que las normas no se contradicen. Deuda residual → CHANGELOG “Sin publicar” o primera línea de la siguiente campaña.

---

## Orden git de la campaña

```text
main @ 0.2.2
  feature/script-hygiene-lf-poetry     → v0.2.3
  Cierre I
  feature/a11y-policy-docs
  feature/a11y-runtime-messages
  feature/a11y-tests                   → v0.2.4
  Cierre II
  feature/interaction-review-protocol  → v0.2.5-docs
  Cierre III
```

Bloques 2 y 3 de A11Y pueden unificarse en una rama si en ejecución conviene; el plan no lo exige.

---

## Criterio de “bloque hecho”

El humano dice el id (`0.2 hecho`, `1.1 hecho`, `Cierre I hecho`). No se entrega el siguiente archivo hasta entonces.

---

## Estado de esta ficha

Diseñada. Se actualizará al cerrar cada grupo (fechas reales de merge y tags).