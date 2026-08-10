MetsuOS (MOS2)

Sistema Operativo simulado y modular basado en Python

Estado
Python
Licencia
Poetry

MetsuOS (también conocido como MOS2) es un sistema operativo simulado y modular escrito en Python.  
Implementa un shell interactivo llamado MOSh que carga dinámicamente comandos desde módulos Python independientes, inspirado en la estructura de un sistema Linux.

Proyecto personal de Metsuke. Actualmente en fase Alpha (funcional pero en desarrollo activo).

Características principales

Shell interactivo propio (MOSh) con prompt personalizado
Carga dinámica de comandos (hot-reload automático al modificar un comando)
Estructura de directorios inspirada en Linux (rootfs/)
Gestión de dependencias y entorno virtual con Poetry
Scripts de instalación y lanzamiento multiplataforma (Linux, macOS y Windows/Git Bash)
Comandos nativos para información del sistema, uptime, versión, etc.
Fácil extensibilidad: añadir un nuevo comando es tan simple como crear un archivo .py

Estructura del proyecto

| Nivel 1     | Nivel 2       | Nivel 3          | Descripción                              |
|-------------|---------------|------------------|------------------------------------------|
| moslib/     |               |                  | Núcleo del sistema                       |
|             | core/         |                  | Componentes principales del shell        |
|             |               | shell.py         | Shell principal (MOSh)                   |
|             |               | cmd_loader.py    | Cargador dinámico de comandos            |
|             | commands/     |                  | Comandos del sistema                     |
|             |               | clear.py         | Limpia la pantalla                       |
|             |               | echo.py          | Imprime texto                            |
|             |               | help.py          | Sistema de ayuda                         |
|             |               | sysinfo.py       | Información del sistema                  |
|             |               | uptime.py        | Tiempo de actividad                      |
|             |               | version.py       | Versión e historial                      |
| rootfs/     |               |                  | Estructura estilo Linux                  |
|             | bin/          |                  | Ejecutables del sistema                  |
|             |               | mos.py           | Punto de entrada del sistema             |
| install.sh  |               |                  | Script de instalación y aliases          |
| mos2.sh     |               |                  | Lanzador principal                       |
| pyproject.toml |            |                  | Configuración de Poetry                  |
| poetry.lock |               |                  | Lock de dependencias                     |

Requisitos

Python 3.10 o superior
Poetry instalado

Instalación

Clonar el repositorio
git clone https://github.com/metsuke/mos2.git
cd mos2

Ejecutar el instalador
chmod +x install.sh
./install.sh

El script install.sh:
Configura Poetry para usar un entorno virtual local (.venv)
Instala las dependencias
Ofrece instalar aliases útiles en tu shell (mos2, mos2f, mos2u, etc.)

Aliases disponibles (opcionales)

| Alias   | Descripción                              |
|---------|------------------------------------------|
| mos2  | Lanza MetsuOS                            |
| mos2f | Cambia al directorio raíz del proyecto   |
| mos2u | Ejecuta de nuevo el instalador           |

Uso

Una vez instalado, puedes iniciar el sistema de varias formas:

Usando el script de lanzamiento
./mos2.sh

O con el alias (si lo instalaste)
mos2

Se abrirá el shell MOSh:

Iniciando MOSh para MetsuOS...
Usa 'exit' para salir, 'help' para ayuda
mosh/metsuke@metsuos:~$ 

Comandos disponibles

| Comando     | Descripción                                                                 |
|-------------|-----------------------------------------------------------------------------|
| help      | Muestra la lista de comandos o la ayuda de uno específico                   |
| version   | Muestra la versión actual (basada en Git). Usa -h [n] para historial     |
| sysinfo   | Información del hardware y estado del sistema anfitrión                     |
| uptime    | Tiempo de actividad del sistema operativo anfitrión                         |
| echo      | Imprime texto en la salida estándar                                         |
| clear     | Limpia la pantalla                                                          |
| exit      | Sale del shell                                                              |

Cómo añadir un nuevo comando

Crea un archivo en moslib/commands/ (ejemplo: hola.py):

def execute(args):
    print("¡Hola desde MetsuOS!")

def help():
    return "Uso: hola - Saluda al usuario"

¡Listo! El comando estará disponible inmediatamente (el cargador detecta cambios automáticamente).

No es necesario reiniciar el shell ni registrar el comando en ningún sitio.

Desarrollo

Activar el entorno virtual de Poetry
poetry shell

O ejecutar comandos directamente
poetry run python rootfs/bin/mos.py

El proyecto está diseñado para crecer de forma modular. La lógica de negocio y utilidades se concentran en moslib/.

Licencia

Este proyecto está licenciado bajo la GNU General Public License v3.0.  
Consulta el archivo LICENSE para más detalles.

Copyright (C) 2026 Metsuke

Autor

Metsuke  
Sitio web: https://metsuke.com  
Repositorio: https://github.com/metsuke/mos2

Nota: MetsuOS es un proyecto experimental en fase Alpha.  
Aunque ya es funcional como shell, todavía no pretende ser un sistema operativo completo. ¡Las contribuciones e ideas son bienvenidas!
`