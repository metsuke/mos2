# 05 – SDD · Arquitectura y diseño

**Versión del documento:** 1.1  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo descriptivo alineado con el código actual  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/02-SRS-Software-Requirements.md, docs/ENVIRONMENTS.md, docs/specs/03-ICD-Interfaces-and-Command-Contract.md, docs/specs/04-SEC-Security-Policy.md

---

## Propósito

Este documento describe la arquitectura y el diseño de MetsuOS tal como existen en la baseline de referencia.

Sirve para:

- entender el sistema sin leer todo el código
- implementar cambios sin romper responsabilidades
- mantener alineados diseño, specs y código

---

## Vista general de arquitectura

MetsuOS se organiza en capas:

1. **Lanzamiento** · scripts anfitrión y punto de entrada
2. **Shell** · interacción con el usuario
3. **Núcleo** · usuario, seguridad, carga de comandos
4. **Comandos** · funciones de sistema y de usuario
5. **Persistencia local de usuario** · espacio `.mos`
6. **Verificación** · tests de arranque y de desarrollo
7. **Documentación** · metodología, entornos, specs, manual y man

Principio rector: el shell coordina; el núcleo decide; los comandos ejecutan acciones concretas bajo contrato y seguridad.

---

## Estructura estática del producto

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Descripción de diseño |
|---------|---------|---------|---------|------------------------|
| moslib/ | | | | Paquete núcleo del producto |
| | core/ | | | Componentes estructurales |
| | | shell.py | | MOSh: bucle interactivo y arranque |
| | | cmd_loader.py | | Resolución, seguridad y carga de comandos |
| | | user.py | | Identidad de usuario y espacio personal |
| | | security.py | | Validación AST de imports |
| | commands/ | | | Comandos oficiales de sistema |
| rootfs/ | | | | Árbol simulado tipo Unix |
| | bin/ | mos.py | | Entrada del sistema |
| | home/ | usuario/.mos/ | | Espacio personal no versionado |
| tests/ | | | | Verificación automatizada |
| docs/ | | | | Metodología, ENVIRONMENTS, specs, manual y man |
| install.sh | | | | Instalación, aliases y Poetry portable |
| mos2.sh | | | | Lanzador principal con Poetry portable |
| pyproject.toml | | | | Dependencias y metadata Poetry |

---

## Responsabilidades por componente

### shell.py · MOSh

Responsabilidades:

- resolver usuario y asegurar espacio personal
- instanciar CommandManager
- ejecutar tests de arranque
- bloquear inicio si los tests fallan
- leer líneas de comando
- invocar comandos resueltos
- manejar exit y errores de interacción

No responsabilidades:

- implementar la lógica de cada comando
- validar AST por sí mismo
- gestionar git update
- resolver el ejecutable de Poetry del anfitrión

### cmd_loader.py · CommandManager

Responsabilidades:

- localizar comandos de sistema y de usuario
- aplicar seguridad antes de cargar
- cargar módulos Python desde archivo
- cachear por mtime para hot-reload
- resolver nombres con la prioridad definida en el ICD

No responsabilidades:

- crear el espacio de usuario
- decidir política de imports
- imprimir el prompt

### security.py

Responsabilidades:

- parsear fuente con AST
- decidir si un import es legal
- devolver lista de errores legibles
- validar archivos de comando

No responsabilidades:

- ejecutar comandos
- conocer el prompt
- gestionar homes de usuario

### user.py

Responsabilidades:

- obtener usuario del anfitrión
- calcular rutas de proyecto, rootfs y home
- migrar home legacy si aplica
- crear estructura `.mos`

No responsabilidades:

- cargar comandos
- validar imports
- ejecutar tests

### commands/*

Responsabilidades:

- implementar una acción concreta
- ofrecer ayuda textual
- respetar política de imports y estilo

No responsabilidades:

- descubrir otros comandos
- administrar el ciclo de vida del shell

### mos2.sh e install.sh

Responsabilidades:

- ubicarse respecto a la raíz del clone (`SCRIPT_DIR`)
- detectar perfil de entorno (unix vs windows/git-bash)
- resolver Poetry de forma portable (`docs/ENVIRONMENTS.md`)
- lanzar MOSh o instalar dependencias con el comando resuelto

No responsabilidades:

- lógica de negocio de comandos
- hardcodear rutas home de un usuario concreto

---

## Diseño de lanzamiento y Poetry

`mos2.sh` e `install.sh` comparten la misma política de resolución:

- **windows/git-bash:** priorizar `poetry.exe`, luego `py -m poetry` / `python -m poetry`; evitar el script `poetry` sin extensión cuando provoca Permission denied
- **linux/native, macos/native, windows/wsl:** priorizar `poetry`, luego `python3 -m poetry` / `python -m poetry`

Tras resolver, todas las invocaciones de ese script usan el mismo comando. Detalle normativo: `docs/ENVIRONMENTS.md`.

---

## Flujo de arranque

1. El usuario lanza `mos2`, `./mos2.sh` o `python rootfs/bin/mos.py`
2. Si usa `mos2.sh`, el script resuelve Poetry y ejecuta `... run python rootfs/bin/mos.py`
3. `mos.py` prepara el path e instancia `MOSh`
4. `MOSh.__init__`: username, espacio `.mos`, `CommandManager`
5. `MOSh.run()` ejecuta tests de arranque
6. Si fallan → mensaje de error y `sys.exit(1)`
7. Si pasan → banner, usuario, espacio personal y bucle REPL

