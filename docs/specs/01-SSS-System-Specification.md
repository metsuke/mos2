# 01 – SSS · Especificación de sistema

**Versión del documento:** 1.5  
**Baseline de referencia:** v0.2.7 (árbol hacia v0.2.8)  
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
| Baseline actual | v0.2.7 |
| Árbol hacia | v0.2.8 (tag de producto pendiente de pruebas humanas) |

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
- Apps locales (ámbito usuario o sistema) con mini-moslib de esa app
- Tareas e hilos locales y worker de sesión
- Enrutador de IA (`iarouter`), apagado hasta que el usuario lo active
- Diagnóstico de red del anfitrión (`red`); no es P2P

MetsuOS se ejecuta sobre un sistema operativo anfitrión y no reemplaza su kernel.

---

## Objetivos del sistema
1. Ofrecer un shell modular, extensible y auditable.
2. Permitir comandos de sistema, de app y de usuario con reglas claras.
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
10. Ser la malla P2P ni una tienda remota de apps.

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
- en comandos de app: `minimoslib` de **esa** app, con `app_dir` de esa app

Cualquier otro import está prohibido.

### Protección de comandos de sistema

Un comando de usuario o de app no puede sobrescribir un comando de sistema.

Prioridad de resolución si el nombre coincide: sistema > app de sistema > app de usuario > comando de usuario (`user_`).

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

### iarouter apagado por defecto

El enrutador de IA no envía peticiones hasta `iarouter usar` / `iarouter preguntar` (u operación equivalente ya implementada). Las claves no se listan.

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
| | | shell.py | | Shell MOSh + worker de tareas |
| | | cmd_loader.py | | Carga de comandos, prefijos de app y seguridad en runtime |
| | | user.py | | Usuario y espacio personal |
| | | security.py | | Validación de imports |
| | | apps.py | | Install path/repo, ámbito usuario/sistema |
| | | tasks.py | | Tareas locales + worker |
| | | ia_router.py | | Fachada Jan/GPT4All/Grok/OpenRouter |
| | commands/ | | | Comandos oficiales de sistema |
| rootfs/ | | | | Sistema de archivos simulado |
| | bin/ | | | Punto de entrada |
| | | mos.py | | Lanzador del shell |
| | home/ | | | Homes de usuario |
| | | usuario/ | | Home del usuario anfitrión |
| | | | .mos/ | Espacio privado MetsuOS |
| | opt/ | apps/ | | Apps de ámbito sistema |
| apps/ | | | | Cunas de apps en el clone |
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
| | | | | apps/ | Apps instaladas de ámbito usuario |
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
- resolución de comandos de sistema, de app y de usuario
- salida de errores comprensible
- comando de salida (`exit`)

### Comandos de sistema

Como mínimo en esta baseline (tabla por tipo A–Z y comando A–Z dentro del tipo):

| Tipo | Comando | Función general |
|------|---------|-----------------|
| accesibilidad | a11y | Validación A11Y e informe automático |
| apps | apps | Instalar, listar, ver y quitar apps |
| ayuda | docs | Listar y mostrar docs/ y ficheros públicos de la raíz |
| ayuda | help | Ayuda de comandos |
| ayuda | man | Manual extendido desde docs/man/ y man de app |
| calidad | synccheck | Comparar HEAD local con origin/main |
| calidad | test | Ejecución de la batería de tests |
| calidad | update | Actualización desde origin/main con backup local y tags |
| host | sysinfo | Información del anfitrión |
| host | uptime | Tiempo de actividad del anfitrión |
| host | version | Versión e historial |
| ia | iarouter | Detectar, elegir proveedor, preguntar (off por defecto) |
| red | red | Diagnóstico de red del anfitrión (no es P2P) |
| sesion | exit | Salida del shell (builtin) |
| tareas | hilos | Vista de tareas por clase |
| tareas | tareas | GTD local |
| utilidad | clear | Limpieza de pantalla |
| utilidad | echo | Eco de texto |

Tras `update`, los módulos ya cargados en la sesión no cambian solos. El sistema debe ofrecer `update reiniciar` o exigir salir y volver a entrar.

### Comandos de usuario

- archivo con prefijo `user_`
- invocación con prefijo completo siempre
- invocación sin prefijo solo si no hay conflicto con un comando de sistema ni de app con más prioridad

### Comandos de app

- viven en el paquete de la app (`commands/`), no como `user_*.py`
- invocables como nombre corto, `id_cmd` o `app_id_cmd` según ICD y spec 08
- misma puerta SEC/A11Y que el núcleo

