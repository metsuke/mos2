# code

## NOMBRE
code – abre un fichero del clone en el editor del anfitrión

## SINOPSIS

- code <ruta>

## DESCRIPCIÓN
Abre la ruta con el binario code (VS Code) o, si no está, cursor.
La ruta es relativa a la raíz del clone.
Si el fichero no existe, lo crea vacío y después abre el editor.

## SEGURIDAD
Rechaza rutas fuera del clone.
Ejecuta solo code o cursor del PATH del anfitrión, con cwd en la raíz del clone.
Comando de sistema. Solo stdlib y moslib.

## VÉASE TAMBIÉN
touch, git, docs