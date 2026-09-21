# 11-INTEGRIDAD Control de hashes del clone

**Version:** 1.0
**Estado:** Normativo SEC
**Padre:** 04-SEC
**Reqs:** REQ-SEC-010 a REQ-SEC-015, REQ-CMD-021 a 024

## Proposito
Define el control de integridad del arbol del clone. Complementa 04-SEC (imports/AST). No lo sustituye.

## Que se protege
Todo path que viaja en git: py, sh, md, json, html generado, write.sh, install, manifiestos.

## Que no promete
No es firma de autor. No resiste a quien controla clone, .mos y las herramientas de hash a la vez. Detecta error de pegado y malware no especializado.

## Manifiesto dual y sello
Repo: integridad.json + integridad.json.sha256.
Local: copia en .mos.
Si falta la local al arrancar, se copia la del repo.
Editar el JSON a mano rompe el sello: fallo grave.

## Clases de fallo
Bloquean arranque: contenido, falta, sello roto, falta sello.
Avisan: eol, sello-eol, desfase-local.

## Quien puede registrar un hash
write en multi, write.sh fuera de MOS, registrar_destino tras docgen generate, integridad aceptar RUTA, update al traer el manifiesto del repo.
No existe aceptar todo.

## Write
Lote: write RUTA, sha256, base64, punto, :e.
Hash distinto: no se toca el destino.
Tras OK abre code.
Maximo 3 write por lote.

## Emergencia
MOS_INTEGRIDAD=recargar o integridad recargar. Solo si MOS no arranca por manifiesto local viejo.

## Autoridad
Si choca con 04-SEC en imports/AST, prevalece 04-SEC. Si choca en hashes/write, prevalece este documento.