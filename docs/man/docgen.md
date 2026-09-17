# docgen

## NOMBRE
docgen – ingesta y regenera la documentación de MetsuOS

## SINOPSIS

- docgen list
- docgen generate man|specs|pages|all|<id>
- docgen req list|add|set|rm
- docgen area list|add|set|rm
- docgen plan list|add|set|rm
- docgen ingest man|specs|pages|reqs|plans|all|<id>
- docgen backup <id>
- docgen backup-list <id>

## DESCRIPCIÓN
La fuente de verdad es JSON en docs/docgen/.
generate pinta markdown y HTML en docs/docgen/html/.
ingest solo primera vez o recuperación; generate no ingerir.
Requisitos: un JSON por id en docs/docgen/reqs/.
Áreas: CRUD sobre docs/docgen/areas.json.
Planes: un JSON por plan en docs/docgen/plans/. El índice de docs/plans/README.md se pinta con generate plans-readme.
El SRS se pinta con una tabla por área.

## EJEMPLOS

- docgen plan list
- docgen plan add 2026-09-14-01-docgen.md En curso
- docgen plan set 2026-09-14-01-docgen Cerrada
- docgen generate plans-readme
- docgen generate man-docgen

## SEGURIDAD
Comando de sistema. Solo stdlib y moslib.

## VÉASE TAMBIÉN
docs, man, help