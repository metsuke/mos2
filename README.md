# MetsuOS (MOS2)

Sistema Operativo simulado y modular basado en Python

**Estado:** Alpha (funcional y en desarrollo activo)  
**Versión:** 0.2.1  
**Python** · **Licencia GPL-3.0** · **Poetry**

MetsuOS (también conocido como MOS2) es un sistema operativo simulado y modular escrito en Python.  
Implementa un shell interactivo llamado **MOSh** que carga dinámicamente comandos desde módulos Python independientes, inspirado en la estructura de un sistema Linux.

Proyecto personal de Metsuke.

---

## Características principales

- Shell interactivo propio (MOSh) con prompt personalizado
- Carga dinámica de comandos con **hot-reload** automático
- Estructura de directorios inspirada en Linux (`rootfs/`)
- **Espacio personal por usuario** basado en el nombre de usuario real del sistema operativo anfitrión
- Migración automática del espacio de usuario desde ubicaciones legacy
- Comandos del sistema protegidos (el usuario no puede sobrescribirlos)
- Comandos de usuario con prefijo `user_` (invocables también sin prefijo si no hay conflicto)
- **Validación de seguridad obligatoria**: solo se permiten imports de la biblioteca estándar y de `moslib`
- Tests unitarios y de seguridad con pytest
- Gestión de dependencias y entorno virtual con Poetry
- Scripts de instalación y lanzamiento multiplataforma (Linux, macOS y Windows/Git Bash)

---

## Estructura del proyecto

mos2/
├── moslib/                     # Núcleo del sistema
│   ├── core/
│   │   ├── shell.py            # Shell principal (MOSh)
│   │   ├── cmd_loader.py       # Cargador dinámico + seguridad
│   │   ├── user.py             # Usuario anfitrión + espacio personal + migración
│   │   └── security.py         # Validación de imports (AST)
│   └── commands/               # Comandos oficiales del sistema
│       ├── clear.py
│       ├── echo.py
│       ├── help.py
│       ├── sysinfo.py
│       ├── test.py             # Ejecuta la batería de tests
│       ├── uptime.py
│       └── version.py
├── rootfs/                     # Sistema de archivos simulado
│   ├── bin/
│   │   └── mos.py              # Punto de entrada
│   └── home/                   # Carpetas personales de los usuarios
│       └── <usuario>/
│           └── .mos/
│               ├── commands/   # Comandos personales (user_*.py)
│               ├── data/
│               ├── config/
│               ├── packages/
│               └── repos/
├── tests/                      # Tests unitarios y de seguridad
│   ├── conftest.py
│   ├── test_security.py
│   ├── test_user.py
│   └── test_cmd_loader.py
├── install.sh
├── mos2.sh
├── pyproject.toml
└── poetry.lock

> **Nota:** El contenido de `rootfs/home/` nunca se sube al repositorio (protegido por `.gitignore`).

---

## Requisitos

- Python 3.10 o superior
- Poetry instalado

---

## Instalación

git clone https://github.com/metsuke/mos2.git
cd mos2
chmod +x install.sh
./install.sh

El script `install.sh`:
- Configura Poetry para usar un entorno virtual local (`.venv`)
- Instala las dependencias
- Ofrece instalar aliases útiles (`mos2`, `mos2f`, `mos2u`, etc.)

### Aliases disponibles (opcionales)

| Alias   | Descripción                              |
|---------|------------------------------------------|
| `mos2`  | Lanza MetsuOS                            |
| `mos2f` | Cambia al directorio raíz del proyecto   |
| `mos2u` | Ejecuta de nuevo el instalador           |

---

## Uso

./mos2.sh
# o
mos2

Se abrirá el shell:

Iniciando MOSh para MetsuOS...
Usuario: tu_usuario_real
Espacio personal: .../rootfs/home/tu_usuario_real/.mos
Usa 'exit' para salir, 'help' para ayuda

mosh/tu_usuario_real@metsuos:~$

---

## Comandos del sistema

| Comando    | Descripción                                                                 |
|------------|-----------------------------------------------------------------------------|
| `help`     | Muestra la lista de comandos (sistema + usuario) o la ayuda de uno específico |
| `version`  | Muestra la versión actual (basada en Git). Usa `-h [n]` para historial     |
| `sysinfo`  | Información del hardware y estado del sistema anfitrión                     |
| `uptime`   | Tiempo de actividad del sistema operativo anfitrión                         |
| `echo`     | Imprime texto en la salida estándar                                         |
| `clear`    | Limpia la pantalla                                                          |
| `test`     | Ejecuta la batería de tests unitarios y de seguridad                        |
| `exit`     | Sale del shell                                                              |

---

## Cómo añadir comandos

### Comandos del sistema (oficiales)

Crea un archivo en `moslib/commands/` (ejemplo `hola.py`):

def execute(args):
    print("¡Hola desde MetsuOS!")

def help():
    return "Uso: hola - Saluda al usuario"

### Comandos de usuario (personales)

1. El sistema crea automáticamente la carpeta:
   rootfs/home/<tu_usuario>/.mos/commands/

2. Crea un archivo cuyo nombre **debe** empezar por `user_`:

# rootfs/home/tu_usuario/.mos/commands/user_hola.py
def execute(args):
    print("¡Hola desde mi espacio personal!")

def help():
    return "Uso: user_hola - Saluda desde el espacio de usuario"

#### Reglas de invocación de comandos de usuario

- Siempre se puede invocar con el nombre completo: `user_hola`
- También se puede invocar **sin el prefijo** (`hola`) **solo si** no existe un comando del sistema con ese mismo nombre
- El usuario **nunca** puede sobrescribir un comando del sistema

#### Regla de seguridad obligatoria

Todo comando (sistema o usuario) **solo puede importar**:
- Módulos de la biblioteca estándar de Python
- Módulos de `moslib` (y submódulos)

Cualquier otro import (por ejemplo `requests`, `numpy`, etc.) hace que el comando sea **rechazado** automáticamente.

---

## Tests

Ejecutar la batería de tests:

poetry run pytest

O desde dentro del shell de MetsuOS:

test

Los tests cubren:
- Validación de seguridad de imports
- Módulo de usuario y espacio personal
- Cargador de comandos (incluyendo rechazo de comandos inseguros)

---

## Desarrollo

# Activar entorno
poetry shell

# Ejecutar el sistema
poetry run python rootfs/bin/mos.py

# Ejecutar tests
poetry run pytest

La lógica de negocio y utilidades se concentran en `moslib/`.

---

## Licencia

Este proyecto está licenciado bajo la **GNU General Public License v3.0**.  
Consulta el archivo `LICENSE` para más detalles.

Copyright (C) 2026 Metsuke

---

## Autor

**Metsuke**  
Sitio web: https://metsuke.com  
Repositorio: https://github.com/metsuke/mos2

> **Nota:** MetsuOS es un proyecto experimental en fase Alpha.  
> Aunque ya es funcional como shell con espacio de usuario, seguridad de imports y tests, todavía no pretende ser un sistema operativo completo. ¡Las contribuciones e ideas son bienvenidas!