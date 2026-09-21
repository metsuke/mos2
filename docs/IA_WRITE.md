# Ritual write y multi para IA

Fichero entero. Hash SHA-256 del contenido en claro. Payload Base64 o gz:+Base64(gzip). generate en el mismo lote.

## Lote
write ruta
hash
[gz:]base64
.
docgen generate <id>
:e

El hash es del fichero descomprimido. gz: solo si el receptor ya decodifica gzip (write_b64._decodificar). Si no acorta, Base64 plano.

## Donde
Dentro: multi/m. Fuera: ./write.sh lanza multi real. Maximo tres writes. write registra integridad.