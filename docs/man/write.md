# write

## NOMBRE
write - escribe un fichero del clone con hash y Base64 (solo multi)

## SINOPSIS

- write <ruta>
- w <ruta>

## DESCRIPCION
Solo funciona dentro de multi o m.
Lote: write RUTA, linea sha256 hex, Base64 del fichero entero, linea con un punto.
Si el hash no coincide no se toca el destino.
Tras OK abre code sobre la ruta.
Alias: w.
Fuera de MOS usar ./write.sh con el mismo lote.

## SEGURIDAD
Ruta relativa a la raiz del clone.
No escribe si el SHA-256 no coincide.
Comando de sistema. Solo stdlib y moslib.

## VEASE TAMBIEN
multi, m, w, code, hash