# Entornos de ejecución de MetsuOS

**Versión del documento:** 1.0  
**Estado:** Normativo  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/USER_MANUAL.md, docs/specs/01-SSS-System-Specification.md

---

## 1. Propósito

Este documento describe los perfiles de entorno soportados por MetsuOS y cómo se comportan el lanzador y el instalador respecto a Poetry y al sistema anfitrión.

Normas:

- No se documentan máquinas personales ni rutas absolutas de usuarios concretos.
- El código y los scripts resuelven rutas respecto a la raíz del clone actual.
- En conversaciones con IA o entre desarrolladores se declara un contexto de sesión genérico.

---

## 2. Contexto de sesión (protocolo)

Formato obligatorio cuando se trabaja por fases (humano o IA):

Contexto: <sistema> / <entorno> / <rol>

### 2.1 Sistema

| Valor | Significado |
|-------|-------------|
| linux | Sistema tipo Linux (nativo o contenedor) |
| macos | macOS |
| windows | Windows |

### 2.2 Entorno

| Valor | Significado |
|-------|-------------|
| native | Shell nativo del sistema (bash/zsh/etc. del OS) |
| git-bash | Git Bash / MSYS / MinGW sobre Windows |
| wsl | Windows Subsystem for Linux (clone en filesystem Linux) |

### 2.3 Rol

| Valor | Significado |
|-------|-------------|
| desarrollo | Editar código, commits, push |
| prueba | Validar comportamiento; no asumir que se publica desde aquí |
| ambos | Desarrollo y prueba en el mismo perfil |

### 2.4 Ejemplos válidos

Contexto: macos / native / desarrollo
Contexto: windows / git-bash / prueba
Contexto: windows / wsl / desarrollo
Contexto: linux / native / ambos

### 2.5 Cambio de contexto

Cambio de contexto: windows / git-bash / prueba

La asistencia por IA debe adaptar comandos al contexto declarado y preguntar si falta.

### 2.6 Qué no va en el repositorio

- Nombres de host o de equipos personales
- Rutas home absolutas de un usuario concreto
- Inventarios privados de hardware

---

## 3. Perfiles soportados

| Sistema | Entorno | Poetry típico | Notas |
|---------|---------|---------------|-------|
| linux | native | poetry o python3 -m poetry | Referencia Unix |
| macos | native | poetry o python3 -m poetry | zsh/bash nativos |
| windows | git-bash | poetry.exe, py -m poetry, python -m poetry | Evitar el script poetry sin extensión (Permission denied) |
| windows | wsl | poetry o python3 -m poetry | Clone en filesystem Linux; comportamiento tipo Linux |

---

## 4. Resolución de Poetry (launcher e installer)

Los scripts mos2.sh e install.sh detectan el entorno y resuelven Poetry así:

### 4.1 windows / git-bash (MINGW, MSYS, CYGWIN)

Orden:

1. poetry.exe
2. py -m poetry
3. python -m poetry
4. python3 -m poetry
5. poetry (último recurso; puede fallar)

### 4.2 linux / macos / windows+wsl (comportamiento Unix)

Orden:

1. poetry
2. python3 -m poetry
3. python -m poetry

### 4.3 Principio de diseño

- No hardcodear rutas de instalación de Poetry ni de Python del usuario.
- Fallar con mensaje claro si no hay candidato viable.
- Tras resolver, usar siempre el mismo comando para run / install / config.

---

## 5. Rutas del repositorio

| Regla | Descripción |
|-------|-------------|
| Raíz del proyecto | Directorio que contiene pyproject.toml, moslib/, rootfs/ |
| Scripts | Se ubican por dirname del propio script (SCRIPT_DIR) |
| Python | Usa Path(__file__) / raíz de proyecto; no asume cwd global del usuario |
| Documentación de ejemplos | Usar rutas relativas (./mos2.sh, rootfs/bin/mos.py) |

En windows/wsl el clone objetivo está en el filesystem Linux, no como único modelo el montaje /mnt/c/...

---

## 6. Lanzamiento e instalación

| Acción | Comando relativo al clone |
|--------|---------------------------|
| Instalar deps y aliases opcionales | ./install.sh |
| Arrancar MOSh | ./mos2.sh |
| Tests fuera del shell | pytest vía el Poetry resuelto del entorno, o el comando test dentro de MOSh |

Dentro de MOSh, los tests de arranque y el comando test usan sys.executable -m pytest (intérprete del proceso actual, normalmente el del venv activado por poetry run).

---

## 7. Diferencias prácticas entre perfiles

| Tema | git-bash | wsl / linux / macos native |
|------|----------|----------------------------|
| Ejecutable Poetry | Preferir .exe o python -m poetry | poetry en PATH suele bastar |
| Fin de línea en scripts | Cuidado con CRLF en .sh | LF recomendado |
| Aliases | bash_profile/bashrc; PowerShell opcional vía install | bashrc/zshrc |
| Paths | Notación Git Bash si se inspecciona el FS de Windows | Paths Unix del clone Linux |

---

## 8. Requisitos derivados (trazabilidad)

| ID orientativo | Enunciado |
|----------------|-----------|
| REQ-PLAT-ENV-001 | El lanzador debe resolver Poetry de forma portable según el perfil |
| REQ-PLAT-ENV-002 | El instalador debe usar la misma política de resolución que el lanzador |
| REQ-PLAT-ENV-003 | La documentación no debe depender de rutas absolutas de un usuario concreto |
| REQ-PLAT-ENV-004 | El trabajo multi-entorno se comunica con contexto de sesión genérico |

La formalización numerada vive en el SRS; este documento es la política operativa.

---

## 9. Verificación manual por perfil

| Perfil | Comprobación mínima |
|--------|---------------------|
| macos/native | ./install.sh y ./mos2.sh resuelven Poetry y arrancan |
| linux/native | Igual |
| windows/git-bash | No debe quedarse solo en Scripts/poetry sin extensión si provoca Permission denied |
| windows/wsl | Mismo comportamiento que Linux en el clone Linux |

---

## 10. Autoridad

Este documento es normativo para perfiles de entorno, resolución de Poetry en scripts de shell y protocolo de contexto de sesión genérico.

Cualquier nuevo perfil soportado debe añadirse aquí y reflejarse en lanzador/instalador cuando aplique.