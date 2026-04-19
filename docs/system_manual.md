Aquí tienes el **Manual Técnico de MOS2** consolidado. Este documento incluye todas las decisiones de arquitectura, la paleta de colores final para accesibilidad universal y la estructura de archivos que hemos construido.

Te recomiendo guardar este contenido en `docs/system_manual.md`.

-----

# 📘 Manual Técnico de MOS2 (MetsuOS System Core)

**Versión:** 1.0.0-beta  
**Autor:** Metsuke ([enlace sospechoso eliminado])  
**Licencia:** GNU GPL v3  
**Propiedad:** MetsuOS Plugin Reference

-----

## 1\. Introducción

MOS2 es un entorno de shell autónomo desarrollado en Python que emula la jerarquía de un sistema Linux. Utiliza un modelo de **VFS (Virtual File System)** para aislar las operaciones del usuario dentro de la estructura del proyecto, permitiendo la portabilidad total entre macOS, Windows (WSL) y Linux.

-----

## 2\. Arquitectura de Archivos y VFS

El sistema trata la raíz del repositorio como el directorio raíz lógico (`/`).

### Tabla de Montajes (Static Mounts)

| Ruta Lógica (MOS2) | Ruta Física (Host) | Descripción |
| :--- | :--- | :--- |
| `/` | `[project_root]/` | Raíz del sistema MOS2. |
| `/bin` | `[project_root]/bin/` | Binarios y puntos de entrada del sistema. |
| `/etc` | `[project_root]/etc/` | Archivos de configuración (futuros .conf). |
| `~/` | `[project_root]/home/[user]/` | Home virtual persistente del usuario. |

> **Nota de Seguridad:** Gracias al `.gitignore` configurado, el contenido de `home/` es local y nunca se sincroniza con el repositorio remoto de GitHub.

-----

## 3\. Especificaciones de Interfaz (UI/UX)

Para garantizar la legibilidad en cualquier terminal (fondo claro o oscuro), se ha seleccionado una paleta basada en **ZX Spectrum** con optimización de contraste **WCAG AAA**.

### Paleta de Colores Institucional

| Elemento | Color Spectrum | Código ANSI | Justificación |
| :--- | :--- | :--- | :--- |
| **Branding / [MOSh]** | **Magenta Bright** | `\033[1;95m` | Máximo contraste universal (AAA). |
| **User @ Host** | **Green Bright** | `\033[1;92m` | Estándar de visibilidad. |
| **Rutas (Paths)** | **Cyan Bright** | `\033[1;96m` | Distinción clara de jerarquía. |
| **Separadores ($)** | **White Bright** | `\033[1;97m` | Neutro de alta luminancia. |

-----

## 4\. Componentes del Core

### 4.1 EntryPoint (`bin/mos`)

Script ejecutable sin extensión que inicializa el sistema.

  - **Bootloader:** Configura el `sys.path` para incluir `moslib`.
  - **Banner:** Muestra el logo ASCII en Magenta Brillante usando *Raw Strings* para evitar errores de sintaxis en Python 3.12+.

### 4.2 Kernel (`moslib/core/kernel.py`)

El "corazón" del sistema. Responsable de:

  - **Identidad:** Carga el usuario (`getpass`) y el hostname (`platform.node`).
  - **Navegación:** Traduce rutas físicas a lógicas para el prompt.
  - **Aislamiento:** Asegura que el usuario comience siempre en su `virtual_home`.

### 4.3 Shell (`moslib/core/shell.py`)

Interfaz de comandos (REPL).

  - **Prefix:** Identifica la sesión con el tag `[MOSh]`.
  - **Modo Bridge:** Ejecuta comandos de Python internos (`cd`, `pwd`, `fetch`) y delega el resto al shell del sistema operativo anfitrión.

-----

## 5\. Log de Decisiones Técnicas (ADR)

  * **Detección Dinámica de Color:** Se descartó la detección automática de fondo por inestabilidad en terminales antiguas. En su lugar, se adoptó el **Magenta Brillante** como color universal AAA.
  * **Heredabilidad de Usuario:** Se decidió heredar el nombre del usuario del SO Host para garantizar que los permisos de escritura en la carpeta `home/` local sean automáticos y sin fricciones.
  * **No-Extensión en Binarios:** Los archivos en `/bin` no llevan `.py` para mimetizarse con el estándar de binarios de Linux/Unix.

-----

## 6\. Comandos del Sistema

  * `cd [dir]`: Cambia el directorio de trabajo dentro del VFS.
  * `pwd`: Muestra la ruta actual relativa a la raíz de MOS2.
  * `fetch`: Muestra el estado del Kernel y puntos de montaje activos.
  * `exit / logout`: Cierra la sesión de MOS2 de forma segura.

-----

*Manual actualizado el 19 de abril de 2026.*