### Seguridad

El sistema debe validar comandos:

- en tiempo de carga/ejecución
- en arranque, sobre comandos de sistema y del usuario actual
- sobre comandos de apps instaladas, con mini-moslib solo de esa app

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

### Apps, tareas e IA

Normativo en detalle: `docs/specs/08-APPS.md`, `09-TASKS.md`, `10-IA-ROUTER.md`.

En el árbol 0.2.7 / hacia 0.2.8 el sistema ya:

- descubre e instala apps desde una ruta del clone o un repo git, ámbito usuario o sistema;
- carga comandos de app con la misma puerta SEC/A11Y; sin A11Y no se acepta ni se ejecuta;
- mantiene tareas manuales y automáticas locales y un worker durante la sesión MOSh;
- expone iarouter (Jan, GPT4All, Grok, OpenRouter), off por defecto, con almacén de claves en `.mos` y sin listar secretos.

Malla P2P, suite de desarrollo completa y DepManager geo no entran en esta baseline.

---

## Restricciones de diseño de sistema
1. No introducir gestores de paquetes Python genéricos dentro del modelo de comandos.
2. No permitir que el usuario reemplace el núcleo modificando solo su espacio personal.
3. No acoplar el núcleo a una única distribución Linux.
4. No depender de servicios de red para el arranque básico (synccheck, update, iarouter remoto y `red` sí usan red cuando se invocan).
5. No debilitar los tests de arranque para facilitar un cambio puntual.
6. No documentar en el repo público rutas absolutas personales ni inventarios de máquinas privadas.
7. No excluir un perfil A11Y declarado por comodidad de implementación.
8. No invocar APIs exclusivas de un forge; solo Git.
9. No tratar el puente HTTP de iarouter como P2P.

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
Control: comandos del sistema, de app y de usuario

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

### Interfaz producto-apps

El núcleo instala y carga apps desde path o repo git; SEC limita mini-moslib al `app_dir` de esa app.

### Interfaz producto-IA

La fachada `moslib.core.ia_router` está off hasta activación explícita. No sustituye al shell.

---

## Criterios de aceptación de sistema
Se considera que una versión del sistema es aceptable para uso alpha cuando:

1. Arranca solo si los tests de arranque pasan.
2. Ejecuta los comandos de sistema de la baseline, incluidos `a11y`, `docs`, `synccheck`, `apps`, `tareas`, `hilos`, `iarouter` y `red`.
3. Rechaza comandos con imports ilegales.
4. Mantiene el espacio de usuario fuera del versionado de producto.
5. No permite sobrescritura de comandos de sistema por comandos de usuario ni de app.
6. Conserva capacidad de actualización controlada y alineación de tags.
7. Documenta sus normas en `docs/`.
8. Puede instalarse y lanzarse en los perfiles de entorno declarados.
9. Publica declaración de accesibilidad y política A11Y.
10. No usa el color como única señal en los mensajes de sistema revisados en esta campaña.
11. iarouter no envía por defecto.

---

## Glosario mínimo
| Término | Definición |
|---------|------------|
| MOSh | Shell interactivo de MetsuOS |
| Comando de sistema | Módulo oficial en moslib/commands |
| Comando de app | Módulo en commands/ de una app instalada |
| Comando de usuario | Módulo personal user_*.py |
| Espacio personal | rootfs/home/usuario/.mos |
| Baseline | Estado de referencia versionado del producto |
| ECSS-light | Conjunto de specs adaptado de ECSS-E-ST-40 |
| Perfil de entorno | Par sistema/entorno (p. ej. windows/git-bash) |
| Declaración de accesibilidad | Texto público al modelo UE/ES adaptado a CLI |
| Informe A11Y | docs/a11y/informe.md e informe.json |
| synccheck | Comando que compara HEAD local con origin/main |
| mini-moslib | Biblioteca mínima de una app, solo para esa app |
| iarouter | Comando y fachada de modelos locales o remotos |

---

## Evolución respecto a SSS 1.3
La v1.3 reservaba apps, tareas e iarouter como «campaña 07 / hueco 0.2.5». Esa reserva se conserva como historia: el código ya está en el árbol 0.2.7. Esta v1.4 no borra el SSS 1.3; declara esas capacidades como producto presente y añade `red` y `update reiniciar`.

---

## Autoridad
Este SSS es normativo.

Cualquier cambio en objetivos, no-objetivos o normas no negociables debe versionarse explícitamente en este documento antes o junto con el cambio de código correspondiente.