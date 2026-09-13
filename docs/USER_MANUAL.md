# Manual de usuario de MetsuOS (MOS2)

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.7 (árbol hacia v0.2.8)  
**Estado:** Manual formal de usuario  
**Documentos relacionados:** docs/man/, docs/ENVIRONMENTS.md, docs/METHODOLOGY.md, docs/specs/01-SSS-System-Specification.md, docs/specs/08-APPS.md, docs/specs/09-TASKS.md, docs/specs/10-IA-ROUTER.md

---

## Nota de revisión 1.2

La v1.1 se conserva. Esta versión **añade** comandos y secciones de producto 0.2.5–0.2.8. No sustituye instalación, entornos, arranque, espacio personal, comandos de usuario, seguridad, tests ni problemas frecuentes de 1.1.

---

## Introducción

MetsuOS (también llamado MOS2) es un sistema operativo simulado y modular escrito en Python.

Su interfaz principal es el shell **MOSh**, donde puedes ejecutar:

- comandos oficiales del sistema
- comandos de apps instaladas
- comandos personales de usuario
- utilidades de ayuda, tests, actualización y documentación

Este manual explica cómo instalar, arrancar y usar MetsuOS en la práctica.

Para ayuda extendida de un comando concreto:

```text
man <comando>
```

---

## Qué necesitas

- Python 3.10 o superior
- Poetry
- Git
- Terminal en Linux, macOS o Windows (Git Bash o WSL)

---

## Instalación

1. Clona el repositorio:

```text
git clone https://github.com/metsuke/mos2.git
cd mos2
```

2. Ejecuta el instalador:

```text
chmod +x install.sh
./install.sh
```

El instalador:

- prepara el entorno virtual local
- instala dependencias
- puede configurar aliases útiles
- resuelve Poetry según el perfil de entorno (ver sección Entornos de ejecución)

### Aliases opcionales

| Alias | Función |
|-------|---------|
| mos2 | Lanza MetsuOS |
| mos2f | Va a la raíz del proyecto |
| mos2u | Relanza el instalador |

---

## Entornos de ejecución

| Sistema | Entorno | Notas |
|---------|----------|-------|
| linux | native | Poetry habitual en PATH |
| macos | native | Igual |
| windows | git-bash | Lanzador prioriza poetry.exe / python -m poetry |
| windows | wsl | Clone en filesystem Linux; comportamiento tipo Linux |

Usa siempre `./install.sh` y `./mos2.sh` desde la **raíz del clone**.  
Normativa: `docs/ENVIRONMENTS.md`.

Si en Git Bash aparece *Permission denied* con el script `poetry` sin extensión, usa `./mos2.sh` (no invoques a mano `Scripts/poetry`).

---

## Arranque

```text
./mos2.sh
```

o, si tienes el alias:

```text
mos2
```

### Qué ocurre al arrancar

1. MetsuOS ejecuta la batería de tests.
2. Si algún test falla, el sistema no entra en modo interactivo.
3. Si todo pasa, verás algo similar a:

```text
Iniciando MOSh para MetsuOS...
Usuario: tu_usuario
Espacio personal: .../rootfs/home/tu_usuario/.mos
Usa 'exit' para salir, 'help' para ayuda

mosh/tu_usuario@metsuos:~$
```

---

## Conceptos básicos

### MOSh

Es el shell de MetsuOS. Lees comandos, los ejecutas y ves el resultado.

### Usuario

MetsuOS usa el nombre de usuario real de tu sistema anfitrión.

### Espacio personal

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 | Uso |
|---------|---------|---------|---------|---------|-----|
| rootfs/ | home/ | usuario/ | .mos/ | | Raíz personal |
| | | | | commands/ | Tus comandos |
| | | | | data/ | Tus datos |
| | | | | config/ | Tu configuración |
| | | | | apps/ | Apps instaladas de usuario |
| | | | | packages/ | Reserva de paquetes personales |
| | | | | repos/ | Reserva de repos personales |

Este contenido no se sube al repositorio principal.

### Comandos de sistema, de app y de usuario

