# 01 – SSS · Especificación de sistema

**Versión del documento:** 1.0  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/specs/00-OVERVIEW.md, docs/specs/04-SEC-Security-Policy.md

---

## 1. Propósito

Este documento define qué es MetsuOS a nivel de sistema, sus objetivos, no-objetivos y normas no negociables.

Todo diseño, requisito software e implementación debe ser compatible con esta especificación.

---

## 2. Identificación del sistema

| Campo | Valor |
|-------|-------|
| Nombre | MetsuOS |
| Nombre alternativo | MOS2 |
| Tipo | Sistema operativo simulado y modular |
| Shell | MOSh |
| Lenguaje principal | Python 3.10+ |
| Licencia | GPL-3.0 |
| Estado | Alpha |
| Baseline actual | v0.2.1 |

---

## 3. Definición del sistema

MetsuOS es un entorno operativo simulado que proporciona:

- Un shell interactivo propio (MOSh)
- Un núcleo modular (`moslib`)
- Un sistema de archivos simulado inspirado en Linux (`rootfs`)
- Un espacio personal por usuario del sistema anfitrión
- Comandos implementados como módulos Python independientes
- Validación de seguridad de imports
- Tests de arranque obligatorios

MetsuOS se ejecuta sobre un sistema operativo anfitrión y no reemplaza su kernel.

---

## 4. Objetivos del sistema

1. Ofrecer un shell modular, extensible y auditable.
2. Permitir comandos de sistema y de usuario con reglas claras.
3. Garantizar aislamiento del espacio personal del usuario.
4. Impedir que comandos carguen código fuera de la política de seguridad.
5. Ser agnóstico de plataforma en los entornos soportados.
6. Evolucionar sin romper funcionalidad existente mediante specs, tests y proceso controlado.

---

## 5. No-objetivos

MetsuOS, en esta baseline, **no** pretende:

1. Ser un kernel real.
2. Virtualizar hardware completo.
3. Sustituir el sistema de usuarios del sistema anfitrión.
4. Permitir instalación arbitraria de paquetes Python dentro de comandos.
5. Ofrecer compatibilidad POSIX completa.
6. Multiplexar procesos reales como un sistema operativo nativo.
7. Garantizar seguridad frente a un atacante con acceso de escritura al código del núcleo fuera de las validaciones definidas.

---

## 6. Normas no negociables

Las siguientes normas son férreas. No se pueden debilitar por comodidad.

### 6.1 Todo pasa por mosLib

La lógica de sistema y la extensión controlada del entorno se canalizan a través de `moslib`.

### 6.2 Política de imports

Los comandos solo pueden importar:

- biblioteca estándar de Python
- `moslib` y sus submódulos

Cualquier otro import está prohibido.

### 6.3 Protección de comandos de sistema

Un comando de usuario no puede sobrescribir un comando de sistema.

### 6.4 Contrato de comando

Todo comando debe exponer:

- `execute(args)`
- `help()` que devuelve `str`

### 6.5 Espacio de usuario aislado

El espacio personal del usuario vive fuera del árbol versionado de producto y no se publica en el repositorio principal.

### 6.6 Tests de arranque

Si la batería de tests de arranque falla, el sistema no debe iniciar sesión interactiva.

### 6.7 Agnosticismo de plataforma

El sistema debe poder instalarse y ejecutarse en Linux, macOS y Windows mediante Git Bash o entorno compatible, sin asumir una única plataforma.

---

## 7. Contexto operativo

### 7.1 Sistema anfitrión

MetsuOS usa el usuario real del sistema anfitrión para:

- personalizar el prompt
- resolver el directorio home simulado del usuario
- aislar datos y comandos personales

### 7.2 Estructura lógica del sistema

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Descripción |
|---------|---------|---------|---------|-------------|
| moslib/ | | | | Núcleo del sistema |
| | core/ | | | Componentes principales |
| | | shell.py | | Shell MOSh |
| | | cmd_loader.py | | Carga de comandos y seguridad en runtime |
| | | user.py | | Usuario y espacio personal |
| | | security.py | | Validación de imports |
| | commands/ | | | Comandos oficiales de sistema |
| rootfs/ | | | | Sistema de archivos simulado |
| | bin/ | | | Punto de entrada |
| | | mos.py | | Lanzador del shell |
| | home/ | | | Homes de usuario |
| | | `<usuario>/` | | Home del usuario anfitrión |
| | | | .mos/ | Espacio privado MetsuOS |
| tests/ | | | | Batería de tests |
| docs/ | | | | Metodología, specs, manual y man |

### 7.3 Espacio personal del usuario

