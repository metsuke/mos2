# AGENTS

## Norma de trabajo

Fuente = tupla o json. MD y HTML se generan. write solo en multi o write.sh. Lote: ruta, sha256, payload gz a 80 columnas, punto, :e. Base64 plano solo tras CRC. multi imprime !!! y sumario. :s avanza un paso. ;s y ;e equivalen. Ningun lote lleva una linea que sea ella sola un comando de sistema (update, dev, exit). tope 120 lineas en moslib. No avanzar producto sobre main.

## Ritual write

Un fichero por write. Hash canónico en la primera linea del payload. Si NO COINCIDE no se toca el destino. Tras OK, code abre el fichero. write.sh lanza el multi real.

## Integridad

Manifiesto repo y copia local. Un fallo de contenido impide arrancar. arreglar_integridad.sh es emergencia consciente. write registra el hash al aplicar.

## Ramas

Trabajo en rama. publicar sube la rama. consolidar a main es humano y ff-only. En lotes no se escribe una linea que sea update ni dev.

## Avance

:s es el siguiente paso. ;s equivale. Un paso = un lote corto. Ficheros enteros. gz por defecto. Tras write o tupla generate, docgen va en el mismo lote si hace falta regenerar.

## Tope de lineas

Ningun .py de moslib/core ni moslib/commands supera 120 lineas. test 120 lista y cuenta; no bloquea. Si se pasa, se trocea con fachada delgada.

## Salida en el chat

Antes y despues de cada bloque de texto hay una linea en blanco. El lote va entero en un solo bloque. Payload a 80 columnas.
