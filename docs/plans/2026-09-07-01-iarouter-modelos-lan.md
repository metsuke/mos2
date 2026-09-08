# Plan — mini campaña iarouter: modelos, claves, LAN y share

**Fecha:** 2026-09-07  
**Revisado:** 2026-09-08  
**Orden del día:** 01  
**Producto de partida:** 0.2.7  
**Antes de:** campaña 08 (app de desarrollo)  
**No es:** suite aceptar/commit, malla P2P (campaña 10), RGPD

---

## Por qué

El cierre 07 dejó iarouter usable (detectar / usar / preguntar). Falta lo que hace el frente usable entre máquinas y con proveedores de pago:

1. Listar y elegir **modelo** en Jan, GPT4All, Grok y OpenRouter.
2. **Guardar claves** dentro de MetsuOS, no solo leer el entorno.
3. **Jan en LAN** de forma fiable (el barrido desde Mac no vio los Windows).
4. **`iarouter share`**: diagnosticar si el servidor local se puede usar desde otra máquina (firewall, bind, puerto).
5. **Puente local** (no es la malla P2P): un endpoint de *este* MetsuOS para que otro MetsuOS de la LAN llame a Jan/GPT4All de aquí si no lo encuentra solo.
6. Si el sistema anfitrión impide compartir: **guía** y, solo con orden explícita, un comando que intente abrir lo mínimo.

---

## Claves API

Al ejecutar `iarouter usar grok` o `iarouter usar openrouter`:

- Si hay clave en memoria de MetsuOS → se usa.
- Si no, se lee del entorno (`XAI_API_KEY`, `OPENROUTER_API_KEY`, `JAN_API_KEY` si aplica).
- Si tampoco hay: el comando **pide** la clave al humano (una línea) y la guarda.

Dónde: espacio de usuario (`.mos/config/`), nunca git, permisos restrictivos del fichero.

Cómo: cifrado en reposo con secreto que no viaja en el repo. Primera versión: envoltorio con secreto local (passphrase del usuario o secreto de máquina en `.mos` no versionado). Si el cifrado fuerte no cabe en stdlib+moslib, se documenta el límite y no se finge AES de juguete. Las claves no se imprimen en `status`, `detectar` ni logs.

Comando de apoyo: `iarouter clave <proveedor>` (alta / borra). No hay subcomando que vuelque la clave.

---

## Modelos

| Subcomando | Efecto |
|------------|--------|
| iarouter modelos [proveedor] | Lista ids del activo o del indicado |
| iarouter modelo <id> | Fija el modelo en la política |
| iarouter preguntar TEXTO | Usa ese id; si es `auto`, el primero de la lista |

Hay que probar Grok y OpenRouter de verdad (listar + preguntar), no solo “variable presente”.

---

## Jan / GPT4All en LAN

Orden: `127.0.0.1` → cache válida → `/24` de las interfaces privadas. Puerto Jan 1337, GPT4All 4891. Cache con TTL. El motivo dice host y origen (local / cache / LAN).

---

## Share, guía y puente

Esto **no** es la matriz P2P. Es un mecanismo extra de la LAN.

### iarouter share

Evalúa y muestra, en tabla + párrafo por ítem:

- Si Jan/GPT4All escuchan en localhost.
- Si escuchan en `0.0.0.0` o solo en loopback.
- Puerto.
- Si el firewall del anfitrión (según perfil de entorno) parece bloquear ese puerto hacia la LAN.
- Si hay cache de un Jan ajeno.

Si no se puede compartir: texto de guía **por entorno** (macos/native, windows/git-bash, windows/wsl, linux/native). Sin recetas de ataque; solo lo que el dueño de la máquina tiene que abrir en *su* firewall y en la app Jan/GPT4All (bind).

### iarouter publicar

Nombre del comando de autorización explícita. No corre dentro de `share` ni de `usar`.

Hace solo lo que el humano confirma: intentar regla mínima de firewall y/o recordar bind en `0.0.0.0`. Si el anfitrión no deja (permisos, WSL, política de empresa), falla con el mismo texto de guía. Nunca “abrir el mundo”: interfaz LAN, puerto concreto.

### iarouter puente

Endpoint HTTP **de MetsuOS** en la LAN (no el de Jan crudo si Jan no es alcanzable). Otro MetsuOS puede usar esa URL como `jan_url` / puente. Off por defecto. Arranque y parada explícitos. No atraviesa NAT ni Internet. No sustituye la campaña 10.

---

## Hecho significa

1. `modelos` / `modelo` / `preguntar` con id persistido.
2. Clave pedida al `usar` si falta; guardada en `.mos`; no sale en listados.
3. Grok y OpenRouter listan modelos con la API y aceptan `preguntar` a un id elegido.
4. Jan: local, cache o LAN; el motivo es legible.
5. `share` diagnostica bind + firewall + guía.
6. `publicar` solo con invocación explícita.
7. `puente` opcional, off por defecto, solo LAN.
8. Tests: off no llama red; `.mos` en payload se rechaza; clave no aparece en status; listar no tumba el shell sin red.
9. Spec 10 y man actualizados.

---

## Fuera

Suite 08. P2P/Onion. Escanear Internet. Guardar claves en git. Campaña de formatos de pantalla (sigue en DEUDA).

---

## Bloques

| Id | Qué |
|----|-----|
| M0 | Este plan + DEUDA (08 después de esta mini campaña) |
| M1 | Listar / fijar modelo + tests |
| M2 | Almacén de claves + prompt en `usar` |
| M3 | Grok y OpenRouter: GET modelos + preguntar |
| M4 | Descubrimiento Jan/GPT4All LAN + cache + diagnóstico |
| M5 | `share` + guía por entorno |
| M6 | `publicar` (autorización explícita) |
| M7 | `puente` LAN de MetsuOS |
| M8 | Spec 10.2, man, CHANGELOG; tag 0.2.8 si hay runtime |

M1–M3 no dependen de que el Mac vea un Jan Windows. M4–M7 sí se prueban en dos máquinas cuando existan.

---

## Criterio de cierre

Checklist al 9/9. Luego se retoma la 08.