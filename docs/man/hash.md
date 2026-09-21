# hash

## NOMBRE
hash - SHA-256 de un fichero del clone

## SINOPSIS

- hash <ruta>

## DESCRIPCION
Imprime el SHA-256 hex de la ruta.
La ruta es relativa a la raiz del clone.
Sirve para contrastar la primera linea de un lote write.

## SEGURIDAD
No escribe. Rechaza rutas fuera del clone.
Comando de sistema. Solo stdlib y moslib.

## VEASE TAMBIEN
write, integridad, code