# 03 – ICD · Interfaces y contrato de comandos

**Versión del documento:** 1.1  
**Baseline de referencia:** v0.2.4  
**Estado:** Normativo  
**Documentos relacionados:** docs/specs/01-SSS-System-Specification.md, docs/specs/04-SEC-Security-Policy.md, docs/A11Y.md, docs/STYLE_GUIDE.md

---

## Propósito

Este documento define las interfaces internas principales de MetsuOS y el contrato obligatorio de los comandos.

Su función es evitar que núcleo, comandos y espacio de usuario se acoplen de forma implícita o incompatible.

---

## Alcance

Cubre:

1. Contrato de todo comando (sistema o usuario)
2. Resolución de nombres de comando
3. Interfaz shell ↔ command loader
4. Interfaz command loader ↔ security
5. Interfaz shell/user ↔ espacio personal
6. Punto de entrada del sistema
7. Ayuda, man y consulta de documentación
8. Actualización y tags
9. Tests de arranque e informe A11Y

No cubre el detalle interno de cada comando concreto, salvo su contrato común.

---

## Contrato de comando

Todo comando válido, de sistema o de usuario, debe ser un módulo Python que exponga:

### execute(args)

- Nombre: `execute`
- Tipo: callable
- Parámetro: `args` (lista de argumentos ya segmentados por el shell)
- Responsabilidad: ejecutar la acción del comando
- No debe depender de un registro manual externo
- Solo imports de biblioteca estándar y de moslib

### help()

- Nombre: `help`
- Tipo: callable
- Retorno: `str` no vacío
- Responsabilidad: devolver texto de ayuda usable por el sistema de ayuda, por A11Y y por el usuario

### Reglas adicionales

1. El módulo se descubre por archivo `.py` en un directorio de comandos.
2. El nombre del comando de sistema coincide con el nombre del archivo sin extensión.
3. El nombre de archivo de un comando de usuario debe empezar por `user_`.
4. Un comando de usuario nunca sobrescribe un comando de sistema.

---

## Ubicación de comandos

| Tipo | Ubicación | Patrón de archivo |
|------|-----------|-------------------|
| Sistema | moslib/commands/ | `<nombre>.py` |
| Usuario | rootfs/home/<usuario>/.mos/commands/ | `user_<nombre>.py` |

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 | Descripción |
|---------|---------|---------|---------|---------|-------------|
| moslib/ | commands/ | | | | Comandos de sistema |
| rootfs/ | home/ | `<usuario>/` | .mos/ | commands/ | Comandos de usuario |

---

## Resolución de nombres de comando

El orden de resolución es obligatorio:

### Prioridad 1 · Comando de sistema

Si existe `moslib/commands/<nombre>.py`, se usa ese.

### Prioridad 2 · Nombre completo de usuario

Si el usuario escribe `user_<nombre>` y existe `user_<nombre>.py` en su espacio, se usa ese.

### Prioridad 3 · Nombre corto de usuario

Si el usuario escribe `<nombre>` y no existe comando de sistema con ese nombre, se busca `user_<nombre>.py`.

### Resultado si no hay match

El shell informa que el comando no fue encontrado, con texto claro (sin basarse solo en color).

### Tabla resumen

| Entrada del usuario | ¿Existe sistema? | ¿Existe user_X? | Resultado |
|---------------------|------------------|-----------------|-----------|
| help | Sí | Irrelevante | Sistema help |
| user_hola | No aplica para sistema con ese nombre literal | Sí | Usuario user_hola |
| hola | No | Sí | Usuario user_hola |
| hola | Sí | Sí o no | Sistema hola |
| noexiste | No | No | No encontrado |

---

## Interfaz Shell ↔ CommandManager

### Componentes

| Componente | Módulo | Responsabilidad |
|------------|--------|-----------------|
| Shell | moslib/core/shell.py | Leer entrada, invocar comandos, controlar ciclo de vida |
| CommandManager | moslib/core/cmd_loader.py | Resolver, validar y cargar módulos de comando |

### Contrato de uso

El shell obtiene un módulo de comando mediante una operación equivalente a:

```text
get_command(cmd_name) -> module | None
```

Si el resultado no es `None` y el módulo tiene `execute`, el shell llama:

```text
module.execute(args)
```

### Seguridad en la interfaz

CommandManager debe aplicar la validación de seguridad antes de devolver un módulo ejecutable en operación normal.

---

## Interfaz CommandManager ↔ Security

### Componente de seguridad

| Componente | Módulo | Responsabilidad |
|------------|--------|-----------------|
| Security | moslib/core/security.py | Analizar fuente y decidir si un comando es admisible |

### Operación principal

```text
validate_command_file(path) -> (ok: bool, errors: list[str])
```

Reglas:

1. Si `ok` es False, el comando no se carga
2. `errors` debe contener motivos legibles, con prefijo estable en el mensaje al usuario (`[SEGURIDAD]`)
3. La validación es estática (AST), no ejecuta el comando

---

## Interfaz de usuario y espacio personal

### Componente

