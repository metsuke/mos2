# Integridad canónica + sync post-pull (EOL y local)

**Fecha:** 2026-09-20
**NN del día:** 01
**Archivo:** 2026-09-20-01-integridad-eol-sync.md
**Estado:** Diseñada (pendiente implementación)
**Rama prevista:** feature/integridad-eol-sync
**Producto al inicio:** 0.2.7 / trabajo 0.2.8
**Producto al cierre:** el que marque VERSIONING al merge (sin bump salvo cierre conjunto de 0.2.8)
**Contexto de sesión:** windows / git-bash / prueba; macos / native / desarrollo
**Documentos relacionados:** docs/plans/2026-09-18-01-integridad-write.md, docs/ENVIRONMENTS.md, docs/METHODOLOGY.md, moslib/core/integridad.py, moslib/core/integridad_sello.py, moslib/core/shell_boot.py, moslib/commands/update.py, moslib/commands/integridad.py, mos2.sh, .gitattributes, tests/test_integridad.py

## Objetivo
Tras `git pull` o el comando `update`, en cualquier perfil soportado (linux/native, macos/native, windows/git-bash, windows/wsl):

1. El hash de un fichero tracked no depende de CRLF o LF en el working tree.
2. La copia local del manifiesto se realinea sola con la del repositorio si falta, si el sello local no vale, o si el mapa del repo cambió.
3. El arranque distingue desfase de fin de línea de cambio real de contenido.
4. Solo se bloquea el arranque si el contenido canónico no cuadra. El EOL sucio y el local viejo se corrigen.

Esta campaña no sustituye a `2026-09-18-01-integridad-write.md`. Cierra el agujero pull + EOL + local que aquel plan no cubría.

## Fuera de alcance
- Firma, TPM, antimalware.
- Cambiar el modelo «todo tracked entra en el manifiesto».
- Autocommit de `integridad sembrar` desde Windows.
- Reescribir el historial Git.
- Hooks de Git que el usuario tenga que instalar.
- Permitir arrancar si un fichero tracked cambió de verdad (digest canónico distinto).
- Escribir `core.autocrlf` en la configuración global de la máquina.

## Diagnóstico
Causa A. `asegurar_local()` y el boot solo copian repo → local si falta el fichero local o su sello. Tras `git pull` el local viejo sigue mandando.

Causa B. `sha256_fichero` usa `read_bytes()`. Git for Windows con `core.autocrlf` convierte a CRLF tipos que `.gitattributes` no fuerza a LF (`*.json`, `*.html`, `LICENSE`). Mac y Linux quedan en LF. Misma revisión, hashes distintos.

Causa C. `fallos()` comprueba el sello del repo y el del local. Un `integridad.json` en CRLF rompe el `.sha256` generado en Unix. MOSh no llega a `integridad recargar`.

## Decisión de diseño

### Hash canónico
Una función compartida por manifiesto y sello:

- `normalizar_eol(data: bytes) -> bytes`: sustituye `\r\n` y `\r` sueltos por `\n`. No altera el resto de bytes.
- `sha256_canonico(path) -> str`: SHA-256 de `normalizar_eol(path.read_bytes())`.
- El JSON del manifiesto y el `.sha256` guardan solo digest canónico.
- Toda comparación usa digest canónico contra digest canónico.

El working tree puede seguir con CRLF; el sello no depende de eso.

### Working tree de referencia
`.gitattributes` cubre el texto que hoy se hashea y aún no forzaba LF:

- `*.json text eol=lf`
- `*.html text eol=lf`
- `*.css text eol=lf`
- `LICENSE text eol=lf`

Se mantienen las reglas ya existentes (`.md`, `.py`, `.sh`, `.gitignore` y el resto).

Tras cambiar attributes: `git add --renormalize .` en un checkout LF (macos, linux o wsl con clone fuera de `/mnt/`). Un commit `chore: eol lf en json html LICENSE`.

No se escribe `core.autocrlf` global. En el clone de git-bash se documenta como recomendación local:

    git config --local core.autocrlf false
    git config --local core.eol lf

### Autoridad repo frente a local
El manifiesto del repositorio es la fuente después de un pull. El local es caché de usuario.

| Situación | Acción automática | ¿Bloquea el arranque? |
|-----------|-------------------|------------------------|
| No hay local o no hay sello local | `copiar_repo_a_local()` | No |
| Mapa local distinto del mapa repo y sello repo canónico válido | `local ← repo` y log de alineación | No |
| Sello repo o local falla en bytes crudos pero el digest canónico del JSON coincide con el `.sha256` | reescribir local desde repo; no tocar el resto de tracked | No |
| Tracked: bytes crudos distintos del manifiesto y bytes canónicos iguales | log de EOL; no es fallo de contenido | No |
| Tracked: digest canónico distinto del manifiesto ya alineado | fallo de contenido | Sí |
| Falta un fichero tracked listado | fallo de falta | Sí |
| No hay manifiesto en repo ni en local | pedir `integridad sembrar`; no inventar mapa | No |

Nunca se usa `integridad sembrar` en Windows para «arreglar» un pull.

