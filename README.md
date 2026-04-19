# MOS2 - MetsuOS System Core

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/Package%20Manager-Poetry-60A5FA?logo=poetry&logoColor=white)](https://python-poetry.org/)

> **Estado:** ⚠️ En desarrollo (No funcional actualmente).

**MOS2** es un proyecto de arquitectura de sistema diseñado por **Metsuke**. Implementa una estructura "espejo" de Linux donde la lógica de sistema es gestionada por scripts de Python que consumen un núcleo de servicios centralizado.

## 🏗 Arquitectura del Sistema

El proyecto replica la jerarquía de un sistema operativo Linux para facilitar su despliegue y organización:

* **/moslib/**: El corazón del proyecto. Contiene las librerías base, utilidades y la lógica de negocio que consumen el resto de scripts.
* **/bin, /etc, /usr**: Carpetas de sistema que contienen scripts ejecutables y configuraciones que importan la lógica de `moslib`.
* **/home**: Estructura de directorios de usuario. Está protegida mediante reglas de Git para que la carpeta exista en el despliegue pero no se suban datos privados de los usuarios locales.
* **Gestión de Dependencias**: El proyecto utiliza **Poetry**. Aunque la lógica reside en `moslib`, el entorno virtual (`.venv`) y las dependencias se gestionan desde la raíz para unificar el contexto de ejecución.

## 🚀 Instalación y Despliegue

Este proyecto está diseñado para ser desplegado mediante un script de instalación automatizado que prepara el entorno de Python.

### Requisitos previos
- Python 3.10 o superior
- Poetry instalado en el sistema

### Despliegue rápido
Clona el repositorio y ejecuta el script de instalación:

```bash
git clone git@github.com:metsuke/mos2.git
cd mos2
chmod +x install.sh
./install.sh