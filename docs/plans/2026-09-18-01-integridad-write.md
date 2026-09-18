# Integridad SHA-256 + write en multi

**Estado:** En curso  
**Rama:** campania/integridad-write

## Objetivo
Todo fichero tracked tiene hash. Arranque y tests contrastan.
write/w solo en multi: hash en la 1ª línea, Base64, restore si no cuadra.
docgen y update mantienen los manifiestos.
Cuando write funcione, el tope 120 sigue con este método.

## Orden
1. Rama y este plan
2. moslib/core/integridad.py
3. write_b64.py + commands/write.py + w.py + gancho multi
4. commands/hash.py + commands/integridad.py (aceptar, recargar, estado, sembrar)
5. update.py: tras pull, copia repo → .mos
6. Arranque + test_integridad
7. docgen _escribir → registrar
8. AGENTS.md + AI_ONBOARDING + man
9. Prueba real: un fichero del tope 120 con write
10. Merge cuando el ritual se use en serie

## Fuera de alcance
Firma, TPM, antimailware serio.