`integridad aceptar` sigue escribiendo repo y local. Un pull posterior pisa el local con el repo. Quien acepte un cambio en una máquina debe commitear el manifiesto.

### Escape sin entrar al shell
Antes de la comprobación estricta, `shell_boot` honra:

- variable de entorno `MOS_INTEGRIDAD=recargar`
- argumento que `mos2.sh` reenvía: `./mos2.sh --integridad-recargar`

Eso ejecuta `copiar_repo_a_local()` y sigue el flujo normal.

### Comando update
Tras un pull con éxito, `update` llama siempre a `copiar_repo_a_local()`. Si `docs/docgen/integridad.json` no cambió, la copia es idempotente.

Un `git pull` hecho fuera de MOSh no lleva hook. Queda cubierto por la tabla de autoridad en el siguiente arranque.

## Bloques

### Bloque 1 — Contrato de hash y attributes
Pasos:

1. Extraer `normalizar_eol` y `sha256_canonico`. Manifiesto y sello usan solo eso.
2. Tests: el mismo texto en LF, CRLF y CR produce el mismo hex. Un fichero que solo cambia `\n` por `\r\n` no genera fallo canónico.
3. Ampliar `.gitattributes`.
4. Renormalizar y commit de attributes antes de resembrar.

Criterio de salida: `pytest tests/test_integridad.py` en verde.

### Bloque 2 — Sync local y arranque
Pasos:

1. Sustituir `asegurar_local()` por `alinear_local_con_repo()` según la tabla de autoridad.
2. `fallos()` clasifica: `eol`, `sello-eol`, `desfase-local`, `contenido`, `falta`.
3. `_integridad()` en `shell_boot`: alinea; imprime avisos EOL; solo devuelve falso si queda `contenido` o `falta`.
4. Honrar `MOS_INTEGRIDAD=recargar` y el flag de `mos2.sh`.
5. Tests: local viejo y repo nuevo copian y pasan; sello crudo roto por CRLF en el JSON no bloquea; un byte no-EOL distinto bloquea.

Criterio de salida: fixture CRLF equivalente al log de Git-Bash arranca; mutación real bloquea.

### Bloque 3 — update y semilla
Pasos:

1. `update` llama a `copiar_repo_a_local()` tras pull correcto.
2. En macos o linux, una vez, `integridad sembrar` con el hasher canónico.
3. Commit de `docs/docgen/integridad.json` y `docs/docgen/integridad.json.sha256`.
4. No sembrar en git-bash para ese commit.

Criterio de salida: arranque en mac correcto; en Windows, pull sin sembrar y arranque correcto.

### Bloque 4 — Documentación
Pasos:

1. `docs/ENVIRONMENTS.md`: sección de integridad y fin de línea, con la recomendación `core.autocrlf false` local al clone.
2. Man de `integridad` y de `update`: alineación automática y flag de emergencia.
3. En el plan `2026-09-18-01-integridad-write.md`, una nota de enlace a esta campaña. No reescribir el objetivo de aquel plan.
4. `docgen plan add 2026-09-20-01-integridad-eol-sync.md` y `docgen generate plans-readme`.
5. CHANGELOG de 0.2.8: integridad canónica y sync local.

Criterio de salida: un lector en git-bash sabe qué corrige el boot solo y cuándo el sello sigue siendo un fallo real.

## Orden
Bloque 1, luego 2, luego 3, luego 4. No resembrar (paso 3.2) antes de que el hasher canónico esté en el código que ejecuta el sembrar.

## Riesgos
| Riesgo | Mitigación |
|--------|------------|
| Sembrar en un tree Windows sucio | Sembrar solo en checkout LF. El hasher canónico evita el CRLF; no evita otros cambios locales |
| Un binario marcado como texto | El manifiesto solo lista tracked que ya son texto. No marcar binarios en attributes |
| La alineación automática pisa un `aceptar` local no commiteado | Contrato: el repo gana tras pull. Hay que commitear el manifiesto |
| Otro módulo sigue hasheando bytes crudos | Unificar llamadas a `sha256_fichero` de integridad y sello |

## Verificación manual por perfil
| Perfil | Comprobación |
|--------|----------------|
| macos/native | Sembrar, commit, `./mos2.sh` muestra `[integridad] OK` |
| windows/git-bash | `git pull` sin borrar el `.mos`; `./mos2.sh` alinea local y arranca |
| windows/git-bash con edición real | Cambiar un `.py` tracked; el arranque bloquea |
| windows/wsl | Clone en filesystem Linux, no bajo `/mnt/<letra>/`; mismo criterio que linux |
| Emergencia | `MOS_INTEGRIDAD=recargar ./mos2.sh` con local basura deja local ← repo |

## Tags
Sin bump de Poetry en esta campaña salvo que el humano cierre 0.2.8 junto con otros cambios. Tag solo si `docs/VERSIONING.md` lo exige al merge.

## Cierre
Un grupo. Para merge: tests verdes, arranque en mac, al menos un arranque git-bash o fixture CRLF, manifiesto y sello coherentes en `main`.