# 03 – ICD · Interfaces y contrato de comandos

**Versión del documento:** 1.0  
**Baseline de referencia:** v0.2.1  
**Estado:** Normativo  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/04-SEC-Security-Policy.md, docs/STYLE_GUIDE.md

---

## 1. Propósito

Este documento define las interfaces internas principales de MetsuOS y el contrato obligatorio de los comandos.

Su función es evitar que núcleo, comandos y espacio de usuario se acoplen de forma implícita o incompatible.

---

## 2. Alcance

Cubre:

1. Contrato de todo comando (sistema o usuario)
2. Resolución de nombres de comando
3. Interfaz shell ↔ command loader
4. Interfaz command loader ↔ security
5. Interfaz shell/user ↔ espacio personal
6. Punto de entrada del sistema

No cubre el detalle interno de cada comando concreto, salvo su contrato común.

---

## 3. Contrato de comando

Todo comando válido, de sistema o de usuario, debe ser un módulo Python que exponga:

### 3.1 execute(args)

- Nombre: `execute`
- Tipo: callable
- Parámetro: `args` (lista de argumentos ya segmentados por el shell)
- Responsabilidad: ejecutar la acción del comando
- No debe depender de un registro manual externo

### 3.2 help()

- Nombre: `help`
- Tipo: callable
- Retorno: `str`
- Responsabilidad: devolver texto de ayuda usable por el sistema de ayuda y por el usuario

### 3.3 Reglas adicionales

1. El módulo se descubre por archivo `.py` en un directorio de comandos.
2. El nombre del comando de sistema coincide con el nombre del archivo sin extensión.
3. El nombre de archivo de un comando de usuario debe empezar por `user_`.
4. Un comando de usuario nunca sobrescribe un comando de sistema.

---

## 4. Ubicación de comandos

| Tipo | Ubicación | Patrón de archivo |
|------|-----------|-------------------|
| Sistema | moslib/commands/ | `<nombre>.py` |
| Usuario | rootfs/home/<usuario>/.mos/commands/ | `user_<nombre>.py` |

Estructura de referencia:

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 | Descripción |
|---------|---------|---------|---------|---------|-------------|
| moslib/ | commands/ | | | | Comandos de sistema |
| rootfs/ | home/ | `<usuario>/` | .mos/ | commands/ | Comandos de usuario |

---

## 5. Resolución de nombres de comando

El orden de resolución es obligatorio:

### 5.1 Prioridad 1 · Comando de sistema

Si existe `moslib/commands/<nombre>.py`, se usa ese.

### 5.2 Prioridad 2 · Nombre completo de usuario

Si el usuario escribe `user_<nombre>` y existe `user_<nombre>.py` en su espacio, se usa ese.

### 5.3 Prioridad 3 · Nombre corto de usuario

Si el usuario escribe `<nombre>` y no existe comando de sistema con ese nombre, se busca `user_<nombre>.py`.

### 5.4 Resultado si no hay match

El shell informa que el comando no fue encontrado.

### 5.5 Tabla resumen

| Entrada del usuario | ¿Existe sistema? | ¿Existe user_X? | Resultado |
|---------------------|------------------|-----------------|-----------|
| help | Sí | Irrelevante | Sistema help |
| user_hola | No aplica para sistema con ese nombre literal | Sí | Usuario user_hola |
| hola | No | Sí | Usuario user_hola |
| hola | Sí | Sí o no | Sistema hola |
| noexiste | No | No | No encontrado |

---

## 6. Interfaz Shell ↔ CommandManager

### 6.1 Componentes

| Componente | Módulo | Responsabilidad |
|------------|--------|-----------------|
| Shell | moslib/core/shell.py | Leer entrada, invocar comandos, controlar ciclo de vida |
| CommandManager | moslib/core/cmd_loader.py | Resolver, validar y cargar módulos de comando |

### 6.2 Contrato de uso

El shell obtiene un módulo de comando mediante una operación equivalente a:

get_command(cmd_name) -> module | None

Si el resultado no es `None` y el módulo tiene `execute`, el shell llama:

module.execute(args)

### 6.3 Seguridad en la interfaz

CommandManager debe aplicar la validación de seguridad antes de devolver un módulo ejecutable en operación normal.

---

## 7. Interfaz CommandManager ↔ Security

### 7.1 Componente de seguridad

