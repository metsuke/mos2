# 01 – SSS · Especificación de sistema

**Versión del documento:** 1.3  
**Baseline de referencia:** v0.2.5  
**Estado:** Normativo  
**Documentos relacionados:** docs/METHODOLOGY.md, docs/ENVIRONMENTS.md, docs/A11Y.md, docs/a11y/DECLARACION.md, docs/specs/00-OVERVIEW.md, docs/specs/04-SEC-Security-Policy.md, docs/specs/08-APPS.md, docs/specs/09-TASKS.md, docs/specs/10-IA-ROUTER.md

---

## Propósito

Este documento define qué es MetsuOS a nivel de sistema, sus objetivos, no-objetivos y normas no negociables.

Todo diseño, requisito software e implementación debe ser compatible con esta especificación.

---

## Identificación del sistema

| Campo | Valor |
|-------|-------|
| Nombre | MetsuOS |
| Nombre alternativo | MOS2 |
| Tipo | Sistema operativo simulado y modular |
| Shell | MOSh |
| Lenguaje principal | Python 3.10+ |
| Licencia | GPL-3.0 |
| Estado | Alpha |
| Baseline actual | v0.2.5 |

---

## Definición del sistema

MetsuOS es un entorno operativo simulado que proporciona:

- Un shell interactivo propio (MOSh)
- Un núcleo modular (`moslib`)
- Un sistema de archivos simulado inspirado en Linux (`rootfs`)
- Un espacio personal por usuario del sistema anfitrión
- Comandos implementados como módulos Python independientes
- Validación de seguridad de imports
- Tests de arranque obligatorios
- Política y declaración de accesibilidad (CLI)
- Consulta de documentación (`docs`) y validación A11Y (`a11y`)
- Comprobación de sincronía del clone con origin/main (`synccheck`)

MetsuOS se ejecuta sobre un sistema operativo anfitrión y no reemplaza su kernel.

---

## Objetivos del sistema

1. Ofrecer un shell modular, extensible y auditable.
2. Permitir comandos de sistema y de usuario con reglas claras.
3. Garantizar aislamiento del espacio personal del usuario.
4. Impedir que comandos carguen código fuera de la política de seguridad.
5. Ser agnóstico de plataforma en los entornos soportados.
6. Evolucionar sin romper funcionalidad existente mediante specs, tests y proceso controlado.
7. No excluir los perfiles de discapacidad declarados en `docs/A11Y.md`.

---

## No-objetivos

MetsuOS, en esta baseline, **no** pretende:

1. Ser un kernel real.
2. Virtualizar hardware completo.
3. Sustituir el sistema de usuarios del sistema anfitrión.
4. Permitir instalación arbitraria de paquetes Python dentro de comandos.
5. Ofrecer compatibilidad POSIX completa.
6. Multiplexar procesos reales como un sistema operativo nativo.
7. Garantizar seguridad frente a un atacante con acceso de escritura al código del núcleo fuera de las validaciones definidas.
8. Ser un sitio web o app del sector público ni declarar conformidad legal con el RD 1112/2018.
9. Ofrecer GUI, laboratorio de lectores de pantalla o certificación WCAG de página web en esta baseline.

---

## Normas no negociables

Las siguientes normas son férreas. No se pueden debilitar por comodidad.

### Accesibilidad

La accesibilidad de la interfaz (MOSh, launchers y documentación consultable) es mandatoria.

Si accesibilidad y seguridad chocan, prevalece no excluir un perfil soportado. El recorte de SEC no es silencioso: se documenta en SEC + A11Y + SRelD.

Referentes: `docs/A11Y.md`, `docs/a11y/DECLARACION.md`, informe en `docs/a11y/informe.md`.

Perfiles mínimos soportados: solo teclado, lector de pantalla de terminal, baja visión, daltonismo, carga cognitiva, sordera/sin audio (N/A de sonido).

### Todo pasa por mosLib

La lógica de sistema y la extensión controlada del entorno se canalizan a través de `moslib`.

### Política de imports

Los comandos solo pueden importar:

- biblioteca estándar de Python
- `moslib` y sus submódulos

Cualquier otro import está prohibido.

### Protección de comandos de sistema

Un comando de usuario no puede sobrescribir un comando de sistema.

### Contrato de comando

Todo comando debe exponer:

- `execute(args)`
- `help()` que devuelve `str`

### Espacio de usuario aislado

El espacio personal del usuario vive fuera del árbol versionado de producto y no se publica en el repositorio principal.

### Tests de arranque

Si la batería de tests de arranque falla, el sistema no debe iniciar sesión interactiva.

### Agnosticismo de plataforma

El sistema debe poder instalarse y ejecutarse en los perfiles:

| Sistema | Entorno |
|---------|----------|
| linux | native |
| macos | native |
| windows | git-bash |
| windows | wsl |

Sin asumir una única plataforma. La política operativa de Poetry, rutas relativas al clone y contexto de sesión genérico está en `docs/ENVIRONMENTS.md`. El lanzador (`mos2.sh`) y el instalador (`install.sh`) deben resolver Poetry de forma portable según el perfil. Un candidato Poetry solo se usa si `--version` se puede ejecutar.

---

## Contexto operativo

### Sistema anfitrión

MetsuOS usa el usuario real del sistema anfitrión para:

- personalizar el prompt
- resolver el directorio home simulado del usuario
- aislar datos y comandos personales

### Estructura lógica del sistema

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
| | | usuario/ | | Home del usuario anfitrión |
| | | | .mos/ | Espacio privado MetsuOS |
| tests/ | | | | Batería de tests |
| docs/ | | | | Metodología, specs, manual, entornos, A11Y y man |
| | a11y/ | | | Declaración e informe de accesibilidad |
| mos2.sh | | | | Lanzador con resolución portable de Poetry |
| install.sh | | | | Instalador con la misma política |

### Espacio personal del usuario

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 | Descripción |
|---------|---------|---------|---------|---------|-------------|
| rootfs/ | home/ | usuario/ | .mos/ | | Raíz privada del usuario |
| | | | | commands/ | Comandos personales user_*.py |
| | | | | data/ | Datos del usuario |
| | | | | config/ | Configuración del usuario |
| | | | | packages/ | Metadatos de paquetes de usuario |
| | | | | repos/ | Repositorios personales |

El contenido de `rootfs/home/` no se versiona como producto. No se documentan rutas home absolutas de usuarios concretos.

---

## Capacidades de sistema requeridas

### Shell interactivo

El sistema debe proporcionar un shell con:

- prompt identificable
- lectura de comandos
- resolución de comandos de sistema y de usuario
- salida de errores comprensible
- comando de salida (`exit`)

### Comandos de sistema

Como mínimo en esta baseline (tabla por tipo A–Z y comando A–Z dentro del tipo):

| Tipo | Comando | Función general |
|------|---------|-----------------|
| accesibilidad | a11y | Validación A11Y e informe automático |
| ayuda | docs | Listar y mostrar docs/ y ficheros públicos de la raíz |
| ayuda | help | Ayuda de comandos |
| ayuda | man | Manual extendido desde docs/man/ |
| calidad | synccheck | Comparar HEAD local con origin/main |
| calidad | test | Ejecución de la batería de tests |
| calidad | update | Actualización desde origin/main con backup local y tags |
| host | sysinfo | Información del anfitrión |
| host | uptime | Tiempo de actividad del anfitrión |
| host | version | Versión e historial |
| sesion | exit | Salida del shell (builtin) |
| utilidad | clear | Limpieza de pantalla |
| utilidad | echo | Eco de texto |

### Comandos de usuario

- archivo con prefijo `user_`
- invocación con prefijo completo siempre
- invocación sin prefijo solo si no hay conflicto con un comando de sistema

### Seguridad

El sistema debe validar comandos:

- en tiempo de carga/ejecución
- en arranque, sobre comandos de sistema y del usuario actual

### Actualización

El sistema debe poder sincronizarse con el repositorio remoto de forma controlada, preservando trabajo local en ramas de backup cuando existan cambios pendientes, y alineando tags locales con origin.

### Documentación

El sistema debe disponer de:

- metodología de desarrollo
- especificaciones
- guía de estilo
- manual de usuario
- política de entornos (`docs/ENVIRONMENTS.md`)
- política y declaración de accesibilidad
- informe automático de accesibilidad
- páginas man por comando
- comando `man` para consultar man
- comando `docs` para listar y leer `docs/` y README, CHANGELOG, AGENTS, LICENSE
- comando `synccheck` para auditar la sincronía Git

### Accesibilidad

El sistema debe:

- publicar declaración al modelo europeo/español adaptado a CLI
- poder ejecutar solo la validación A11Y
- regenerar el informe al ejecutar esa validación o la batería que incluya tests A11Y
- no usar el color como única señal
- ofrecer help/man y mensajes con pista de acción

---

## Restricciones de diseño de sistema

1. No introducir gestores de paquetes Python genéricos dentro del modelo de comandos.
2. No permitir que el usuario reemplace el núcleo modificando solo su espacio personal.
3. No acoplar el núcleo a una única distribución Linux.
4. No depender de servicios de red para el arranque básico (synccheck y update sí usan red cuando se invocan).
5. No debilitar los tests de arranque para facilitar un cambio puntual.
6. No documentar en el repo público rutas absolutas personales ni inventarios de máquinas privadas.
7. No excluir un perfil A11Y declarado por comodidad de implementación.
8. No invocar APIs exclusivas de un forge; solo Git.

