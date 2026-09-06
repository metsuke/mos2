# iarouter

## NOMBRE
iarouter – enrutador de modelos (local y remoto)

## SINOPSIS
iarouter
iarouter status
iarouter detectar
iarouter usar jan|gpt4all|grok|openrouter
iarouter preguntar TEXTO

## DESCRIPCIÓN
Muestra el proveedor activo, detecta cuáles están disponibles y, solo con
`preguntar`, envía el texto al modelo y lo imprime.

`usar` escribe la política local (enabled=true y el proveedor). La IA no
escribe esa política.

## DETECCIÓN
- jan: HTTP local, por defecto http://127.0.0.1:1337/v1/
- gpt4all: HTTP local, por defecto http://127.0.0.1:4891/v1/
- grok: variable de entorno XAI_API_KEY
- openrouter: variable de entorno OPENROUTER_API_KEY

Sin clave o sin servidor, el proveedor aparece como no disponible.
`usar` un proveedor no disponible se rechaza.

## SEGURIDAD
Off por defecto hasta `usar`.
No incluye rutas `.mos` en el payload salvo allowlist del humano.
Las claves no van en git.
Solo stdlib y moslib.

## VER TAMBIÉN
docs/specs/10-IA-ROUTER.md