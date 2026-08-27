# Onboarding humano de MetsuOS

**Versión del documento:** 1.0  
**Estado:** Guía de entrada  
**Documentos relacionados:** README.md, docs/USER_MANUAL.md, docs/ENVIRONMENTS.md, docs/METHODOLOGY.md, docs/DEVELOPER_GUIDE.md

---

## Para quién es este documento

Personas que clonan el repo por primera vez y quieren:

- instalar y arrancar MOSh
- entender el mapa de documentación
- no perderse entre Mac, Git Bash y WSL

No sustituye al manual de usuario ni a las specs. Es el “por dónde empiezo”.

---

## Arranque rápido

Desde la raíz del clone:

```text
./install.sh
./mos2.sh
```

Dentro del shell: `help`, `man`, `exit`.

Detalle de uso cotidiano: docs/USER_MANUAL.md.

---

## Elige un solo clone

No mezcles dos copias del mismo proyecto (por ejemplo una en disco Windows montado y otra en home Linux). Cada clone tiene su propio `.venv`.

En WSL usa un clone en filesystem Linux (por ejemplo bajo $HOME), no bajo /mnt/c/...  
Si lanzas install.sh o mos2.sh desde /mnt/... en WSL, el sistema debe rechazarlo y explicarte el motivo.

---

## Perfiles de entorno

Declara (en chat con IA o en notas de trabajo):

```text
Contexto: <sistema> / <entorno> / <rol>
```

| Sistema | Entorno | Notas |
|---------|----------|-------|
| linux | native | Poetry habitual |
| macos | native | Igual |
| windows | git-bash | Preferir py -m poetry; poetry.exe puede dar Permission denied |
| windows | wsl | Clone en FS Linux |

Normativa: docs/ENVIRONMENTS.md.

---

## Mapa corto de documentación

| Documento | Para qué |
|-----------|----------|
| README.md | Visión del repo |
| docs/USER_MANUAL.md | Uso de MOSh |
| docs/ENVIRONMENTS.md | Plataformas y Poetry |
| docs/METHODOLOGY.md | Cómo se desarrolla el proyecto |
| docs/STYLE_GUIDE.md | Cómo se escribe el código |
| docs/VERSIONING.md | Versiones, tags y Poetry |
| docs/DEVELOPER_GUIDE.md | Flujo de desarrollo |
| docs/AI_ONBOARDING.md / AGENTS.md | Si colaboras con una IA |
| docs/specs/ | Requisitos y diseño (ECSS-light) |
| docs/man/ | Manual extendido por comando |

---

## Qué puedes hacer como usuario

- Crear comandos personales `user_*.py` en tu espacio `.mos/commands/`
- Invocarlos como `user_algo` o `algo` si no choca con un comando de sistema
- No puedes pisar comandos oficiales
- No puedes importar librerías Python de terceros en comandos (solo stdlib y moslib)

---

## Si algo falla

| Síntoma | Qué mirar |
|---------|-----------|
| Tests de arranque en rojo | Comando con import ilegal o pytest no instalado en ESE clone |
| Permission denied con poetry | Git Bash: usar ./mos2.sh (py -m poetry), no Scripts/poetry |
| install.sh /bin/bash^M | Finales de línea CRLF; convertir scripts a LF |
| WSL + /mnt/ | Mover el trabajo a un clone en home Linux |

---

## Siguiente lectura

1. docs/USER_MANUAL.md
2. Si vas a programar: docs/DEVELOPER_GUIDE.md y docs/STYLE_GUIDE.md
3. Si vas a cambiar el producto: docs/METHODOLOGY.md y docs/VERSIONING.md