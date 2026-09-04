# Plan 07-fix — apps usables de verdad

**Fecha:** 2026-09-04  
**Orden del día:** 01  
**Producto de partida:** 0.2.6 + rama 08 (loader)  
**Estado:** Obliga a pausar 8.2+ hasta cerrar esto

---

## Por qué

La 07 entregó install/list/remove y SEC del núcleo. No entregó lo que una app **necesita para existir**:

- mini-moslib de la app
- SEC que lo permita **solo** a los comandos de esa app
- loader que enlace ese mini-moslib al importar
- instalar desde ruta relativa al **clone**, no al cwd de MOSh
- man y help de comandos de app

Sin eso, la suite de desarrollo (08) se apoya otra vez en arena. La 08 se **pausa**. Este plan no implementa `aceptar` ni Grok.

---

## Qué tiene que quedar funcionando

Una app de prueba (puede ser `apps/dev` como cuna) debe:

1. Tener `minimoslib/` con helpers (p. ej. leer JSON de estado).
2. Tener comandos que hagan `from minimoslib.xxx import …` y **pasen** SEC e install.
3. No poder importar otra cosa (`apps.dev.commands`, `requests`, otra app).
4. Instalarse con `apps install apps/dev` **dentro de MOSh** (ruta respecto a la raíz del proyecto).
5. Invocarse en el shell (`app_dev_campania`).
6. `help` listar esos comandos como de app.
7. `man app_dev_campania` leer `apps/dev/man/…` o la copia instalada en `.mos/apps/dev/man/`.
8. Dos apps distintas no se pisan el `minimoslib` al cargar.

Si uno de esos puntos falla, 07-fix no está cerrada.

---

## Diseño (no negociable aquí)

| Pieza | Decisión |
|-------|----------|
| Carpeta | `<app>/minimoslib/` (paquete: `__init__.py` + módulos) |
| Import en comandos | solo `minimoslib` y `minimoslib.*` |
| Import entre comandos de la app | no; el compartido va a minimoslib |
| Núcleo | no importa minimoslib de ninguna app |
| SEC | al validar un comando de app, se pasa el directorio de esa app; se permite `minimoslib` si el módulo existe ahí |
| Loader | al cargar un `.py` de `…/apps/<id>/commands/`, inyecta ese `minimoslib` en el namespace del módulo (no un `sys.path` global eterno que mezcle apps) |
| Install | `Path(src)` si es absoluto; si es relativo, `get_project_root() / src` |
| Man | `man` busca: docs/man del núcleo; si no, apps instaladas `…/man/<cmd>.md`; si no, cuna `apps/<id>/man/` |
| Help | aparte de sistema y user_, lista comandos de apps instaladas |

---

## Bloques de este plan (en orden)

| Id | Qué | Criterio de hecho |
|----|-----|-------------------|
| F.0 | Este archivo + nota en plan 08 “pausada hasta 07-fix” | Ficheros en git |
| F.1 | SEC: `validate_command_file(..., app_dir=)` permite `minimoslib` solo si hay fichero en `app_dir/minimoslib/` | Tests: legal / `import requests` / `from apps.dev` siguen mal |
| F.2 | `apps._validate_source` pasa `app_dir` a SEC | install de fixture con minimoslib OK |
| F.3 | `cmd_loader` carga el comando con minimoslib de **esa** app | test dos apps, dos helpers distintos |
| F.4 | `apps install` resuelve ruta contra `get_project_root()` | `apps install apps/dev` en MOSh funciona |
| F.5 | `help` y `man` ven comandos y man de app | man no está en docs/man del núcleo |
| F.6 | Tests + man de sistema `apps` si cambia comportamiento + DEUDA | pytest verde |

No se abre F.2 si F.1 no tiene tests. No se vuelve a 8.2 hasta F.6.

---

## Fuera de 07-fix

- `app_dev_aceptar`, commit, iarouter on
- Repo propio de la suite
- P2P, RGPD, DepManager

La cuna `apps/dev` se puede usar como fixture; no se avanza la suite.

---

## Relación con planes previos

- `2026-09-01-02-campana-07-soporte-…`: frente A incompleto; este plan lo cierra.
- `2026-09-03-01-campana-08-…`: bloques 8.2+ **congelados** hasta F.6.

---

## Criterio de cierre 07-fix

Checklist de “Qué tiene que quedar funcionando” al 8/8. Tag de producto solo si SEC/loader/install cambian runtime (probable **0.2.7**).