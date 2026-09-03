# MetsuOS (MOS2)

Sistema Operativo simulado y modular basado en Python

**Estado:** Alpha (funcional y en desarrollo activo)  
**Versión:** 0.2.6  
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
- **Accesibilidad mandatoria** de la interfaz CLI (`docs/A11Y.md` y declaración en `docs/a11y/`)
- Apps locales (instalar/quitar en `.mos/apps`) con la misma puerta SEC/A11Y
- Tareas locales (manuales y automáticas) y vista de hilos
- Fachada de enrutador de IA (off por defecto)
- Tests unitarios y de seguridad con pytest
- Gestión de dependencias y entorno virtual con Poetry
- Scripts de instalación y lanzamiento multiplataforma (linux/native, macos/native, windows/git-bash, windows/wsl)

---

## Estructura del proyecto

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Descripción |
|---------|---------|---------|---------|-------------|
| moslib/ | | | | Núcleo del sistema |
| | core/ | | | Componentes principales |
| | | shell.py | | Shell principal (MOSh) |
| | | cmd_loader.py | | Cargador dinámico de comandos + seguridad |
| | | user.py | | Usuario anfitrión + espacio personal + migración |
| | | security.py | | Validación de imports (AST) |
| | | apps.py | | Apps locales install/list/remove |
| | | tasks.py | | Tareas GTD locales |
| | | ia_router.py | | Fachada de modelos (off por defecto) |
| | commands/ | | | Comandos oficiales del sistema |
| | | a11y.py | | Validación A11Y e informe |
| | | apps.py | | Gestión de apps locales |
| | | clear.py | | Limpia la pantalla |
| | | docs.py | | Consulta documentación del clone |
| | | echo.py | | Imprime texto |
| | | help.py | | Sistema de ayuda |
| | | hilos.py | | Vista de tareas por clase |
| | | iarouter.py | | Estado del enrutador de IA |
| | | man.py | | Manual extendido (docs/man/) |
| | | synccheck.py | | Compara HEAD local con origin/main |
| | | sysinfo.py | | Información del sistema |
| | | tareas.py | | Lista y gestiona tareas |
| | | test.py | | Ejecuta la batería de tests |
| | | update.py | | Actualiza desde origin/main |
| | | uptime.py | | Tiempo de actividad |
| | | version.py | | Versión e historial |
| rootfs/ | | | | Sistema de archivos simulado |
| | bin/ | | | Ejecutables del sistema |
| | | mos.py | | Punto de entrada del sistema |
| | home/ | | | Carpetas personales de los usuarios |
| | | usuario/ | | Carpeta del usuario del sistema anfitrión |
| | | | .mos/ | Espacio privado (commands, apps, data, config) |
| docs/ | | | | Documentación del proyecto |
| | A11Y.md | | | Política de accesibilidad |
| | a11y/ | | | Declaración e informe A11Y |
| | AI_ONBOARDING.md | | | Arranque para agentes IA |
| | HUMAN_ONBOARDING.md | | | Arranque para humanos |
| | INCENTIVOS.md | | | Dirección de trabajo (vectores y roles) |
| | INTERACTION_REVIEW.md | | | Cierre de interacción y deuda |
| | DEVELOPER_GUIDE.md | | | Flujo de desarrollo |
| | VERSIONING.md | | | Versiones, tags y Poetry |
| | ENVIRONMENTS.md | | | Perfiles de entorno y Poetry |
| | METHODOLOGY.md | | | Método de trabajo |
| | STYLE_GUIDE.md | | | Normas de código |
| | USER_MANUAL.md | | | Manual de usuario |
| | DEUDA_Y_CAMPANAS.md | | | Deuda y campañas previstas |
| | plans/ | | | Planes de campaña |
| | specs/ | | | Especificaciones ECSS-light |
| | man/ | | | Páginas man por comando |
| tests/ | | | | Tests unitarios, seguridad y estilo |
| | conftest.py | | | Configuración compartida de pytest |
| | test_apps.py | | | Apps locales |
| | test_tasks.py | | | Tareas |
| | test_ia_router.py | | | Enrutador IA |
| | test_security.py | | | Validación de imports |
| | test_user.py | | | Módulo de usuario |
| | test_cmd_loader.py | | | Cargador de comandos |
| | test_version_metadata.py | | | Formato SemVer de Poetry |
| AGENTS.md | | | | Entrada corta para agentes IA |
| CHANGELOG.md | | | | Historial de cambios por release |
| install.sh | | | | Instalación y aliases |
| mos2.sh | | | | Lanzador principal (Poetry portable) |
| pyproject.toml | | | | Configuración de Poetry |
| poetry.lock | | | | Lock de dependencias |

> **Nota:** El contenido de `rootfs/home/` no se versiona (`.gitignore`). Las rutas de usuario son siempre relativas al clone.

---

## Requisitos

- Python 3.10 o superior
- Poetry instalado

---

## Instalación

```text
git clone https://github.com/metsuke/mos2.git
cd mos2
chmod +x install.sh
./install.sh
```

El script `install.sh`:

- Configura Poetry para usar un entorno virtual local (`.venv`)
- Instala las dependencias
- Ofrece instalar aliases útiles (`mos2`, `mos2f`, `mos2u`, etc.)
- Resuelve Poetry según el perfil de entorno

### Aliases disponibles (opcionales)

| Alias | Descripción |
|-------|-------------|
| mos2 | Lanza MetsuOS |
| mos2f | Cambia al directorio raíz del proyecto |
| mos2u | Ejecuta de nuevo el instalador |