- **Sistema:** los trae MetsuOS, protegidos (`moslib/commands/`).
- **App:** vienen de un paquete con identidad propia; no son un `user_*.py`.
- **Usuario:** los creas tú en tu espacio personal.

Prioridad si el nombre coincide: sistema > app de sistema > app de usuario > comando de usuario.

---

## Comandos de sistema

| Tipo | Comando | Descripción |
|------|---------|-------------|
| accesibilidad | a11y | Tests A11Y e informe en docs/a11y/ |
| apps | apps | Instalar, listar, ver y quitar apps |
| ayuda | docs | Listar y mostrar docs/ y ficheros públicos de la raíz |
| ayuda | help | Lista de comandos o ayuda de uno concreto |
| ayuda | man | Manual extendido (docs/man/ y man de apps) |
| calidad | synccheck | Compara HEAD local con origin/main |
| calidad | test | Batería de tests |
| calidad | update | Sincroniza con origin/main y tags (backup si hay cambios) |
| host | sysinfo | Información del anfitrión |
| host | uptime | Tiempo activo del anfitrión |
| host | version | Versión e historial Git |
| ia | iarouter | Modelos locales o remotos (apagado por defecto) |
| red | red | Diagnóstico de red del anfitrión (no es P2P) |
| sesion | exit | Sale del shell |
| tareas | hilos | Vista de tareas automáticas |
| tareas | tareas | GTD local |
| utilidad | clear | Limpia la pantalla |
| utilidad | echo | Imprime texto |

Norma de tablas: tipos en orden alfabético; dentro de cada tipo, comandos en orden alfabético.

Ejemplos:

```text
help
help version
man update
version
version -h 20
sysinfo
test
update
docs specs/00-OVERVIEW.md
synccheck
apps list
tareas
iarouter status
red
```

---

## Ayuda: help y man

### help

- `help` lista comandos y ayuda corta
- `help <comando>` muestra la ayuda específica

### man

- `man` lista páginas de manual disponibles
- `man <comando>` muestra el manual extendido

Los manuales viven en `docs/man/` y, si la app lo aporta, en el man de esa app.

### docs

- `docs` lista documentos bajo `docs/`
- `docs <ruta>` muestra un fichero de ese árbol o de la lista blanca de la raíz (README, CHANGELOG, AGENTS, LICENSE)

---

## Apps

Una app tiene `app.json` (id, nombre, versión, comandos). Se instala con el comando `apps` desde un directorio local o un repo git, en ámbito usuario o sistema.

Ejemplo versionado en este repositorio: `apps/dev`.

```text
apps list
apps show <id>
apps install <ruta-o-url>
apps remove <id>
```

Los comandos de la app se invocan por nombre corto, `id_cmd` o `app_id_cmd`. No pueden tapar un comando de sistema. Solo imports de stdlib, moslib y, si SEC lo admite, el mini-moslib de esa app.

---

## Tareas e hilos

```text
tareas
hilos
```

Tareas manuales y automáticas locales (GTD). Las automáticas pueden avanzar con un worker durante la sesión MOSh. No es la malla P2P. Detalle: `man tareas`, `man hilos`, spec 09.

---

## iarouter

Apagado por defecto. No llama a modelos hasta que actives un proveedor y uses `preguntar`.

```text
iarouter status
iarouter detectar
iarouter usar jan
iarouter modelos
iarouter modelo jan nombre del modelo
iarouter clave grok
iarouter preguntar hola
iarouter share
iarouter puente status
```

Claves en `.mos`, no se listan en status. Grok y OpenRouter pueden ingerir `XAI_API_KEY` y `OPENROUTER_API_KEY` al almacén. El puente HTTP `:17337` no es P2P. Detalle: `man iarouter` y spec 10.

Si Grok **dentro de X** responde «Something went wrong», eso es el cliente web de X, no este comando.

---

## Crear tus propios comandos

### Dónde crearlos

```text
rootfs/home/<tu_usuario>/.mos/commands/
```

### Nombre obligatorio

El archivo debe empezar por `user_` (ejemplo: `user_hola.py`).

### Contenido mínimo

