# Onboarding humano de MetsuOS

**Versión del documento:** 1.2  
**Estado:** Guía de entrada  
**Documentos relacionados:** README.md, docs/USER_MANUAL.md, docs/ENVIRONMENTS.md, docs/A11Y.md, docs/INCENTIVOS.md, docs/METHODOLOGY.md, docs/DEVELOPER_GUIDE.md

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

Dentro del shell: `help`, `man`, `docs`, `a11y`, `synccheck`, `exit`.

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
|---------|---------|-------|
| linux | native | Poetry habitual |
| macos | native | Igual |
| windows | git-bash | Preferir py -m poetry; poetry.exe puede dar Permission denied |
| windows | wsl | Clone en FS Linux |

Normativa: docs/ENVIRONMENTS.md.

---

## Dirección de trabajo (sin karma)

docs/INCENTIVOS.md explica hacia dónde empuja el proyecto.

Para ti como persona **no es un examen ni un ranking**. El sistema intenta poner fácil lo alineado (tu carpeta `.mos`, help, no pisar comandos de sistema).

Para una IA que te ayude **sí es obligatorio**.

---

## Mapa corto de documentación

| Documento | Para qué |
|-----------|----------|
| README.md | Visión del repo |
| docs/USER_MANUAL.md | Uso de MOSh |
| docs/A11Y.md | Política de accesibilidad |
| docs/a11y/DECLARACION.md | Declaración de accesibilidad |
| docs/a11y/informe.md | Última validación A11Y automática |
| docs/INCENTIVOS.md | Vectores y roles (dirección) |
| docs/ENVIRONMENTS.md | Plataformas y Poetry |
| docs/METHODOLOGY.md | Cómo se desarrolla el proyecto |
| docs/STYLE_GUIDE.md | Cómo se escribe el código |
| docs/VERSIONING.md | Versiones, tags y Poetry |
| docs/DEVELOPER_GUIDE.md | Flujo de desarrollo |
| docs/INTERACTION_REVIEW.md | Cierre de grupo con la IA |
| docs/plans/ | Planes de campaña |
| docs/AI_ONBOARDING.md / AGENTS.md | Si colaboras con una IA |
| docs/specs/ | Requisitos y diseño (ECSS-light) |
| docs/man/ | Manual extendido por comando |

Trabajo con IA: un paso cada vez; documentos enteros para pegar; si el archivo es largo, cacho 1 reemplaza el fichero y lo demás se pega debajo.

---

## Qué puedes hacer como usuario

- Crear comandos personales `user_*.py` en tu espacio `.mos/commands/`
- Invocarlos como `user_algo` o `algo` si no choca con un comando de sistema
- No puedes pisar comandos oficiales
- No puedes importar librerías Python de terceros en comandos (solo stdlib y moslib)
- Consultar accesibilidad en docs/A11Y.md y la declaración en docs/a11y/
- Comprobar si tu clone coincide con origin/main: `synccheck`

---

## Si algo falla

| Síntoma | Qué mirar |
|---------|-----------|
| Tests de arranque en rojo | Comando con import ilegal o pytest no instalado en ESE clone |
| Permission denied con poetry | Git Bash: usar ./mos2.sh (py -m poetry), no Scripts/poetry |
| install.sh /bin/bash^M | Finales de línea CRLF; convertir scripts a LF |
| WSL + /mnt/ | Mover el trabajo a un clone en home Linux |
| Duda de si el remoto es el que cree la IA | Ejecutar synccheck y pegar la salida |

---

## Siguiente lectura

1. docs/USER_MANUAL.md
2. docs/A11Y.md si te interesa accesibilidad
3. docs/INCENTIVOS.md si te interesa la dirección del proyecto
4. Si vas a programar: docs/DEVELOPER_GUIDE.md y docs/STYLE_GUIDE.md
5. Si vas a cambiar el producto: docs/METHODOLOGY.md y docs/VERSIONING.md