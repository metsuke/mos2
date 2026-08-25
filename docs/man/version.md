# version

## NOMBRE
version – muestra la versión de MetsuOS y su historial

## SINOPSIS
version
version -h [n]

## DESCRIPCIÓN
Sin argumentos, muestra la versión actual basada en git describe.

Con -h, muestra historial de versiones. Si se indica n, limita la cantidad de entradas.

El historial prioriza tags y puede completar con commits recientes según la implementación del comando.

## OPCIONES
| Opción | Significado |
|--------|-------------|
| -h | Muestra historial |
| -h n | Muestra hasta n entradas de historial |

## EJEMPLOS
version
version -h
version -h 20

## SEGURIDAD
Comando de sistema. Consulta metadatos git del repositorio del producto.

## VÉASE TAMBIÉN
update, help, man