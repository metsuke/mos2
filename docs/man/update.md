# update

## NOMBRE
update – actualiza MetsuOS desde origin/main con backup local

## SINOPSIS
update

## DESCRIPCIÓN
Sincroniza la copia local del producto con origin/main de forma forzada.

Si hay cambios locales pendientes:

1. crea una rama backup/YYYYMMDD_HHMMSS
2. preserva ahí el trabajo local
3. vuelve a main
4. hace fetch + reset hard a origin/main
5. elimina ramas backup antiguas dejando un máximo controlado

Las ramas backup son locales y no se publican como parte del producto.

## OPCIONES
Ninguna en esta baseline.

## EJEMPLOS
update

## SEGURIDAD
Comando de sistema. Opera sobre el repositorio git del producto. Úsalo solo cuando quieras alinear tu árbol local con el remoto.

## VÉASE TAMBIÉN
version, test, help