| Componente | Módulo | Responsabilidad |
|------------|--------|-----------------|
| Security | moslib/core/security.py | Analizar fuente y decidir si un comando es admisible |

### 7.2 Operación principal

validate_command_file(path) -> (ok: bool, errors: list[str])

Reglas:

1. Si `ok` es False, el comando no se carga
2. `errors` debe contener motivos legibles
3. La validación es estática (AST), no ejecuta el comando

---

## 8. Interfaz de usuario y espacio personal

### 8.1 Componente

| Componente | Módulo | Responsabilidad |
|------------|--------|-----------------|
| User | moslib/core/user.py | Resolver usuario anfitrión, rutas y espacio .mos |

### 8.2 Operaciones conceptuales

| Operación | Resultado esperado |
|-----------|--------------------|
| get_username() | Nombre del usuario del sistema anfitrión |
| get_project_root() | Raíz del proyecto MetsuOS |
| get_user_home() | rootfs/home/<usuario> |
| get_user_mos_dir() | rootfs/home/<usuario>/.mos |
| ensure_user_space() | Crea estructura .mos si falta y aplica migración legacy si procede |

### 8.3 Migración legacy

Si existe una ubicación antigua de home de usuario y no existe la nueva, el sistema debe migrar de forma automática a:

rootfs/home/<usuario>/

---

## 9. Punto de entrada del sistema

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| rootfs/ | bin/ | mos.py | Entrada principal del shell |

Responsabilidad de `mos.py`:

1. Preparar el path de importación del proyecto si hace falta
2. Instanciar el shell
3. Lanzar el bucle interactivo

No debe contener lógica de negocio que pertenezca a `moslib/core`.

---

## 10. Interfaz de ayuda

### 10.1 help de sistema

El comando `help` debe poder:

- listar comandos disponibles
- mostrar ayuda de un comando concreto
- distinguir, cuando proceda, origen de sistema o de usuario

### 10.2 help() de cada comando

Cada comando aporta su propia ayuda mediante `help()`.

### 10.3 man

La interfaz de documentación extendida se basa en páginas:

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| docs/ | man/ | `<comando>.md` | Manual extendido del comando |

El comando de sistema `man` debe leer esas páginas y mostrarlas al usuario.

---

## 11. Interfaz de actualización

El comando `update` interactúa con el repositorio git del producto.

Contrato de comportamiento a nivel de interfaz de sistema:

1. Detectar cambios locales pendientes
2. Si existen, preservarlos en una rama local `backup/YYYYMMDD_HHMMSS`
3. Sincronizar `main` con `origin/main` de forma forzada
4. Podar ramas `backup/*` antiguas dejando un máximo controlado

Esta interfaz no publica automáticamente las ramas backup al remoto.

---

## 12. Interfaz de tests de arranque

Antes de entrar en modo interactivo, el shell debe invocar la batería de tests del proyecto.

Interfaz conceptual:

run_startup_tests() -> bool

- True: continuar arranque
- False: abortar arranque con mensaje claro

---

## 13. Datos intercambiados en la ejecución de un comando

| Dato | Dirección | Formato | Notas |
|------|-----------|---------|-------|
| Línea de entrada | Usuario → Shell | str | Texto crudo |
| cmd_name | Shell → Loader | str | Primer token |
| args | Shell → Comando | list[str] | Resto de tokens |
| module | Loader → Shell | module/None | Tras seguridad |
| salida | Comando → Usuario | texto en stdout/stderr | Mensajes de negocio o error |

---

## 14. Invariantes de interfaz

1. El shell no ejecuta un comando sin pasar por el loader en operación normal.
2. El loader no entrega un comando ilegal si la seguridad está activa.
3. El nombre corto de usuario nunca gana a un comando de sistema.
4. `help()` de un comando siempre devuelve string.
5. El espacio de usuario no se usa como fuente de comandos de sistema.

---

## 15. Verificación de este ICD

Se verifica mediante:

1. Tests de contrato execute/help
2. Tests de resolución de nombres y seguridad en loader
3. Tests de espacio de usuario
4. Pruebas manuales de invocación con y sin prefijo `user_`
5. Arranque con y sin comandos ilegales

---

## 16. Autoridad

Este ICD es normativo para cualquier cambio en la forma de descubrir, cargar, nombrar o invocar comandos.

Romper este contrato requiere actualización explícita del documento y de sus tests asociados.