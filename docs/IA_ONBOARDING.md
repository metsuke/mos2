# Onboarding IA MetsuOS

Leer antes de tocar codigo. Fuente JSON. generate no es ingest.

## Edicion
Dentro: multi/m. Fuera: ./write.sh (el mismo multi). Lote write + hash + payload + punto + docgen generate. Cerrar con :e. Tope 120 lineas. Maximo tres writes por lote.

## Codecs
Hash SHA-256 del claro. Payload: b64, gz:, xz:, b85:, gzb85:, xzb85:. Elegir el mas corto que el decoder tenga.

## Indice
docs/docgen/index.json. docgen index add|set|rm|list. Si generate no escribe, falta el id en el indice.

## Integridad
./arreglar_integridad.sh solo si MOS no arranca. 30s de aviso. Lanza ./mos2.sh con MOS_INTEGRIDAD=recargar. No uso diario.