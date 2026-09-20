# update

## NOMBRE
update — trae origin/main o una rama de desarrollo

## SINOPSIS

- update
- update dev
- update reiniciar

## DESCRIPCIÓN
Sin argumentos alinea el clon con origin/main (fetch + checkout main + reset --hard). Se niega si el árbol está sucio: publica con dev publicar o limpia.

update dev lista ramas remotas que no son main, pide un número y hace checkout + pull de esa rama para probar en otra máquina.

El código nuevo no entra en la sesión actual. Sal y entra, o update reiniciar.

## OPCIONES
dev — elige rama remota distinta de main.
reiniciar — relanza MOSh sobre el árbol actual.

## EJEMPLOS

- update
- update dev
- update reiniciar

## SEGURIDAD
No avanza main. No hace force-push. Sincroniza integridad local desde el repo.

## VÉASE TAMBIÉN
dev, git, test, version