```text
def execute(args):
    print("Hola desde mi comando personal")

def help():
    return "Uso: user_hola - Saluda desde el espacio de usuario"
```

### Cómo invocarlo

- Siempre: `user_hola`
- También: `hola` si no existe un comando de sistema (ni de app con prioridad) llamado `hola`

### Regla importante

Tu comando **no puede** sustituir un comando oficial del sistema.

---

## Seguridad de comandos

Solo se permiten imports de:

- biblioteca estándar de Python
- moslib
- mini-moslib de una app, solo en comandos de esa app

Un import ilegal hace que el comando se rechace; si sigue presente, el arranque puede bloquearse.

---

## Tests

### Desde fuera del shell

Con Poetry operativo en el PATH:

```text
poetry run pytest
```

Preferible usar el flujo del proyecto (`./mos2.sh` y luego `test`), que respeta la resolución de Poetry del entorno.

### Desde dentro del shell

```text
test
```

`a11y` ejecuta solo los tests de accesibilidad y regenera `docs/a11y/informe.md`.

### Al arrancar

Los tests se ejecutan solos. Si fallan, MetsuOS no abre la sesión interactiva.

---

## Actualizar MetsuOS

Dentro del shell:

```text
update
```

Qué hace:

1. Si hay cambios locales, los guarda en una rama backup con fecha y hora
2. Alinea tags locales con origin
3. Sincroniza main con origin/main de forma forzada
4. Limpia backups antiguos dejando un máximo controlado

Los módulos ya cargados en la sesión **no cambian solos** tras un update. Usa `update reiniciar` o `exit` y vuelve a lanzar `./mos2.sh`.

Emergencia desde fuera del shell: `mos2_forced_update.sh` (solo si sabes lo que implica).

`synccheck` compara HEAD local con origin/main sin aplicar el update.

---

## Flujo de trabajo recomendado

1. Arranca MetsuOS
2. Consulta `help` o `man`
3. Trabaja con comandos de sistema
4. Instala apps o crea comandos personales si lo necesitas
5. Ejecuta `test` cuando hagas cambios relevantes
6. Usa `update` para alinear tu copia local con el repositorio

---

## Problemas frecuentes

### El sistema no arranca

Causa habitual: tests en rojo o un comando de usuario o de app con import ilegal.

1. Revisar tests (`test` o `poetry run pytest` si aplica)
2. Revisar `rootfs/home/<usuario>/.mos/commands/` y apps instaladas
3. Corregir o quitar el comando ilegal
4. Volver a arrancar

### Permission denied con Poetry en Git Bash

Usa `./mos2.sh` o `./install.sh`. No ejecutes a mano el script `poetry` sin extensión del directorio Scripts de Python.

### Mi comando de usuario no aparece

1. Archivo en `commands/`
2. Nombre `user_algo.py`
3. Define `execute` y `help`
4. Sin imports ilegales

### Quiero un nombre corto y no funciona

Si existe un comando de sistema o de app con prioridad con ese nombre, ese gana. Usa `user_...`.

### iarouter dice que está apagado

Es el valor por defecto. `iarouter detectar` y `iarouter usar <id>` si está disponible.

---

## Dónde encontrar más documentación

| Documento | Contenido |
|-----------|-----------|
| docs/USER_MANUAL.md | Este manual |
| docs/ENVIRONMENTS.md | Perfiles de entorno y Poetry |
| docs/man/ | Manual extendido por comando |
| docs/METHODOLOGY.md | Cómo se desarrolla el proyecto |
| docs/STYLE_GUIDE.md | Normas de código |
| docs/specs/ | Especificaciones técnicas |
| README.md | Visión general del repositorio |

---

## Limitaciones de la fase Alpha

MetsuOS todavía no es un sistema operativo completo.

- no sustituye tu sistema anfitrión
- no es un kernel real
- no permite paquetes Python arbitrarios dentro de comandos
- no es la malla P2P ni una tienda remote de apps
- está en evolución activa

Aun así es usable como shell modular con seguridad, espacio personal, apps locales, tareas, tests y actualización controlada.

---

## Salir

```text
exit
```
