# Manual de usuario de MetsuOS (MOS2)

**Versión del documento:** 1.4  
**Baseline de referencia:** v0.2.7 (árbol hacia v0.2.8)  
**Estado:** Manual formal de usuario  
**Documentos relacionados:** docs/man/, docs/ENVIRONMENTS.md, docs/METHODOLOGY.md, docs/HUMAN_ONBOARDING.md, docs/IA_WRITE.md

---

## Introducción
MetsuOS (también llamado MOS2) es un sistema operativo simulado y modular escrito en Python.

Su interfaz principal es el shell **MOSh**, donde puedes ejecutar:

- comandos oficiales del sistema
- comandos de apps instaladas
- comandos personales de usuario
- utilidades de ayuda, tests, actualización y documentación

Este manual explica cómo instalar, arrancar y usar MetsuOS en la práctica.

Para ayuda extendida de un comando concreto:

```text
man <comando>
```

La v1.2 se conserva. Esta v1.3 añade `multi`/`write`, menú `docs`, `test 120` e integridad.

---

## Qué necesitas
- Python 3.10 o superior
- Poetry
- Git
- Terminal en Linux, macOS o Windows (Git Bash o WSL)

---

## Instalación
1. Clona el repositorio:

```text
git clone https://github.com/metsuke/mos2.git
cd mos2
```

2. Ejecuta el instalador:

```text
chmod +x install.sh
./install.sh
```

### Aliases opcionales

| Alias | Función |
|-------|---------|
| mos2 | Lanza MetsuOS |
| mos2f | Va a la raíz del proyecto |
| mos2u | Relanza el instalador |

---

## Entornos de ejecución
| Sistema | Entorno | Notas |
|---------|----------|-------|
| linux | native | Poetry habitual en PATH |
| macos | native | Igual |
| windows | git-bash | Lanzador prioriza poetry.exe / python -m poetry |
| windows | wsl | Clone en filesystem Linux |

Usa siempre `./install.sh` y `./mos2.sh` desde la **raíz del clone**. Normativa: `docs/ENVIRONMENTS.md`.

---

## Arranque
```text
./mos2.sh
```

o alias `mos2`.

1. Comprueba integridad de ficheros del repo.
2. Ejecuta la batería de tests (barra de progreso, varios hilos).
3. Si integridad o tests fallan, no entra en modo interactivo.
4. Si todo pasa, MOSh muestra prompt, historial con flechas, y avisos de `multi`/`m`.

---

## Conceptos básicos
### MOSh

Shell de MetsuOS. Historial con flechas. Lotes con `multi` o `m`.

### Usuario

Nombre del anfitrión.

### Espacio personal

| Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 | Uso |
|---------|---------|---------|---------|---------|-----|
| rootfs/ | home/ | usuario/ | .mos/ | | Raíz personal |
| | | | | commands/ | Tus comandos |
| | | | | apps/ | Apps de ámbito usuario |
| | | | | data/ | Tus datos |
| | | | | config/ | Tu configuración |

No se sube al repositorio principal.

Prioridad de comandos: sistema > app de sistema > app de usuario > `user_`.

---

## Comandos de sistema
| Tipo | Comando | Descripción |
|------|---------|-------------|
| accesibilidad | a11y | Tests A11Y e informe |
| apps | apps | Instalar, listar, ver y quitar apps |
| ayuda | docs | Menú por categoría; número o Nh (HTML) |
| ayuda | help | Lista de comandos o ayuda de uno |
| ayuda | man | Manual extendido |
| calidad | synccheck | Compara HEAD con origin/main |
| calidad | test | Batería; `test 120` lista tope de líneas |
| calidad | update | Sincroniza; `update dev` ramas no main |
| desarrollo | dev | Publicar / consolidar rama de desarrollo |
| desarrollo | multi / m | Pegar lote; `:e` ejecuta, `:q` cancela |
| host | sysinfo | Información del anfitrión |
| host | uptime | Tiempo activo |
| host | version | Versión e historial Git |
| ia | iarouter | Modelos; off hasta activarlo |
| red | red | Diagnóstico del anfitrión |
| sesion | exit | Sale |
| tareas | hilos | Vista de tareas |
| tareas | tareas | Tareas locales |
| utilidad | clear | Limpia pantalla |
| utilidad | echo | Imprime texto |
| utilidad | git / code / touch | Wrappers desde la raíz del clone |

Fuera de MOS, si no arranca: `./write.sh` (mismo ritual que multi).

---

## Ayuda: help, man y docs
### help

`help` lista; `help <comando>` detalle.

### man

`man` lista; `man <comando>` manual en docs/man/.

### docs

1. Lista categorías numeradas.
2. Eliges categoría.
3. Lista documentos. `N` abre markdown; `Nh` abre HTML con el visor del sistema.

---

## Crear tus propios comandos
Archivo `rootfs/home/<usuario>/.mos/commands/user_<nombre>.py` con `execute` y `help`. No pisa sistema. Solo stdlib y moslib.

---

## Apps
`apps list|show|install|remove`. Sin A11Y mínima no se acepta. Detalle: specs 08 y `man apps`.

---

## Tareas e hilos
`tareas` y `hilos`. Locales. Specs 09.

---

## iarouter
Apagado hasta `usar` / `preguntar`. Specs 10. `iarouter share` / `iarouter connect` para Jan en LAN.

---

## Seguridad de comandos
Solo stdlib, moslib y minimoslib de la app. Import ilegal: rechazo y posible bloqueo de arranque.

---

## Tests
```text
test
test 120
a11y
```

Arranque ejecuta la batería (no el tope 120 como fallo). Si fallan, no hay sesión.

---

## Actualizar MetsuOS
`update` alinea con origin/main si el trabajo local es de main. `update dev` elige rama no-main. `dev publicar` sube la rama de prueba. Tras update: `update reiniciar` o `exit` + `./mos2.sh`.

`synccheck` no cambia nada.

---

## Lotes write / multi
Dentro de MOS: `m` o `multi`. Pegas el bloque (write + hash + payload + `.` + otros comandos). Línea sola `:e` ejecuta; `:q` cancela. El punto suelto cierra el payload.

Fuera de MOS: `./write.sh` con el mismo bloque.

---

## Flujo de trabajo recomendado
1. Arranca MetsuOS
2. `help`, `man` o `docs`
3. Trabaja
4. Apps o `user_*` si hace falta
5. `test` / `test 120` si tocas código
6. `update` + `update reiniciar` para alinear

---

## Problemas frecuentes
| Síntoma | Qué mirar |
|---------|-----------|
| No arranca | Tests o integridad |
| Integridad en rojo | Cambio no registrado; write.sh o recargar solo si es tuyo |
| Permission denied Poetry | ./mos2.sh |
| CRLF en scripts | Convertir a LF |
| user_* no aparece | nombre, execute/help, imports |
| Tras update no ves código | update reiniciar |

---

## Dónde encontrar más documentación
| Documento | Contenido |
|-----------|-----------|
| docs/USER_MANUAL.md | Este manual |
| docs/HUMAN_ONBOARDING.md | Primer arranque |
| docs/ENVIRONMENTS.md | Perfiles y Poetry |
| docs/man/ | Manual por comando |
| docs/IA_WRITE.md | Ritual write |
| docs/specs/ | Especificaciones |
| README.md | Visión |
| CHANGELOG.md | Releases |

---

## Limitaciones de la fase Alpha
No sustituye el anfitrión. No es kernel. No hay paquetes Python arbitrarios en comandos. No es malla P2P. Evolución activa.

---

## Salir
```text
exit
```