# Ritual write, multi y write.sh

Norma de IA. Hash del fichero en claro. Probado: multi dentro de MOS y ./write.sh fuera.

## Dentro
m o multi. Pegar bloque. Linea sola :e ejecuta. :q cancela. No parsear hasta :e.

## Fuera
./write.sh lanza el mismo multi. Mismo bloque. chmod +x write.sh. Nunca emular el lote en bash.

## Lote
write <ruta>
<sha256>
[gz:|xz:|b85:|gzb85:|xzb85:]payload
.
docgen index add <id> <rel>
docgen generate <id>

## Integridad
Si MOS no arranca: ./arreglar_integridad.sh (30s, luego ./mos2.sh). No es uso diario.