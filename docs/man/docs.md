# docs

## NOMBRE
docs – consulta la documentación del clone desde MOSh

## SINOPSIS
docs
docs <ruta>

## DESCRIPCIÓN
Sin argumentos, lista:

- ficheros públicos de la raíz: README.md, CHANGELOG.md, AGENTS.md, LICENSE
- todos los ficheros bajo docs/

Con argumento, muestra el contenido en texto plano si la ruta está permitida.

Rutas válidas:

- README.md, CHANGELOG.md, AGENTS.md, LICENSE
- cualquier fichero bajo docs/ (A11Y.md, a11y/DECLARACION.md, specs/..., plans/..., man/...)
- también se acepta el prefijo docs/ delante de una ruta interna

No se pueden leer rutas fuera de esa lista (por ejemplo el espacio de usuario o ficheros del anfitrión).

Pensado para teclado y lector de terminal.

## OPCIONES
Ninguna en esta baseline. La ruta es el resto de la línea.

## EJEMPLOS
docs
docs README.md
docs A11Y.md
docs a11y/DECLARACION.md
docs a11y/informe.md

## SEGURIDAD
Comando de sistema. Solo stdlib y moslib. Resuelve paths y rechaza lo que salga de docs/ o de la lista blanca de la raíz.

## VÉASE TAMBIÉN
a11y, man, help