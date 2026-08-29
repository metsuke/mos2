# Onboarding para agentes IA (MetsuOS)

**Versión del documento:** 1.1  
**Estado:** Normativo de proceso  
**Documentos relacionados:** AGENTS.md, docs/METHODOLOGY.md, docs/ENVIRONMENTS.md, docs/VERSIONING.md, docs/A11Y.md, docs/STYLE_GUIDE.md, docs/specs/00-OVERVIEW.md, docs/plans/README.md

---

## Propósito

Permitir que cualquier modelo o agente, al estudiar el repositorio desde cero, asuma el contexto real de MetsuOS sin reinventar normas ni romper lo existente.

Este documento es la guía de arranque para IA. El punto de entrada corto en la raíz es `AGENTS.md`.

---

## Orden de lectura obligatorio

1. AGENTS.md (raíz)
2. Este archivo (docs/AI_ONBOARDING.md)
3. docs/METHODOLOGY.md
4. docs/ENVIRONMENTS.md
5. docs/VERSIONING.md
6. docs/A11Y.md y docs/a11y/DECLARACION.md
7. docs/STYLE_GUIDE.md
8. docs/specs/00-OVERVIEW.md y, según la tarea, SSS / SEC / ICD / SRS / SDD / TEST / SRelD
9. docs/plans/ si hay campaña en curso
10. docs/USER_MANUAL.md y docs/man/ si la tarea afecta al uso
11. Código solo después de saber qué norma aplica

No inventar features que no existan en el código o en las specs.

---

## Qué es MetsuOS (recordatorio férreo)

- SO simulado modular en Python; shell MOSh.
- Núcleo en moslib/; rootfs/ simulado.
- Todo comando pasa por contrato execute(args) y help() -> str.
- Imports de comandos: solo stdlib + moslib (validación AST).
- Espacio de usuario por usuario anfitrión; comandos user_*.py.
- Tests de arranque bloqueantes.
- Accesibilidad de interfaz mandatoria.
- Poetry + mos2.sh / install.sh multi-entorno.

---

## Contexto de sesión (obligatorio)

Formato:

```text
Contexto: <sistema> / <entorno> / <rol>
```

Ejemplos: macos/native/desarrollo, windows/git-bash/prueba, windows/wsl/ambos.

Si el humano no lo declara y la tarea implica paths, Poetry o git push, **preguntar** antes de asumir.

No documentar ni pedir nombres de host ni rutas home personales en el repo público. Rutas siempre relativas al clone.

Detalle: docs/ENVIRONMENTS.md.

---

## Cómo entregar trabajo al humano

- Un archivo o sección completa en **un único bloque de texto** listo para copiar y pegar.
- Explicar en pocas líneas **qué ha cambiado** para validar leyendo.
- No pedir al humano que reescriba tablas o párrafos largos a mano.
- Si una fase toca varias piezas: **un paso cada vez**.
- Encabezados de documentación **sin numeración**.
- Si el archivo del repo aún tiene números, entregar el documento completo ya sin números.
- Si la versión nueva es más corta que la del repo (docs **o** código), comprobar que no se pierde contenido e **informarlo**. Prohibido resumir sin consultar.
- Documentos largos: **cacho 1 sustituye todo el fichero**; los siguientes se pegan **debajo**.
- Estructuras de directorios: tablas markdown, una columna por nivel.
- Tablas de comandos del sistema: columna Tipo (A–Z) y, dentro de cada tipo, comandos A–Z.
- Crear carpetas o ficheros: secuencia bash (`mkdir -p`, `touch`, editor).
- Cada paso de campaña: breadcrumb (campaña, grupo, bloque x/y, paso, progreso aproximado).
- Git, no funciones exclusivas de un forge.
- No usar «corrida»; usar «ejecución» o «pasada de tests».
- CHANGELOG: no dejar «Sin publicar» a criterio del humano.

---

## Antes de proponer cambios de código

1. Leer el estado real del repo (ficheros, no solo memoria de chat).
2. Comprobar impacto en SEC / SSS / ICD / SRS / A11Y.
3. Respetar STYLE_GUIDE y seguridad de imports.
4. Plan por fases con commits atómicos; campaña → `docs/plans/`.
5. No desactivar tests de arranque ni la seguridad para “hacer pasar” un cambio.
6. Si es cambio de producto: aplicar docs/VERSIONING.md (¿bump Poetry? ¿tag?).
7. Tags solo-docs: `vX.Y.Z-docs` o `vX.Y.Z-docs.N` con la Poetry vigente; nunca un parche mayor que el producto.

---

## Versionado (resumen operativo)

| Tipo de cambio | Poetry pyproject.toml | Tag típico |
|----------------|----------------------|------------|
| Runtime / scripts / comandos / seguridad | Bump X.Y.Z | vX.Y.Z |
| Solo documentación / onboarding | No bump | vX.Y.Z-docs o vX.Y.Z-docs.N |

Detalle: docs/VERSIONING.md (ajuste fino de nomenclatura: deuda de cierre).

---

## Plataforma y Poetry

- mos2.sh e install.sh resuelven Poetry según perfil.
- Un candidato solo cuenta si `--version` se puede ejecutar.
- windows/git-bash: priorizar `py -m poetry`.
- windows/wsl: clone en filesystem Linux; rechazo si la raíz está bajo `/mnt/<letra>/` (SCRIPT_DIR antes del check).

---

## Accesibilidad

- Política: docs/A11Y.md
- Declaración: docs/a11y/DECLARACION.md
- Informe: docs/a11y/informe.md
- Si A11Y y SEC chocan: procedimiento en A11Y.md y 04-SEC. No excepción silenciosa.
- Comandos `a11y` y `docs`: previstos en producto 0.2.5.

---

## Checklist rápido antes de cerrar una fase

1. ¿Contexto de sesión claro?
2. ¿Normas SEC/SSS/ICD/A11Y respetadas?
3. ¿Tests y arranque contemplados?
4. ¿Docs actualizados si cambió comportamiento o proceso?
5. ¿VERSIONING aplicado (bump o explícitamente no)?
6. ¿Entrega en un bloque / un paso / cachos sin pérdida?
7. ¿Encabezados sin números?
8. ¿Breadcrumb de campaña?

---

## Autoridad

Este documento es normativo para el comportamiento de asistencia por IA en MetsuOS.

Si entra en conflicto con SEC, SSS o A11Y, prevalecen esas normas; luego hay que actualizar este onboarding.