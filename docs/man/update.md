# update

## NOMBRE
update – actualiza MetsuOS desde origin/main con backup local y tags alineados

## SINOPSIS
update
update reiniciar

## DESCRIPCIÓN
Sincroniza la copia local del producto con origin/main de forma forzada.

Si hay cambios locales pendientes:

1. crea una rama backup/YYYYMMDD_HHMMSS
2. preserva ahí el trabajo local
3. vuelve a main
4. hace fetch de origin
5. sincroniza tags con origin (alta y baja)
6. hace reset hard a origin/main
7. elimina ramas backup antiguas dejando un máximo de 10

Las ramas backup son locales y no se publican como parte del producto.

Los tags locales pasan a coincidir con los de origin. Desaparecen tags que el remoto ya no tiene. También desaparecen tags que solo existían en este clone y nunca se empujaron.

Esto usa Git (fetch --tags --prune --prune-tags), no una función de un forge concreto.

El código nuevo no sustituye los módulos ya cargados en esta sesión de MOSh. Tras update hay que salir y volver a entrar, o usar update reiniciar, que relanza rootfs/bin/mos.py (vuelve a pasar los tests de arranque).

## OPCIONES
reiniciar – relanza MOSh sobre el árbol actual. Si se combina con update (sin haber hecho solo esa palabra), primero hace el pull y después relanza.

## EJEMPLOS
update
update reiniciar

## SEGURIDAD
Comando de sistema. Opera sobre el repositorio git del producto. Úsalo solo cuando quieras alinear tu árbol local y tus tags con el remoto.

## VÉASE TAMBIÉN
version, test, help, synccheck