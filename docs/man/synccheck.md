# synccheck

## NOMBRE
synccheck – compara el clone local con origin/main

## SINOPSIS
synccheck

## DESCRIPCIÓN
Hace git fetch origin y muestra:

- SHA de HEAD local
- SHA de origin/main
- si están sincronizados
- version de Poetry y línea de versión del README en origin/main
- URL raw de GitHub anclada a ese SHA (no uses /main/ a secas para auditar)

No usa APIs de un forge. Solo Git.

## EJEMPLOS
synccheck

## SEGURIDAD
Comando de sistema. stdlib + moslib. Requiere red para fetch.

## VÉASE TAMBIÉN
update, version