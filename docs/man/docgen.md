# docgen

## NOMBRE
docgen – ingesta y regenera la documentación de MetsuOS

## SINOPSIS
docgen
docgen list
docgen ingest man|specs|pages|all
docgen ingest <id>
docgen generate man|specs|pages|all
docgen generate <id>
docgen backup <id>
docgen backup-list <id>

## DESCRIPCIÓN
Regenera markdown publicado a partir de json + plantilla implícita
(secciones) + scan de help() en las páginas man.

La ingesta elige el origen más largo entre el fichero actual y los
backups de docs/docgen/backup/<id>/. Si falta el preámbulo (versión,
baseline, estado, documentos relacionados), lo busca en backups
de más reciente a más antiguo.

Los ficheros sin encabezados ## (por ejemplo LICENSE) se guardan
enteros en cuerpo_completo y se vuelven a escribir iguales.

generate hace backup del destino antes de pisarlo. Si el texto nuevo
(sin contar el número de versión) no coincide con el último backup,
incrementa **Versión del documento**.

## EJEMPLOS
docgen list
docgen ingest man
docgen generate man
docgen ingest 00-overview
docgen generate 00-overview
docgen ingest all
docgen generate all

## SEGURIDAD
Comando de sistema. Solo stdlib y moslib. No envía red.

## VÉASE TAMBIÉN
docs, man, help

## HELP DEL COMANDO
Uso: docgen generate man|specs|pages|all|<id> - Pinta markdown desde docs/docgen JSON. ingest solo primera vez o recuperación.
