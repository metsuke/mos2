# Manual de usuario de MetsuOS (MOS2)

**Versión del documento:** 1.2  
**Baseline de referencia:** v0.2.7 (árbol hacia v0.2.8)  
**Estado:** Manual formal de usuario  
**Documentos relacionados:** docs/man/, docs/ENVIRONMENTS.md, docs/METHODOLOGY.md, docs/specs/01-SSS-System-Specification.md, docs/specs/08-APPS.md, docs/specs/09-TASKS.md, docs/specs/10-IA-ROUTER.md

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

La v1.1 se conserva. Esta v1.2 añade apps, tareas, iarouter, red y `update reiniciar`.

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
| | | | | apps/ | Apps de ámbito usuario |
| | | | | data/ | Tus datos |
| | | | | config/ | Tu configuración |
| | | | | packages/ | Reserva de paquetes personales |
| | | | | repos/ | Reserva de repos personales |

Este contenido no se sube al repositorio principal.

### Comandos de sistema, de app y de usuario

- **Sistema:** los trae MetsuOS, protegidos. Ganan siempre si el nombre coincide.
- **App:** viven en una app instalada (usuario o sistema).
- **Usuario:** los creas tú en `.mos/commands/` con prefijo `user_`.

Prioridad: sistema > app de sistema > app de usuario > comando `user_`.

---

## Comandos de sistema

| Tipo | Comando | Descripción |
|------|---------|-------------|
| accesibilidad | a11y | Tests A11Y e informe |
| apps | apps | Instalar, listar, ver y quitar apps |
| ayuda | docs | Lista y muestra docs/ y ficheros públicos de la raíz |
| ayuda | help | Lista de comandos o ayuda de uno concreto |
| ayuda | man | Manual extendido (docs/man/ y man de app) |
| calidad | synccheck | Compara HEAD local con origin/main |
| calidad | test | Batería de tests |
| calidad | update | Sincroniza con origin/main (backup si hay cambios) |
| host | sysinfo | Información del anfitrión |
| host | uptime | Tiempo activo del anfitrión |
| host | version | Versión e historial Git |
| ia | iarouter | Modelos locales/remotos; apagado hasta que lo actives |
| red | red | Diagnóstico de red del anfitrión (no es P2P) |
| sesion | exit | Sale del shell |
| tareas | hilos | Vista de tareas por clase |
| tareas | tareas | Tareas locales (GTD) |
| utilidad | clear | Limpia la pantalla |
| utilidad | echo | Imprime texto |

Norma de tablas: tipos en orden alfabético; dentro de cada tipo, comandos en orden alfabético.

Ejemplos:

```text
help
help version
man update
docs
a11y
synccheck
apps list
tareas
hilos
iarouter
red
version
sysinfo
test
update
update reiniciar
```

---

## Ayuda: help, man y docs

### help

- `help` lista comandos y ayuda corta
- `help <comando>` muestra la ayuda específica

### man

- `man` lista páginas de manual disponibles
- `man <comando>` muestra el manual extendido

Los manuales de sistema viven en `docs/man/`. Una app puede aportar el suyo.

### docs

- `docs` lista documentos
- `docs <ruta>` muestra un fichero bajo `docs/` o README, CHANGELOG, AGENTS, LICENSE


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
- También: `hola` si no existe un comando de sistema ni de app con más prioridad llamado `hola`

### Regla importante

Tu comando **no puede** sustituir un comando oficial del sistema.

---

## Apps

```text
apps list
apps show <id>
apps install <ruta-o-repo>
apps remove <id>
```

Una app no es un `user_*.py`. Lleva `app.json` y comandos propios. Sin A11Y mínima no se acepta. Detalle: `docs/specs/08-APPS.md` y `man apps`.

---

## Tareas e hilos

```text
tareas
hilos
```

Son locales a tu sesión y a tu espacio. No son la malla P2P. Detalle: `docs/specs/09-TASKS.md`.

---

## iarouter

```text
iarouter
```

Va apagado hasta que lo actives (`usar` / `preguntar`). No lista claves. Jan y GPT4All son locales; Grok y OpenRouter necesitan clave. El puente HTTP, si lo enciendes, no es P2P. Detalle: `docs/specs/10-IA-ROUTER.md`.

---

## Seguridad de comandos

Solo se permiten imports de:

- biblioteca estándar de Python
- moslib
- en un comando de app: minimoslib de esa app

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

### Al arrancar

Los tests se ejecutan solos. Si fallan, MetsuOS no abre la sesión interactiva.

También puedes lanzar solo A11Y:

```text
a11y
```

---

## Actualizar MetsuOS

Dentro del shell:

```text
update
```

Qué hace:

1. Si hay cambios locales, los guarda en una rama backup con fecha y hora
2. Sincroniza main con origin/main de forma forzada
3. Alinea tags locales con origin
4. Limpia backups antiguos dejando un máximo controlado

Los módulos ya cargados en esta sesión **no cambian solos**. Después de un update:

```text
update reiniciar
```

o sal con `exit` y vuelve a lanzar `./mos2.sh`.

Comprobar sin actualizar:

```text
synccheck
```

Emergencia desde fuera del shell: `mos2_forced_update.sh` (solo si sabes lo que implica).

---

## Flujo de trabajo recomendado

1. Arranca MetsuOS
2. Consulta `help`, `man` o `docs`
3. Trabaja con comandos de sistema
4. Instala apps o crea comandos personales si lo necesitas
5. Ejecuta `test` cuando hagas cambios relevantes
6. Usa `update` y luego `update reiniciar` para alinear tu copia con el repositorio

---

## Problemas frecuentes

### El sistema no arranca

Causa habitual: tests en rojo o un comando de usuario con import ilegal.

1. Revisar tests (`test` o `poetry run pytest` si aplica)
2. Revisar `rootfs/home/<usuario>/.mos/commands/`
3. Corregir o quitar el comando ilegal
4. Volver a arrancar

### Permission denied con Poetry en Git Bash

Usa `./mos2.sh` o `./install.sh`. No ejecutes a mano el script `poetry` sin extensión del directorio Scripts de Python.

### Mi comando de usuario no aparece

1. Archivo en `commands/`
2. Nombre `user_algo.py`
3. Define `execute` y `help`
4. Sin imports ilegales
5. Que no lo tape un comando de sistema o de app

### Quiero un nombre corto y no funciona

Si existe un comando de sistema o de app con ese nombre, ese gana. Usa `user_...`.

### Tras update no veo el código nuevo

Usa `update reiniciar` o sal y vuelve a entrar.


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
| docs/A11Y.md | Política de accesibilidad |
| README.md | Visión general del repositorio |
| CHANGELOG.md | Historial de releases |

---

## Limitaciones de la fase Alpha

MetsuOS todavía no es un sistema operativo completo.

- no sustituye tu sistema anfitrión
- no es un kernel real
- no permite paquetes Python arbitrarios dentro de comandos
- no es la malla P2P ni una tienda remota de apps
- está en evolución activa

Aun así es usable como shell modular con seguridad, espacio personal, apps locales, tareas, iarouter (off por defecto), tests y actualización controlada.

---

## Salir

```text
exit
```