---

## Flujo de ejecución de un comando

1. El usuario escribe una línea
2. El shell separa `cmd_name` y `args`
3. Si `cmd_name == exit` → termina
4. El shell pide el módulo a `CommandManager.get_command(cmd_name)`
5. El loader busca sistema, user_ completo y user_ por nombre corto
6. Antes de cargar, valida seguridad del archivo
7. Si es ilegal → rechazo y no ejecución
8. Si es legal → carga/recarga módulo
9. El shell llama `module.execute(args)`

---

## Diseño de seguridad

### Enfoque

Validación estática por AST, no sandbox completo del intérprete.

### Enforcement runtime

`CommandManager._load_module()` llama a `validate_command_file()` antes de importlib.

### Enforcement de arranque

`MOSh._run_startup_tests()` lanza pytest; el inventario de seguridad debe fallar si hay comandos ilegales de sistema o del usuario actual.

### Ventaja

- no ejecuta el comando para detectar el problema
- errores explícitos
- aplica a sistema y usuario

---

## Diseño del espacio de usuario

### Identidad

El usuario de MetsuOS es el usuario del sistema anfitrión.

### Ruta canónica

```text
rootfs/home/<usuario>/.mos/
```

### Subestructura

| Subdir | Uso de diseño |
|--------|----------------|
| commands/ | extensión personal por comandos |
| data/ | datos persistentes del usuario |
| config/ | configuración personal |
| packages/ | reserva de empaquetado personal |
| repos/ | reserva de repos personales |

### Migración

Si existe home legacy y no la canónica, `user.py` migra el directorio.

---

## Diseño de comandos de sistema de la baseline

| Tipo | Comando | Rol de diseño |
|------|---------|---------------|
| ayuda | help | descubrimiento y ayuda corta |
| ayuda | man | documentación extendida en docs/man |
| calidad | test | batería de tests |
| calidad | update | sincronización controlada con el remoto |
| host | sysinfo | inspección del anfitrión |
| host | uptime | tiempo de actividad del anfitrión |
| host | version | versión e historial git |
| utilidad | clear | higiene de terminal |
| utilidad | echo | salida de texto |

---

## Diseño de hot-reload

CommandManager guarda cache de módulos y mtime del archivo. Si cambió, recarga; si no, reutiliza. La seguridad se reevalúa en la carga.

---

## Diseño de actualización

El comando `update`:

1. detectar working tree sucio
2. crear rama `backup/timestamp` si hay cambios
3. commit de preservación si procede
4. volver a main
5. fetch + reset hard a origin/main
6. podar backups antiguos

Prioriza no perder trabajo local y dejar main idéntico al remoto; no publica backups como release.

---

## Diseño de verificación

### tests/

Validan seguridad, usuario, loader, contrato de comandos, estilo crítico e inventario.

### Arranque bloqueante

La verificación es puerta de entrada a la sesión interactiva.

---

## Diseño documental

| Nivel 1 | Nivel 2 | Papel |
|---------|---------|-------|
| docs/ | METHODOLOGY.md | proceso de evolución |
| docs/ | ENVIRONMENTS.md | perfiles de entorno y Poetry |
| docs/ | STYLE_GUIDE.md | normas de implementación |
| docs/ | specs/ | requisitos y diseño controlados |
| docs/ | USER_MANUAL.md | visión de usuario |
| docs/ | man/ | ayuda extendida por comando |

---

## Decisiones de diseño relevantes

| Decisión | Motivo |
|----------|--------|
| Comandos como archivos .py independientes | máxima modularidad |
| Seguridad por AST | detectar antes de ejecutar |
| Usuario = usuario del anfitrión | simplicidad y realismo alpha |
| rootfs/home para homes | escalabilidad y analogía Unix |
| Tests al arranque | no operar sobre base rota |
| update con backup local | reducir riesgo de pérdida de trabajo |
| docs/man + comando man | ayuda extendida estilo Unix |
| Poetry resuelto en shell scripts | portabilidad git-bash / wsl / native |

---

## Límites actuales de diseño

En esta baseline el diseño no incluye todavía:

1. sistema real de paquetes instalables multi-repo
2. permisos internos ricos multi-usuario MetsuOS
3. IPC entre comandos
4. UI gráfica
5. sandbox OS-level de procesos

Las reservas `packages/` y `repos/` existen para no cerrar esas líneas de evolución.

---

## Guía práctica para modificar el sistema

| Si necesitas... | Toca principalmente... | No olvides... |
|-----------------|------------------------|---------------|
| Cambiar el prompt o el REPL | shell.py | tests de arranque |
| Cambiar resolución de comandos | cmd_loader.py | ICD + tests loader |
| Cambiar política de imports | security.py | SEC + tests security |
| Cambiar homes/migración | user.py | USER reqs + tests user |
| Añadir comando de sistema | moslib/commands/cmd.py | contrato, man, tests, help |
| Añadir comando de usuario | rootfs/home/.../user_*.py | prefijo user_ y seguridad |
| Cambiar resolución de Poetry | mos2.sh / install.sh | ENVIRONMENTS + REQ-PLAT |
| Cambiar normas de producto | docs/specs/ | luego código y tests |

---

## Autoridad

Este SDD describe el diseño de la baseline actual.

Si el código cambia de arquitectura, este documento debe actualizarse en la misma fase o inmediatamente después, antes de considerar el cambio cerrado.