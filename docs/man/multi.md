# multi

## NOMBRE
multi – pega un lote de comandos y luego los ejecuta

## SINOPSIS

- multi
- m

## DESCRIPCIÓN
Entra en un prompt multi>. Ahí se pegan o escriben comandos, uno por línea.
No se ejecutan al pegar.
:e o :w lanza el lote en orden.
:q cancela sin ejecutar.
El alias m hace lo mismo.
No se puede anidar multi dentro del lote.
Las rutas de touch, code y git siguen siendo la raíz del clone.

## SEGURIDAD
Cada línea del lote pasa por el mismo CommandManager que el prompt normal.
Mismos imports y política SEC.
Comando de sistema. Solo stdlib y moslib.

## VÉASE TAMBIÉN
m, touch, code, git, help