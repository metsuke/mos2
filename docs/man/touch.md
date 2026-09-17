# touch

## NOMBRE
touch – crea un fichero vacío en el clone

## SINOPSIS

- touch <ruta>

## DESCRIPCIÓN
Crea el fichero indicado si no existe. La ruta es relativa a la raíz del clone, no al directorio de trabajo del anfitrión.
Si faltan directorios intermedios, los crea.
No pisa el contenido de un fichero que ya existe; solo actualiza la marca de tiempo.

## SEGURIDAD
Rechaza rutas que salgan del clone.
No llama a la utilidad touch del anfitrión; usa pathlib.
Comando de sistema. Solo stdlib y moslib.

## VÉASE TAMBIÉN
code, git, docs