---

## Requisitos de calidad de sistema

### Modularidad

Los comandos deben poder añadirse como archivos independientes sin reescribir el shell.

### Auditabilidad

Las reglas críticas de seguridad y de accesibilidad deben estar centralizadas y ser verificables por tests.

### Robustez de evolución

Los cambios se introducen por fases, con commits atómicos, ramas feature y verificación previa a merge.

### Claridad de uso

Los mensajes orientados a usuario final deben estar en español y ser accionables.

### Accesibilidad de interfaz

La salida debe ser texto lineal usable con teclado y con lector de terminal, sin significado solo-color.

---

## Interfaces de sistema de alto nivel

### Interfaz humano-shell

Entrada: línea de texto  
Salida: texto en terminal  
Control: comandos del sistema y de usuario

### Interfaz núcleo-comandos

El núcleo carga módulos de comando desde directorios conocidos y les exige el contrato `execute` / `help`.

### Interfaz núcleo-seguridad

Ningún comando se ejecuta si incumple la política de imports.

### Interfaz núcleo-usuario

El núcleo resuelve el usuario anfitrión y asegura su espacio `.mos`.

### Interfaz producto-repositorio

El producto puede actualizarse desde `origin/main` y comparar HEAD con origin/main (`update`, `synccheck`).

### Interfaz producto-entorno anfitrión

El lanzador y el instalador resuelven Poetry según el perfil de entorno, sin hardcodear rutas de usuario.

### Interfaz producto-documentación

El sistema debe poder listar y mostrar ficheros de `docs/` y de la lista blanca de la raíz sin salir a un navegador.

### Interfaz producto-accesibilidad

El sistema debe poder emitir una situación de cumplimiento a partir de tests y dejarla en `docs/a11y/informe.md` e `informe.json`.

---

## Criterios de aceptación de sistema

Se considera que una versión del sistema es aceptable para uso alpha cuando:

1. Arranca solo si los tests de arranque pasan.
2. Ejecuta los comandos de sistema de la baseline, incluidos `a11y`, `docs` y `synccheck`.
3. Rechaza comandos con imports ilegales.
4. Mantiene el espacio de usuario fuera del versionado de producto.
5. No permite sobrescritura de comandos de sistema por comandos de usuario.
6. Conserva capacidad de actualización controlada y alineación de tags.
7. Documenta sus normas en `docs/`.
8. Puede instalarse y lanzarse en los perfiles de entorno declarados.
9. Publica declaración de accesibilidad y política A11Y.
10. No usa el color como única señal en los mensajes de sistema revisados en esta campaña.

---

## Glosario mínimo

| Término | Definición |
|---------|------------|
| MOSh | Shell interactivo de MetsuOS |
| Comando de sistema | Módulo oficial en moslib/commands |
| Comando de usuario | Módulo personal user_*.py |
| Espacio personal | rootfs/home/usuario/.mos |
| Baseline | Estado de referencia versionado del producto |
| ECSS-light | Conjunto de specs adaptado de ECSS-E-ST-40 |
| Perfil de entorno | Par sistema/entorno (p. ej. windows/git-bash) |
| Declaración de accesibilidad | Texto público al modelo UE/ES adaptado a CLI |
| Informe A11Y | docs/a11y/informe.md e informe.json |
| synccheck | Comando que compara HEAD local con origin/main |

---

## Capacidades en curso (campaña 07)

Normativo en detalle: `docs/specs/08-APPS.md`, `09-TASKS.md`, `10-IA-ROUTER.md`.

El sistema, al cerrar la 07, debe poder:

- Descubrir e instalar apps locales (no son comandos sueltos en moslib/commands).
- Cargar comandos de app con la misma puerta SEC/A11Y que el núcleo. Sin A11Y no se acepta ni se ejecuta.
- Mantener tareas manuales (comandos) y automáticas locales (vista de hilos en texto lineal).
- Exponer una fachada de IA en moslib, off por defecto, sin leer `.mos` salvo allowlist.

No son capacidades de esta baseline 0.2.5 hasta que el código de 7.1–7.3 exista. Este apartado reserva el hueco para no romper el SSS al implementar.

Malla P2P, suite de desarrollo completa y DepManager geo no entran en este apartado.

---

## Autoridad

Este SSS es normativo.

Cualquier cambio en objetivos, no-objetivos o normas no negociables debe versionarse explícitamente en este documento antes o junto con el cambio de código correspondiente.