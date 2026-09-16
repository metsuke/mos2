# docgen

## NOMBRE
docgen – ingesta y regenera la documentación de MetsuOS

## SINOPSIS
docgen list
docgen generate man|specs|pages|all|<id>
docgen req list|add|set|rm
docgen area list|add|set|rm
docgen ingest man|specs|pages|reqs|all
docgen backup <id>
docgen backup-list <id>

## DESCRIPCIÓN
La fuente de verdad es JSON en docs/docgen/.
generate pinta markdown y HTML en docs/docgen/html/.
ingest solo primera vez o recuperación; generate no ingerir.
Requisitos: un JSON por id en docs/docgen/reqs/.
Áreas: CRUD sobre docs/docgen/areas.json.
El SRS se pinta con una tabla por área.

## EJEMPLOS
docgen area list
docgen req list
docgen req add REQ-CMD-021 texto del requisito
docgen generate 02-srs
docgen generate man-docgen

## SEGURIDAD
Comando de sistema. Solo stdlib y moslib.

## VÉASE TAMBIÉN
docs, man, help

## HELP DEL COMANDO
Uso: docgen generate ... | docgen req list|add|set|rm | docgen area list|add|set|rm | docgen ingest ... (recuperación).
