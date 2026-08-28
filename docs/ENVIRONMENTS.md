# Entornos de ejecución de MetsuOS

**Versión del documento:** 1.2  
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
| native | Shell nativo del sistema (bash/zsh/etc. del OS) |
| git-bash | Git Bash / MSYS / MinGW sobre Windows |
| wsl | Windows Subsystem for Linux (clone en filesystem Linux) |

### Rol

| Valor | Significado |
|-------|-------------|
| desarrollo | Editar código, commits, push |
| prueba | Validar comportamiento; no asumir que se publica desde aquí |
| ambos | Desarrollo y prueba en el mismo perfil |

### Ejemplos válidos

```text
Contexto: macos / native / desarrollo
Contexto: windows / git-bash / prueba
Contexto: windows / wsl / desarrollo
Contexto: linux / native / ambos
```

### Cambio de contexto

```text
Cambio de contexto: windows / git-bash / prueba
```

La asistencia por IA debe adaptar comandos al contexto declarado y preguntar si falta.

### Qué no va en el repositorio

- Nombres de host o de equipos personales
- Rutas home absolutas de un usuario concreto
- Inventarios privados de hardware

---

## Perfiles soportados

| Sistema | Entorno | Poetry típico | Notas |
|---------|---------|---------------|-------|
| linux | native | poetry o python3 -m poetry | Referencia Unix |
| macos | native | poetry o python3 -m poetry | zsh/bash nativos |
| windows | git-bash | py -m poetry primero | poetry.exe solo si --version funciona |
| windows | wsl | poetry o python3 -m poetry | Clone en filesystem Linux |

---

## Resolución de Poetry (launcher e installer)

mos2.sh e install.sh usan la misma función de resolución. Un candidato solo cuenta si responde a `--version`.

### windows / git-bash (MINGW, MSYS, CYGWIN)

Orden:

1. py -m poetry
2. python -m poetry
3. python3 -m poetry
4. poetry.exe (solo si poetry.exe --version funciona)
5. poetry (solo si poetry --version funciona)

### linux / macos / windows+wsl (Unix)

Orden:

1. poetry (solo si poetry --version funciona)
2. python3 -m poetry
3. python -m poetry

### Principio de diseño

- No hardcodear rutas de instalación de Poetry ni de Python del usuario.
- Fallar con mensaje claro si no hay candidato viable.
- Tras resolver, usar siempre el mismo comando para run / install / config.

---

## Fin de línea (Git)

`.gitattributes` en la raíz marca `*.sh` y textos habituales con `eol=lf`.

Es una función de **Git**, no de GitHub u otro forge. Evita el error `/bin/bash^M` en WSL y Linux cuando el clone pasó por Windows.

---

## Rutas del repositorio

| Regla | Descripción |
|-------|-------------|
| Raíz del proyecto | Directorio que contiene pyproject.toml, moslib/, rootfs/ |
| Scripts | Se ubican por dirname del propio script (SCRIPT_DIR) |
| Python | Usa Path(__file__) / raíz de proyecto; no asume cwd global del usuario |
| Documentación de ejemplos | Usar rutas relativas (./mos2.sh, rootfs/bin/mos.py) |

En windows/wsl el clone objetivo está en el filesystem Linux, no como único modelo el montaje /mnt/c/...

---

## windows/wsl y rutas /mnt/

En WSL el clone debe vivir en el filesystem Linux (por ejemplo bajo $HOME), no bajo /mnt/c/... ni otros montajes del disco Windows.

Motivos:

- venvs distintos o rotos entre clones
- finales de línea CRLF en scripts .sh
- confusión entre alias que apuntan a otra ruta

mos2.sh e install.sh, si detectan WSL y que la raíz del proyecto está bajo /mnt/<letra>/, terminan con error y un mensaje guiado. No reubican ni copian el repositorio automáticamente.

Flujo recomendado:

```text
git clone <url-del-repo> "$HOME/mos2"
cd "$HOME/mos2"
./install.sh
./mos2.sh
```

---

## Lanzamiento e instalación

| Acción | Comando relativo al clone |
|--------|---------------------------|
| Instalar deps y aliases opcionales | ./install.sh |
| Arrancar MOSh | ./mos2.sh |
| Tests fuera del shell | pytest vía el Poetry resuelto del entorno, o el comando test dentro de MOSh |

Dentro de MOSh, los tests de arranque y el comando test usan sys.executable -m pytest (intérprete del proceso actual, normalmente el del venv activado por poetry run).

---

## Diferencias prácticas entre perfiles

| Tema | git-bash | wsl / linux / macos native |
|------|----------|----------------------------|
| Ejecutable Poetry | py -m poetry; poetry.exe solo si --version ok | poetry en PATH si --version ok |
| Fin de línea | .gitattributes fuerza LF en el repo | LF |
| Aliases | bash_profile/bashrc; PowerShell opcional vía install | bashrc/zshrc |
| Paths | Notación Git Bash si se inspecciona el FS de Windows | Paths Unix del clone Linux |
| Clone en WSL | No aplica | No usar /mnt/<letra>/... como raíz del proyecto |

---

## Requisitos derivados (trazabilidad)

| ID orientativo | Enunciado |
|----------------|-----------|
| REQ-PLAT-ENV-001 | El lanzador debe resolver Poetry de forma portable según el perfil |
| REQ-PLAT-ENV-002 | El instalador debe usar la misma política de resolución que el lanzador |
| REQ-PLAT-ENV-003 | La documentación no debe depender de rutas absolutas de un usuario concreto |
| REQ-PLAT-ENV-004 | El trabajo multi-entorno se comunica con contexto de sesión genérico |
| REQ-PLAT-ENV-005 | En WSL, lanzador e instalador deben rechazar clones bajo /mnt/<letra>/ |
| REQ-PLAT-ENV-006 | Un candidato Poetry solo se usa si --version se puede ejecutar |

La formalización numerada vive en el SRS; este documento es la política operativa.

---

## Verificación manual por perfil

| Perfil | Comprobación mínima |
|--------|---------------------|
| macos/native | ./install.sh y ./mos2.sh resuelven Poetry y arrancan |
| linux/native | Igual |
| windows/git-bash | No debe elegir poetry.exe si --version da Permission denied |
| windows/wsl | Clone en FS Linux; rechazo si la raíz está bajo /mnt/ |

---

## Autoridad

Este documento es normativo para perfiles de entorno, resolución de Poetry en scripts de shell y protocolo de contexto de sesión genérico.

Cualquier nuevo perfil soportado debe añadirse aquí y reflejarse en lanzador/instalador cuando aplique.