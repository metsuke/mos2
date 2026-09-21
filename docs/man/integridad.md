# integridad

## NOMBRE
integridad - manifiesto de hashes del clone y copia local

## SINOPSIS

- integridad estado
- integridad sembrar
- integridad aceptar <ruta>
- integridad recargar

## DESCRIPCION
Comprueba SHA-256 de los paths tracked.
Subcomandos: sembrar, aceptar RUTA, recargar.
aceptar solo una ruta.
recargar sustituye la copia .mos por la del repo.
El arranque copia solo si falta la local.

## SEGURIDAD
contenido y falta bloquean. avisos eol no bloquean.
Comando de sistema. Solo stdlib y moslib.

## VEASE TAMBIEN
write, hash, update, test