# Lote write + generate

Anexo de metodologia IA. El hash es del fichero en claro.

## Dentro de MOS
Comando m o multi.
Pegas el bloque.
Linea sola :e ejecuta. :q cancela.
Forma:
write <ruta>
<sha256>
[prefijo]payload
.
docgen generate <id>

## Fuera de MOS
./write.sh lanza el mismo multi.
Mismo bloque y mismo :e.
No emular el lote en bash.

## Prefijos
sin prefijo = Base64
gz: gzip+b64
xz: lzma+b64
b85: ascii85
gzb85: gzip+ascii85
xzb85: lzma+ascii85
Elegir el mas corto que el decoder ya tenga.