| Componente | Módulo | Responsabilidad |
|------------|--------|-----------------|
| User | moslib/core/user.py | Resolver usuario anfitrión, rutas y espacio .mos |

### Operaciones conceptuales

| Operación | Resultado esperado |
|-----------|--------------------|
| get_username() | Nombre del usuario del sistema anfitrión |
| get_project_root() | Raíz del proyecto MetsuOS |
| get_user_home() | rootfs/home/<usuario> |
| get_user_mos_dir() | rootfs/home/<usuario>/.mos |
| ensure_user_space() | Crea estructura .mos si falta y aplica migración legacy si procede |

### Migración legacy

Si existe una ubicación antigua de home de usuario y no existe la nueva, el sistema debe migrar de forma automática a:

```text
rootfs/home/<usuario>/
```

---

## Punto de entrada del sistema

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| rootfs/ | bin/ | mos.py | Entrada principal del shell |

Responsabilidad de `mos.py`:

1. Preparar el path de importación del proyecto si hace falta
2. Instanciar el shell
3. Lanzar el bucle interactivo

No debe contener lógica de negocio que pertenezca a `moslib/core`.

---

## Interfaz de ayuda

### help de sistema

El comando `help` debe poder:

- listar comandos disponibles
- mostrar ayuda de un comando concreto
- distinguir, cuando proceda, origen de sistema o de usuario

### help() de cada comando

Cada comando aporta su propia ayuda mediante `help()`.

### man

La interfaz de documentación extendida de comandos se basa en páginas:

| Nivel 1 | Nivel 2 | Nivel 3 | Descripción |
|---------|---------|---------|-------------|
| docs/ | man/ | `<comando>.md` | Manual extendido del comando |

El comando de sistema `man` debe leer esas páginas y mostrarlas al usuario.

---

## Interfaz de documentación general

El comando de sistema `docs` (baseline 0.2.5) consulta el árbol `docs/` del clone.

Comportamiento de interfaz:

- sin argumentos: listar documentos disponibles (paths relativos a `docs/`)
- con argumento: mostrar el fichero si está bajo `docs/` (p. ej. `A11Y.md`, `a11y/DECLARACION.md`, `a11y/informe.md`, `plans/...`, `specs/...`)
- no debe salir del árbol `docs/`
- salida en texto plano, usable por lector de terminal

---

## Interfaz de accesibilidad

El comando de sistema `a11y` (baseline 0.2.5):

- ejecuta solo tests con marca `a11y`
- escribe `docs/a11y/informe.md` y `docs/a11y/informe.json`
- imprime la situación de cumplimiento en texto

El comando `test` (batería completa) regenera el mismo informe si esa batería incluye tests `a11y`.

---

## Interfaz de actualización

El comando `update` interactúa con el repositorio git del producto (Git, no un forge).

Contrato de comportamiento a nivel de interfaz de sistema:

1. Detectar cambios locales pendientes
2. Si existen, preservarlos en una rama local `backup/YYYYMMDD_HHMMSS`
3. Fetch de origin
4. Sincronizar tags locales con origin (alta y baja)
5. Sincronizar `main` con `origin/main` de forma forzada
6. Podar ramas `backup/*` antiguas dejando un máximo controlado

Esta interfaz no publica automáticamente las ramas backup al remoto.

---

## Interfaz de tests de arranque

Antes de entrar en modo interactivo, el shell debe invocar la batería de tests del proyecto.

Interfaz conceptual:

```text
run_startup_tests() -> bool
```

- True: continuar arranque
- False: abortar arranque con mensaje claro y accionable

---

## Datos intercambiados en la ejecución de un comando

| Dato | Dirección | Formato | Notas |
|------|-----------|---------|-------|
| Línea de entrada | Usuario → Shell | str | Texto crudo |
| cmd_name | Shell → Loader | str | Primer token |
| args | Shell → Comando | list[str] | Resto de tokens |
| module | Loader → Shell | module/None | Tras seguridad |
| salida | Comando → Usuario | texto en stdout/stderr | Mensajes de negocio o error |

---

## Invariantes de interfaz

1. El shell no ejecuta un comando sin pasar por el loader en operación normal.
2. El loader no entrega un comando ilegal si la seguridad está activa.
3. El nombre corto de usuario nunca gana a un comando de sistema.
4. `help()` de un comando siempre devuelve string no vacío.
5. El espacio de usuario no se usa como fuente de comandos de sistema.
6. `docs` no lee ficheros fuera de `docs/`.
7. El color no es la única señal de resultado en las interfaces de este ICD.

---

## Verificación de este ICD

Se verifica mediante:

1. Tests de contrato execute/help
2. Tests de resolución de nombres y seguridad en loader
3. Tests de espacio de usuario
4. Pruebas manuales de invocación con y sin prefijo `user_`
5. Arranque con y sin comandos ilegales
6. Tests A11Y y comando docs cuando existan en 0.2.5

---

## Autoridad

Este ICD es normativo para cualquier cambio en la forma de descubrir, cargar, nombrar o invocar comandos.

Romper este contrato requiere actualización explícita del documento y de sus tests asociados.