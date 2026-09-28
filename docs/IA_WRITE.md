# Ritual write, multi y write.sh

Norma de IA. Hash del fichero en claro. Probado: multi dentro de MOS y ./write.sh fuera.

## Dentro
m o multi. Pegar bloque. Linea sola :e ejecuta. :q cancela. No parsear hasta :e.

## Fuera
./write.sh lanza el mismo multi. Mismo bloque. chmod +x write.sh. Nunca emular el lote en bash.

## Lote
write <ruta>
<sha256 64 hex>
gz:payload partido a 80 columnas
.
Prohibido emitir codec con ^C o ^Z (tipico de gzb85). Preferir gz: sobre xz: y b64 plano. multi no se cambia para tragar lineas enormes de contenido; solo rutas pueden ser largas. El chat pone el lote entero en un bloque markdown, con linea en blanco antes y despues.

## Integridad
Si MOS no arranca: ./arreglar_integridad.sh (30s, quita rutas fantasma, luego MOS_INTEGRIDAD=recargar mos2). No es uso diario.