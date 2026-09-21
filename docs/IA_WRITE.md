# Ritual write y multi para IA

Fichero entero. SHA-256 del contenido en claro. Payload: plano b64 o prefijo gz:/xz:/b85:/gzb85:/xzb85:. generate en el mismo lote. La IA elige el payload mas corto que el receptor ya decodifique.

## Lote
write ruta
hash
payload
.
docgen generate <id>
:e

## Prefijos
sin prefijo = Base64 del fichero.
gz: gzip+b64
xz: lzma+b64
b85: ascii85 del fichero
gzb85: gzip+ascii85
xzb85: lzma+ascii85
CRC/gzip roto = payload cortado; repetir en b64 plano.

## Donde
multi/m o write.sh que lanza multi. Maximo tres writes. write registra integridad. Varios codecs no sustituyen el hash.