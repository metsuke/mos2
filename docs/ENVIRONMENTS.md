# Entornos de ejecución de MetsuOS

**Versión del documento:** 1.4  
**Estado:** Normativo  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/USER_MANUAL.md, docs/specs/01-SSS-System-Specification.md, .gitattributes

---

## Propósito
Este documento describe los perfiles de entorno soportados por MetsuOS y cómo se comportan el lanzador y el instalador respecto a Poetry y al sistema anfitrión.

Normas:

- No se documentan máquinas personales ni rutas absolutas de usuarios concretos.
- El código y los scripts resuelven rutas respecto a la raíz del clone actual.
- En conversaciones con IA o entre desarrolladores se declara un contexto de sesión genérico.
- Las reglas de fin de línea viven en Git (`.gitattributes`), no en funcionalidades de un forge concreto.

---

## Contexto de sesión (protocolo)
Formato obligatorio cuando se trabaja por fases (humano o IA):

```text
Contexto: <sistema> / <entorno> / <rol>
```

### Sistema

| Valor | Significado |
|-------|-------------|
| linux | Sistema tipo Linux (nativo o contenedor) |
| macos | macOS |
| windows | Windows |

### Entorno

| Valor | Significado |
|-------|-------------|
| native | Shell nativo del sistema |
| git-bash | Git Bash / MSYS / MinGW sobre Windows |
| wsl | WSL (clone en filesystem Linux) |

### Rol

| Valor | Significado |
|-------|-------------|
| desarrollo | Editar código, commits, push |
| prueba | Validar; no asumir publicación |
| ambos | Desarrollo y prueba en el mismo perfil |

```text
Contexto: macos / native / desarrollo
```

La asistencia por IA debe adaptar comandos al contexto y preguntar si falta.

No van al repo: hostnames, rutas home absolutas, inventarios privados.

---

## Perfiles soportados
| Sistema | Entorno | Poetry típico | Notas |
|---------|---------|---------------|-------|
| linux | native | poetry o python3 -m poetry | Referencia Unix |
| macos | native | poetry o python3 -m poetry | zsh/bash nativos |
| windows | git-bash | py -m poetry primero | poetry.exe solo si --version funciona |
| windows | wsl | poetry o python3 -m poetry | Clone en filesystem Linux |

---

## Resolución de Poetry
mos2.sh e install.sh usan la misma función. Un candidato solo cuenta si responde a `--version`.

Git Bash: py -m poetry, python -m poetry, python3 -m poetry, poetry.exe, poetry.
Unix/WSL: poetry, python3 -m poetry, python -m poetry.

No hardcodear rutas. Fallar con mensaje claro. Tras resolver, el mismo comando para run/install/config.

---

## Fin de línea (Git)
`.gitattributes` marca `*.sh` y textos con `eol=lf`. Es Git, no el forge. Evita `/bin/bash^M`.

El hash de integridad es canónico (EOL normalizado). Distinto contenido sigue fallando.

---

## Rutas del repositorio
| Regla | Descripción |
|-------|-------------|
| Raíz | Directorio con pyproject.toml, moslib/, rootfs/ |
| Scripts | dirname del propio script |
| Python | Path(__file__); no asume cwd |
| Ejemplos | Rutas relativas (./mos2.sh, ./write.sh) |

Comandos `git`, `code`, `touch` y `write` resuelven desde la raíz del clone.

---

## windows/wsl y rutas /mnt/
En WSL el clone vive en filesystem Linux (p. ej. $HOME), no bajo /mnt/c/...

mos2.sh e install.sh, si detectan WSL y raíz bajo /mnt/<letra>/, terminan con error guiado. No reubican solos.

---

## Locale de arranque
El sistema no arranca si el locale de la máquina no es español de España (es_ES). El bloqueo explica el criterio (regímenes democráticos; reservas ante sharia o equivalentes) y enlaza la DUDH. Se puede pedir de forma razonada la apertura a otros locales.

Parámetro de prueba en mos2 para simular el bloqueo sin cambiar el locale real.

---

## Lanzamiento e instalación
| Acción | Comando |
|--------|---------|
| Instalar | ./install.sh |
| Arrancar | ./mos2.sh |
| Lote fuera de MOS | ./write.sh |
| Tests | comando test en MOSh |

Dentro de MOSh: sys.executable -m pytest.

---

## Diferencias prácticas
| Tema | git-bash | wsl / linux / macos |
|------|----------|---------------------|
| Poetry | py -m poetry | poetry en PATH si --version ok |
| EOL | .gitattributes LF | LF |
| Clone WSL | No aplica | No /mnt/<letra>/ |

---

## Requisitos derivados
| ID | Enunciado |
|----|-----------|
| REQ-PLAT-ENV-001 | Poetry portable según perfil |
| REQ-PLAT-ENV-002 | Instalador = misma política que lanzador |
| REQ-PLAT-ENV-003 | Docs sin rutas absolutas de un usuario |
| REQ-PLAT-ENV-004 | Contexto de sesión genérico |
| REQ-PLAT-ENV-005 | WSL rechaza /mnt/<letra>/ |
| REQ-PLAT-ENV-006 | Candidato Poetry solo si --version |
| REQ-PLAT-ENV-007 | Arranque exige locale es_ES salvo simulación |

Formalización en SRS.

---

## Verificación manual por perfil
| Perfil | Comprobación |
|--------|--------------|
| macos/native | install + mos2 arrancan |
| linux/native | Igual |
| windows/git-bash | No poetry.exe si Permission denied |
| windows/wsl | Clone Linux; rechazo /mnt/ |

---

## Autoridad
Normativo para perfiles, Poetry en scripts y contexto de sesión. Nuevo perfil: aquí + lanzador/instalador.