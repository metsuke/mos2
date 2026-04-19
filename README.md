# MOS2 - MetsuOS System Core

Estructura de sistema basada en Linux gestionada con Python y Poetry.

## Estructura del Proyecto
* **moslib/**: Núcleo de funciones y gestión de dependencias (Poetry).
* **etc/, usr/, bin/**: Scripts de sistema que consumen la lógica de `moslib`.
* **home/**: Estructura de usuarios (vacía por seguridad).

## Instalación
Ejecuta el script de despliegue:
```bash
./install.sh

## Licencia
Este proyecto está bajo la licencia GNU GPL v3. Consulta el archivo [LICENSE](LICENSE) para más detalles.