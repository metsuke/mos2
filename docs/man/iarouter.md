# iarouter

## NOMBRE
iarouter – enrutador de modelos (local y remoto)

## SINOPSIS
iarouter
iarouter status
iarouter detectar
iarouter usar jan|gpt4all|grok|openrouter
iarouter clave <proveedor> [borrar]
iarouter modelos [proveedor]
iarouter modelo [proveedor] <id del modelo...>
iarouter preguntar TEXTO

## DESCRIPCIÓN
Muestra el proveedor activo, detecta cuáles están disponibles y, solo con
`preguntar`, envía el texto al modelo y lo imprime.

`usar` escribe la política local (enabled=true y el proveedor). La IA no
escribe esa política.

`modelos` lista los ids que publica el proveedor. `modelo` fija el id
activo (puede llevar espacios; el proveedor solo si el primer token es
jan, gpt4all, grok u openrouter).

`clave` guarda la clave en `.mos/config/` envuelta con moslib.core.secreto.
No imprime la clave. Si existe XAI_API_KEY u OPENROUTER_API_KEY en el
entorno y aún no hay valor en `.mos`, se copia al almacén.

## DETECCIÓN
- jan: HTTP local (127.0.0.1:1337) y, si falta, /24 privada con cache
- gpt4all: HTTP local, por defecto http://127.0.0.1:4891/v1/
- grok: clave en .mos o XAI_API_KEY (se ingiere)
- openrouter: clave en .mos o OPENROUTER_API_KEY (se ingiere)

Sin clave o sin servidor, el proveedor aparece como no disponible.
`usar` un proveedor no disponible se rechaza. Si falta la clave de grok
u openrouter, `usar` pide la clave (sin eco).

## SEGURIDAD
Off por defecto hasta `usar`.
No incluye rutas `.mos` en el payload salvo allowlist del humano.
Las claves no van a git. El JSON del almacén no lleva el texto en claro.
Quien copie a la vez `.ia_wrap` e `ia_keys.json` puede recuperarlas.
Solo stdlib y moslib.

## VER TAMBIÉN
docs/specs/10-IA-ROUTER.md