Estructura mínima del espacio personal:

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 | Descripción |
|---------|---------|---------|---------|---------|-------------|
| rootfs/ | home/ | `<usuario>/` | .mos/ | | Raíz privada del usuario |
| | | | | commands/ | Comandos personales `user_*.py` |
| | | | | data/ | Datos del usuario |
| | | | | config/ | Configuración del usuario |
| | | | | packages/ | Metadatos de paquetes de usuario |
| | | | | repos/ | Repositorios personales |

El contenido de `rootfs/home/` no se versiona como producto.

---

## 8. Capacidades de sistema requeridas

### 8.1 Shell interactivo

El sistema debe proporcionar un shell con:

- prompt identificable
- lectura de comandos
- resolución de comandos de sistema y de usuario
- salida de errores comprensible
- comando de salida (`exit`)

### 8.2 Comandos de sistema

El sistema debe incluir, como mínimo en esta baseline:

| Comando | Función general |
|---------|-----------------|
| help | Ayuda de comandos |
| version | Versión e historial |
| sysinfo | Información del anfitrión |
| uptime | Tiempo de actividad del anfitrión |
| echo | Eco de texto |
| clear | Limpieza de pantalla |
| test | Ejecución de la batería de tests |
| update | Actualización forzada desde origin/main con backup local |

### 8.3 Comandos de usuario

El sistema debe permitir comandos personales:

- archivo con prefijo `user_`
- invocación con prefijo completo siempre
- invocación sin prefijo solo si no hay conflicto con un comando de sistema

### 8.4 Seguridad

El sistema debe validar comandos:

- en tiempo de carga/ejecución
- en arranque, sobre comandos de sistema y del usuario actual

### 8.5 Actualización

El sistema debe poder sincronizarse con el repositorio remoto de forma controlada, preservando trabajo local en ramas de backup cuando existan cambios pendientes.

### 8.6 Documentación

El sistema debe disponer de:

- metodología de desarrollo
- especificaciones
- guía de estilo
- manual de usuario
- páginas man por comando
- comando `man` para consultarlas

Nota: la existencia del comando `man` y sus páginas forma parte de la evolución documental/funcional iniciada sobre la baseline v0.2.1.

---

## 9. Restricciones de diseño de sistema

1. No introducir gestores de paquetes Python genéricos dentro del modelo de comandos.
2. No permitir que el usuario reemplace el núcleo modificando solo su espacio personal.
3. No acoplar el núcleo a una única distribución Linux.
4. No depender de servicios de red para el arranque básico.
5. No debilitar los tests de arranque para facilitar un cambio puntual.

---

## 10. Requisitos de calidad de sistema

### 10.1 Modularidad

Los comandos deben poder añadirse como archivos independientes sin reescribir el shell.

### 10.2 Auditabilidad

Las reglas críticas de seguridad deben estar centralizadas y ser verificables por tests.

### 10.3 Robustez de evolución

Los cambios se introducen por fases, con commits atómicos, ramas feature y verificación previa a merge.

### 10.4 Claridad de uso

Los mensajes orientados a usuario final deben estar en español y ser accionables.

---

## 11. Interfaces de sistema de alto nivel

### 11.1 Interfaz humano-shell

Entrada: línea de texto  
Salida: texto en terminal  
Control: comandos del sistema y de usuario

### 11.2 Interfaz núcleo-comandos

El núcleo carga módulos de comando desde directorios conocidos y les exige el contrato `execute` / `help`.

### 11.3 Interfaz núcleo-seguridad

Ningún comando se ejecuta si incumple la política de imports.

### 11.4 Interfaz núcleo-usuario

El núcleo resuelve el usuario anfitrión y asegura su espacio `.mos`.

### 11.5 Interfaz producto-repositorio

El producto puede actualizarse desde `origin/main` mediante mecanismos controlados de sincronización.

---

## 12. Criterios de aceptación de sistema

Se considera que una versión del sistema es aceptable para uso alpha cuando:

1. Arranca solo si los tests de arranque pasan.
2. Ejecuta los comandos de sistema de la baseline.
3. Rechaza comandos con imports ilegales.
4. Mantiene el espacio de usuario fuera del versionado de producto.
5. No permite sobrescritura de comandos de sistema por comandos de usuario.
6. Conserva capacidad de actualización controlada.
7. Documenta sus normas en `docs/`.

---

## 13. Glosario mínimo

| Término | Definición |
|---------|------------|
| MOSh | Shell interactivo de MetsuOS |
| Comando de sistema | Módulo oficial en moslib/commands |
| Comando de usuario | Módulo personal user_*.py |
| Espacio personal | rootfs/home/<usuario>/.mos |
| Baseline | Estado de referencia versionado del producto |
| ECSS-light | Conjunto de specs adaptado de ECSS-E-ST-40 |

---

## 14. Autoridad

Este SSS es normativo.

Cualquier cambio en objetivos, no-objetivos o normas no negociables debe versionarse explícitamente en este documento antes o junto con el cambio de código correspondiente.