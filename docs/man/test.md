# test

## NOMBRE
test – ejecuta la batería de tests de MetsuOS

## SINOPSIS
test [args-pytest...]

## DESCRIPCIÓN
Lanza pytest sobre el proyecto.

Sirve para verificar seguridad, contrato de comandos, loader, usuario y estilo crítico.

Además, MetsuOS ya ejecuta tests al arrancar. Si fallan en el arranque, el shell no inicia.

## OPCIONES
Cualquier argumento adicional se reenvía a pytest cuando la implementación lo permite.

## EJEMPLOS
test
test -q
test tests/test_security.py

## SEGURIDAD
Comando de sistema. No reduce la política de seguridad; la verifica.

## VÉASE TAMBIÉN
update, help, man