---

## Uso

```text
./mos2.sh
```

o, si tienes el alias:

```text
mos2
```

Se abrirá el shell:

```text
Iniciando MOSh para MetsuOS...
Usuario: tu_usuario_real
Espacio personal: .../rootfs/home/tu_usuario_real/.mos
Usa 'exit' para salir, 'help' para ayuda

mosh/tu_usuario_real@metsuos:~$
```

---

## Comandos del sistema

| Tipo | Comando | Descripción |
|------|---------|-------------|
| accesibilidad | a11y | Validación A11Y e informe |
| apps | apps | Apps locales: list/show/install/remove |
| ayuda | docs | Lista y muestra documentación |
| ayuda | help | Lista o ayuda de un comando |
| ayuda | man | Manual extendido (docs/man/) |
| calidad | synccheck | Compara HEAD local con origin/main |
| calidad | test | Batería de tests |
| calidad | update | Sincroniza origin/main |
| host | sysinfo | Hardware y estado del anfitrión |
| host | uptime | Tiempo de actividad del anfitrión |
| host | version | Versión e historial |
| ia | iarouter | Estado del enrutador de modelos (off por defecto) |
| sesion | exit | Sale del shell |
| tareas | hilos | Vista por clase de las tareas |
| tareas | tareas | Lista, alta, hecha, tick |
| utilidad | clear | Limpia la pantalla |
| utilidad | echo | Imprime texto |

---

## Cómo añadir comandos

### Comandos del sistema (oficiales)

Crea un archivo en `moslib/commands/` (ejemplo `hola.py`):

```text
def execute(args):
    print("¡Hola desde MetsuOS!")

def help():
    return "Uso: hola - Saluda al usuario"
```

### Comandos de usuario (personales)

1. El sistema crea automáticamente `rootfs/home/<tu_usuario>/.mos/commands/`
2. Crea un archivo cuyo nombre **debe** empezar por `user_`

```text
def execute(args):
    print("¡Hola desde mi espacio personal!")

def help():
    return "Uso: user_hola - Saluda desde el espacio de usuario"
```

#### Reglas de invocación de comandos de usuario

- Siempre se puede invocar con el nombre completo: `user_hola`
- También se puede invocar sin el prefijo (`hola`) solo si no existe un comando del sistema con ese mismo nombre
- El usuario nunca puede sobrescribir un comando del sistema

#### Regla de seguridad obligatoria

Todo comando (sistema, usuario o de app) solo puede importar:

- módulos de la biblioteca estándar de Python
- módulos de `moslib` (y submódulos)

Cualquier otro import hace que el comando sea rechazado. Sin A11Y mínima no se acepta ni se ejecuta.

---

## Tests

Los scripts `./install.sh` y `./mos2.sh` resuelven Poetry según el perfil de entorno.  
Ver `docs/ENVIRONMENTS.md`.

Desde la raíz del clone:

```text
./mos2.sh
```

Dentro del shell:

```text
test
```

Si Poetry ya funciona en tu PATH:

```text
poetry run pytest
```

---

## Accesibilidad

Política: `docs/A11Y.md`  
Declaración: `docs/a11y/DECLARACION.md`  
Informe automático: `docs/a11y/informe.md`

A11Y es mandatoria para humano e IA. No es un incentivo opcional.

---

## Desarrollo

Activar entorno:

```text
poetry shell
```

Ejecutar el sistema (alternativa recomendada: `./mos2.sh`):

```text
poetry run python rootfs/bin/mos.py
```

La lógica de negocio está en `moslib/`.  
Guía: `docs/DEVELOPER_GUIDE.md`.  
Historial: `CHANGELOG.md`.  
Planes: `docs/plans/`.  
Dirección: `docs/INCENTIVOS.md`.

---

## Documentación

| Documento | Contenido |
|-----------|-----------|
| AGENTS.md | Entrada corta para agentes IA |
| CHANGELOG.md | Historial de cambios por release |
| docs/A11Y.md | Política de accesibilidad |
| docs/a11y/DECLARACION.md | Declaración de accesibilidad |
| docs/AI_ONBOARDING.md | Protocolo completo para IA |
| docs/HUMAN_ONBOARDING.md | Arranque para personas |
| docs/INCENTIVOS.md | Vectores y actuaciones por rol |
| docs/INTERACTION_REVIEW.md | Cierre de interacción y deuda |
| docs/DEUDA_Y_CAMPANAS.md | Deuda y campañas previstas |
| docs/DEVELOPER_GUIDE.md | Flujo de desarrollo |
| docs/VERSIONING.md | Versiones, tags y Poetry |
| docs/USER_MANUAL.md | Manual de usuario formal |
| docs/ENVIRONMENTS.md | Perfiles de entorno, Poetry y contexto de sesión |
| docs/METHODOLOGY.md | Método de trabajo |
| docs/STYLE_GUIDE.md | Normas de estilo de código |
| docs/plans/ | Planes de campaña |
| docs/specs/ | Especificaciones ECSS-light |
| docs/man/ | Páginas man por comando |

Estudiar el repo desde cero (IA): `AGENTS.md` → `docs/AI_ONBOARDING.md` → `docs/INCENTIVOS.md`.  
Estudiar el repo (humano): `docs/HUMAN_ONBOARDING.md`.

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
> Aunque ya es funcional como shell con espacio de usuario, seguridad de imports, apps locales y tareas, todavía no pretende ser un sistema operativo completo.