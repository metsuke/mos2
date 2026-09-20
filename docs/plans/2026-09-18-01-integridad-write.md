# Integridad SHA-256 + write en multi

**Estado:** En curso (tope 120 cerrado; falta prueba share/connect y merge)
**Rama:** campania/integridad-write

## Objetivo
Todo fichero tracked tiene hash. Arranque y tests contrastan.
write/w solo en multi: hash en la 1ª línea, Base64, restore si no cuadra.
write abre code al guardar OK. docgen y update mantienen manifiestos.
Tope 120 en moslib: `test 120` lista excesos y no tumba el arranque.

## Hecho
1. Rama, plan, integridad + sello de ambos JSON.
2. write_b64 + write/w + multi (`:e` ejecuta; `;e` solo atajo).
3. hash, integridad aceptar/recargar/estado.
4. update copia integridad repo → local.
5. Arranque bloquea si el hash no cuadra.
6. docgen registra destino al escribir; backups podados (máx. 8).
7. Ritual write usado en serie para trocear moslib ≤120.
8. `test 120` (solo lista; no pytest ni a11y).
9. Tope 120 en moslib cerrado (último: ia_check_share → hechos + fachada).
10. `iarouter share`: diagnóstico original + puente on + publicar + diagnóstico.
11. `iarouter connect`: check_share + ofrecer URL + usar jan (cliente sin Jan local).

## Pendiente antes de main
- Probar share (anfitrión) y connect (cliente) en LAN real.
- Commit/push de lo local no subido.
- Regenerar man/docs de iarouter, write, test, integridad.
- Merge a main cuando el ritual y share/connect estén validados.

## Fuera de alcance
Firma, TPM, antimalware serio.
