# multi

## NOMBRE
multi - pega un lote de comandos y luego los ejecuta

## SINOPSIS

- multi
- m

## DESCRIPCION
Entra en prompt multi>. Se pegan comandos, uno por linea.
No se ejecutan al pegar.
:e o :w lanza el lote en orden. ;e y ;q se aceptan; el canonico es :e y :q.
:q cancela.
Alias: m.
write solo se admite dentro de este lote.
Maximo tres write por lote si los ficheros son pequenos.

## SEGURIDAD
Cada linea pasa por el mismo CommandManager que el prompt normal.
Comando de sistema. Solo stdlib y moslib.

## VEASE TAMBIEN
m, write, w, code, git, touch