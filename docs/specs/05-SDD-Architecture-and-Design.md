# 05 – SDD · Arquitectura y diseño

**Versión del documento:** 1.0  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo descriptivo alineado con el código actual  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/02-SRS-Software-Requirements.md, docs/specs/03-ICD-Interfaces-and-Command-Contract.md, docs/specs/04-SEC-Security-Policy.md

---

## 1. Propósito

Este documento describe la arquitectura y el diseño de MetsuOS tal como existen en la baseline de referencia.

Sirve para:

- entender el sistema sin leer todo el código
- implementar cambios sin romper responsabilidades
- mantener alineados diseño, specs y código

---

## 2. Vista general de arquitectura

MetsuOS se organiza en capas:

1. **Lanzamiento** · scripts y punto de entrada
2. **Shell** · interacción con el usuario
3. **Núcleo** · usuario, seguridad, carga de comandos
4. **Comandos** · funciones de sistema y de usuario
5. **Persistencia local de usuario** · espacio `.mos`
6. **Verificación** · tests de arranque y de desarrollo
7. **Documentación** · metodología, specs, manual y man

Principio rector: el shell coordina; el núcleo decide; los comandos ejecutan acciones concretas bajo contrato y seguridad.

---

## 3. Estructura estática del producto

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
| | home/ | `<usuario>/.mos/` | | Espacio personal no versionado |
| tests/ | | | | Verificación automatizada |
| docs/ | | | | Metodología, specs, manual y man |
| install.sh | | | | Instalación y aliases en anfitrión |
| mos2.sh | | | | Lanzador principal |
| pyproject.toml | | | | Dependencias y metadata Poetry |

---

## 4. Responsabilidades por componente

### 4.1 shell.py · MOSh

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

### 4.2 cmd_loader.py · CommandManager

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

### 4.3 security.py

Responsabilidades:

- parsear fuente con AST
- decidir si un import es legal
- devolver lista de errores legibles
- validar archivos de comando

No responsabilidades:

- ejecutar comandos
- conocer el prompt
- gestionar homes de usuario

### 4.4 user.py

Responsabilidades:

- obtener usuario del anfitrión
- calcular rutas de proyecto, rootfs y home
- migrar home legacy si aplica
- crear estructura `.mos`

No responsabilidades:

- cargar comandos
- validar imports
- ejecutar tests

### 4.5 commands/*

Responsabilidades:

- implementar una acción concreta
- ofrecer ayuda textual
- respetar política de imports y estilo

No responsabilidades:

- descubrir otros comandos
- administrar el ciclo de vida del shell

---

## 5. Flujo de arranque

1. El usuario lanza `mos2`, `./mos2.sh` o `python rootfs/bin/mos.py`
2. `mos.py` prepara el path e instancia `MOSh`
3. `MOSh.__init__`:
   - obtiene username
   - asegura espacio `.mos`
   - crea `CommandManager` con dirs de sistema y usuario
4. `MOSh.run()` ejecuta tests de arranque
5. Si fallan → mensaje de error y `sys.exit(1)`
6. Si pasan → muestra banner, usuario, espacio personal y entra en bucle REPL

---

## 6. Flujo de ejecución de un comando

1. El usuario escribe una línea
2. El shell separa `cmd_name` y `args`
3. Si `cmd_name == exit` → termina
4. El shell pide el módulo a `CommandManager.get_command(cmd_name)`
5. El loader busca:
   - sistema
   - user_ completo
   - user_ por nombre corto
6. Antes de cargar, valida seguridad del archivo
7. Si es ilegal → rechazo y no ejecución
8. Si es legal → carga/recarga módulo
9. El shell llama `module.execute(args)`

---

## 7. Diseño de seguridad

### 7.1 Enfoque

La seguridad de extensión se implementa por validación estática, no por sandbox completo del intérprete.

### 7.2 Punto de enforcement runtime

`CommandManager._load_module()` llama a `validate_command_file()` antes de ejecutar el loader de importlib.

### 7.3 Punto de enforcement de arranque

`MOSh._run_startup_tests()` lanza pytest. Los tests de inventario de seguridad deben fallar si existe cualquier comando ilegal de sistema o del usuario actual.

### 7.4 Ventaja de diseño

- no ejecuta el comando para detectar el problema
- produce errores explícitos
- se aplica por igual a sistema y usuario

---

## 8. Diseño del espacio de usuario

### 8.1 Identidad

El usuario de MetsuOS es el usuario del sistema anfitrión.

### 8.2 Ruta canónica

rootfs/home/<usuario>/.mos/

### 8.3 Subestructura

