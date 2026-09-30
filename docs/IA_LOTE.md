# IA_LOTE

## Regla

Un lote es un bloque que multi o write.sh ejecuta al :e. Maximo tres ficheros write si son cortos; si no, uno. docgen del mismo destino va en el mismo lote. Ninguna linea del lote es un comando de sistema suelto.

## Forma write

write ruta / sha256 / payload gz a 80 columnas / linea con un punto. gz por defecto. Base64 solo si ese fichero dio CRC.

## Fallos

Al cerrar: sumario ok=N y !!! fallos=M. Cada fallo lleva !!!. write devuelve 1 si el payload no aplica.
