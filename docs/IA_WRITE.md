# IA_WRITE

## Proposito

**Resumen.** write y write.sh escriben con hash y codecs; el MD de este doc se pinta desde tuplas.

## Lote write

**Pasos.** write ruta, hash esperado, payload, punto, :e. write.sh fuera de MOS. Un solo bloque de texto.

## Codecs

**Prefijos.** gzb85 gz xz b85 y combinaciones; se elige el payload mas corto.

## Salida IA bloques

**Linea en blanco.** Obligatorio: una linea en blanco inmediatamente ANTES y DESPUES de cualquier bloque de texto copiable. Nada pegado al fence de apertura ni al de cierre.

## Sumario de errores

Al cerrar el lote, multi imprime sumario ok=N y !!! fallos=M. Cada fallo lleva prefijo !!!. execute devuelve 0 o None si ok, 1 o False si fallo. Comando inexistente cuenta como fallo.
