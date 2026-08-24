# Manual de usuario de MetsuOS (MOS2)

**Versión del documento:** 1.0  
**Baseline de referencia:** v0.2.1  
**Estado:** Manual formal de usuario  
**Documentos relacionados:** docs/man/, docs/METHODOLOGY.md, docs/specs/01-SSS-System-Specification.md

---

## 1. Introducción

MetsuOS (también llamado MOS2) es un sistema operativo simulado y modular escrito en Python.

Su interfaz principal es el shell **MOSh**, donde puedes ejecutar:

- comandos oficiales del sistema
- comandos personales de usuario
- utilidades de ayuda, tests, actualización y documentación

Este manual explica cómo instalar, arrancar y usar MetsuOS en la práctica.

Para ayuda extendida de un comando concreto, usa:

man <comando>

---

## 2. Qué necesitas

- Python 3.10 o superior
- Poetry
- Git
- Terminal en Linux, macOS o Windows con Git Bash

---

## 3. Instalación

1. Clona el repositorio:

git clone https://github.com/metsuke/mos2.git
cd mos2

2. Ejecuta el instalador:

chmod +x install.sh
./install.sh

El instalador:

- prepara el entorno virtual local
- instala dependencias
- puede configurar aliases útiles

### Aliases opcionales

| Alias | Función |
|-------|---------|
| mos2 | Lanza MetsuOS |
| mos2f | Va a la raíz del proyecto |
| mos2u | Relanza el instalador |

---

## 4. Arranque

Puedes iniciar el sistema así:

./mos2.sh

o, si tienes el alias:

mos2

### Qué ocurre al arrancar

1. MetsuOS ejecuta la batería de tests.
2. Si algún test falla, el sistema no entra en modo interactivo.
3. Si todo pasa, verás algo similar a:

Iniciando MOSh para MetsuOS...
Usuario: tu_usuario
Espacio personal: .../rootfs/home/tu_usuario/.mos
Usa 'exit' para salir, 'help' para ayuda

mosh/tu_usuario@metsuos:~$

---

## 5. Conceptos básicos

### 5.1 MOSh

Es el shell de MetsuOS. Lees comandos, los ejecutas y ves el resultado.

### 5.2 Usuario

MetsuOS usa el nombre de usuario real de tu sistema anfitrión.

### 5.3 Espacio personal

Cada usuario tiene un espacio propio:

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 | Uso |
|---------|---------|---------|---------|---------|-----|
| rootfs/ | home/ | `<usuario>/` | .mos/ | | Raíz personal |
| | | | | commands/ | Tus comandos |
| | | | | data/ | Tus datos |
| | | | | config/ | Tu configuración |
| | | | | packages/ | Reserva de paquetes personales |
| | | | | repos/ | Reserva de repos personales |

Este contenido no se sube al repositorio principal.

### 5.4 Comandos de sistema y de usuario

- **Sistema:** los trae MetsuOS, protegidos.
- **Usuario:** los creas tú en tu espacio personal.

---

## 6. Comandos de sistema

| Comando | Para qué sirve |
|---------|----------------|
| help | Ayuda corta de comandos |
| man | Manual extendido de un comando |
| version | Versión e historial |
| sysinfo | Información del equipo anfitrión |
| uptime | Tiempo activo del anfitrión |
| echo | Imprime texto |
| clear | Limpia la pantalla |
| test | Ejecuta la batería de tests |
| update | Actualiza MetsuOS desde el repositorio |
| exit | Sale del shell |

Ejemplos:

help
help version
man update
version
version -h 20
sysinfo
test
update

---

## 7. Ayuda: help y man

### 7.1 help

- `help` lista comandos y ayuda corta
- `help <comando>` muestra la ayuda específica

### 7.2 man

- `man` lista páginas de manual disponibles
- `man <comando>` muestra el manual extendido de ese comando

Los manuales viven en docs/man/ y están pensados para explicación más completa que help.

---

## 8. Crear tus propios comandos

### 8.1 Dónde crearlos

rootfs/home/<tu_usuario>/.mos/commands/

### 8.2 Nombre obligatorio

El archivo debe empezar por `user_`

Ejemplo:

user_hola.py

### 8.3 Contenido mínimo

def execute(args):
    print("Hola desde mi comando personal")

def help():
    return "Uso: user_hola - Saluda desde el espacio de usuario"

### 8.4 Cómo invocarlo

- Siempre: `user_hola`
- También: `hola` si no existe un comando de sistema llamado `hola`

### 8.5 Regla importante

Tu comando **no puede** sustituir un comando oficial del sistema.

---

## 9. Seguridad de comandos

MetsuOS solo permite que un comando importe:

- biblioteca estándar de Python
- moslib

Si escribes, por ejemplo:

import jander

el comando será rechazado.

También:

- si intentas ejecutarlo, verás un error de seguridad
- si ese comando ilegal sigue presente, el sistema puede negarse a arrancar hasta que lo corrijas

Esto protege el modelo modular de MetsuOS.

---

## 10. Tests

### 10.1 Desde fuera del shell

poetry run pytest

### 10.2 Desde dentro del shell

test

### 10.3 Al arrancar

Los tests se ejecutan solos.  
Si fallan, MetsuOS no abre la sesión interactiva.

---

## 11. Actualizar MetsuOS

Dentro del shell:

update

Qué hace:

1. Si tienes cambios locales pendientes, los guarda en una rama backup con fecha y hora
2. Sincroniza main con origin/main de forma forzada
3. Limpia backups antiguos dejando un máximo controlado

Si solo quieres un reset de emergencia desde fuera del shell, existe el script:

mos2_forced_update.sh

Úsalo solo si sabes lo que implica.

---

## 12. Flujo de trabajo recomendado

1. Arranca MetsuOS
2. Consulta `help` o `man`
3. Trabaja con comandos de sistema
4. Crea comandos personales si lo necesitas
5. Ejecuta `test` cuando hagas cambios relevantes
6. Usa `update` para alinear tu copia local con el repositorio

---

## 13. Problemas frecuentes

### El sistema no arranca

Causa habitual: tests en rojo o un comando de usuario con import ilegal.

Qué hacer:

1. poetry run pytest
2. Revisar rootfs/home/<usuario>/.mos/commands/
3. Corregir o quitar el comando ilegal
4. Volver a arrancar

### Mi comando de usuario no aparece

Comprueba:

1. que el archivo esté en commands/
2. que se llame user_algo.py
3. que defina execute y help
4. que no tenga imports ilegales

### Quiero usar un nombre corto y no funciona

Si existe un comando de sistema con ese nombre, el sistema siempre gana.  
Usa el nombre completo user_...

---

## 14. Dónde encontrar más documentación

| Documento | Contenido |
|-----------|-----------|
| docs/USER_MANUAL.md | Este manual |
| docs/man/<comando>.md | Manual extendido de cada comando |
| docs/METHODOLOGY.md | Cómo se desarrolla el proyecto |
| docs/STYLE_GUIDE.md | Normas de código |
| docs/specs/ | Especificaciones técnicas |
| README.md | Visión general del repositorio |

---

## 15. Limitaciones de la fase Alpha

MetsuOS todavía no es un sistema operativo completo.

En esta fase:

- no sustituye tu sistema anfitrión
- no es un kernel real
- no permite instalar paquetes Python arbitrarios dentro de comandos
- está en evolución activa

Aun así, ya es usable como shell modular con seguridad, espacio personal, tests y actualización controlada.

---

## 16. Salir

Para cerrar MOSh:

exit