# docs

## NOMBRE
docs – consulta la documentación del clone desde MOSh

## SINOPSIS
docs
docs <ruta>

## DESCRIPCIÓN
Uso: docs - Lista documentación (docs/ y README, CHANGELOG, AGENTS, LICENSE). Uso: docs <ruta> - Muestra un fichero permitido (ejemplo: docs README.md, docs A11Y.md)

Uso: docs - Lista documentación (docs/ y README, CHANGELOG, AGENTS, LICENSE). Uso: docs <ruta> - Muestra un fichero permitido (ejemplo: docs README.md, docs A11Y.md)

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
