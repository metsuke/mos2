# man

## NOMBRE
man – muestra el manual extendido de un comando

## SINOPSIS
man
man <comando>

## DESCRIPCIÓN
man consulta las páginas de manual almacenadas en docs/man/.

Sin argumentos, lista las páginas disponibles.
Con un nombre de comando, muestra el manual extendido correspondiente.

A diferencia de help, man está pensado para explicación más completa: sinopsis, descripción, ejemplos y referencias.

## OPCIONES
Ninguna. El primer argumento se interpreta como nombre de comando.

## EJEMPLOS
man
man update
man help

## SEGURIDAD
Comando de sistema. Solo lee archivos de documentación del producto.

## VÉASE TAMBIÉN
help, docs/USER_MANUAL.md