| Subdir | Uso de diseño |
|--------|----------------|
| commands/ | extensión personal por comandos |
| data/ | datos persistentes del usuario |
| config/ | configuración personal |
| packages/ | reserva para metadatos de empaquetado personal |
| repos/ | reserva para repos personales |

### 8.4 Migración

Si existe una ruta legacy de home de usuario y no existe la canónica, `user.py` migra el directorio para no romper instalaciones alpha previas.

---

## 9. Diseño de comandos de sistema de la baseline

| Comando | Rol de diseño |
|---------|---------------|
| help | descubrimiento y ayuda corta |
| version | identidad de versión e historial git |
| sysinfo | inspección del anfitrión |
| uptime | tiempo de actividad del anfitrión |
| echo | utilidad básica de salida |
| clear | higiene de terminal |
| test | acceso explícito a la batería de tests |
| update | sincronización controlada con el repositorio remoto |
| man | consulta de documentación extendida en docs/man |

Nota de diseño: `man` forma parte de la evolución documental/funcional iniciada sobre v0.2.1 y debe implementarse conforme al ICD y al SRS.

---

## 10. Diseño de hot-reload

CommandManager guarda:

- cache de módulos
- mtime del archivo fuente

Si el archivo cambió, se recarga.  
Si no cambió, se reutiliza el módulo cacheado.

La seguridad se reevalúa en el camino de carga según el diseño actual del loader.

---

## 11. Diseño de actualización

El comando `update` encapsula una política operativa:

1. detectar working tree sucio
2. crear rama `backup/timestamp` si hay cambios
3. commit de preservación en esa rama si procede
4. volver a main
5. fetch + reset hard a origin/main
6. podar backups antiguos

Diseño intencional:

- prioriza no perder trabajo local
- prioriza que main quede idéntico al remoto
- no publica backups como release

---

## 12. Diseño de verificación

### 12.1 tests/

Los tests validan:

- seguridad
- usuario
- loader
- contrato de comandos
- estilo crítico
- inventario de comandos

### 12.2 Arranque bloqueante

La verificación no es solo de desarrollo: es puerta de entrada a la sesión interactiva.

Esto convierte la calidad en propiedad de runtime del sistema.

---

## 13. Diseño documental

| Nivel 1 | Nivel 2 | Papel en la arquitectura de información |
|---------|---------|------------------------------------------|
| docs/ | METHODOLOGY.md | proceso de evolución |
| docs/ | STYLE_GUIDE.md | normas de implementación |
| docs/ | specs/ | requisitos y diseño controlados |
| docs/ | USER_MANUAL.md | visión de usuario |
| docs/ | man/ | ayuda extendida por comando |

La documentación no es accesoria: forma parte del sistema de control de cambios.

---

## 14. Decisiones de diseño relevantes

| Decisión | Motivo |
|----------|--------|
| Comandos como archivos .py independientes | máxima modularidad |
| Seguridad por AST | detectar antes de ejecutar |
| Usuario = usuario del anfitrión | simplicidad y realismo alpha |
| rootfs/home para homes | escalabilidad y analogía Unix |
| Tests al arranque | no operar sobre base rota |
| update con backup local | reducir riesgo de pérdida de trabajo |
| docs/man + comando man | ayuda extendida estilo Unix |

---

## 15. Límites actuales de diseño

En esta baseline el diseño no incluye todavía:

1. sistema real de paquetes instalables multi-repo
2. permisos internos ricos multi-usuario MetsuOS
3. IPC entre comandos
4. UI gráfica
5. sandbox OS-level de procesos

Las reservas `packages/` y `repos/` existen para no cerrar esas líneas de evolución.

---

## 16. Guía práctica para modificar el sistema

| Si necesitas... | Toca principalmente... | No olvides... |
|-----------------|------------------------|---------------|
| Cambiar el prompt o el REPL | shell.py | tests de arranque |
| Cambiar resolución de comandos | cmd_loader.py | ICD + tests loader |
| Cambiar política de imports | security.py | SEC + tests security |
| Cambiar homes/migración | user.py | USER reqs + tests user |
| Añadir comando de sistema | moslib/commands/<cmd>.py | contrato, man, tests, help |
| Añadir comando de usuario | rootfs/home/.../user_*.py | prefijo user_ y seguridad |
| Cambiar normas de producto | docs/specs/ | luego código y tests |

---

## 17. Autoridad

Este SDD describe el diseño de la baseline actual.

Si el código cambia de arquitectura, este documento debe actualizarse en la misma fase o inmediatamente después, antes de considerar el cambio cerrado.