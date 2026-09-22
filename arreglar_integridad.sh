#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "ADVERTENCIA: reescribe hashes del manifiesto al contenido ACTUAL del clone."
echo "No lo uses si no reconoces los cambios, hay un clone ajeno o sospechas de toqueteo."
echo "Ctrl-C para abortar."
SEGS=30
for ((i=1; i<=SEGS; i++)); do
  pct=$((i * 100 / SEGS))
  filled=$((i * 28 / SEGS))
  bar=""
  for ((k=0; k<28; k++)); do
    if ((k < filled)); then bar+="█"; else bar+="░"; fi
  done
  printf "\r[arreglar] %s %s/%s %s%% espera" "$bar" "$i" "$SEGS" "$pct"
  sleep 1
done
printf "\n"
python3 - <<'PY'
import hashlib, json, sys
from pathlib import Path
root = Path.cwd()
mans = []
for p in root.rglob("integridad.json"):
    if ".venv" in p.parts or "docgen/man/integridad.json" in p.as_posix():
        continue
    mans.append(p)
if not mans:
    print("No hay integridad.json")
    sys.exit(1)
raros = []
for man in mans:
    data = json.loads(man.read_text(encoding="utf-8"))
    dest = data.get("archivos") if isinstance(data.get("archivos"), dict) else data.get("files")
    if not isinstance(dest, dict):
        dest = data
    faltan = []
    for rel, _viejo in list(dest.items()):
        if not isinstance(rel, str):
            continue
        path = root / rel
        if not path.is_file():
            faltan.append(rel)
            continue
        dest[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    if faltan:
        raros.extend(faltan)
        print("FALTAN", man, faltan[:20])
    man.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sello = man.with_name(man.name + ".sha256")
    sello.write_text(hashlib.sha256(man.read_bytes()).hexdigest() + "\n", encoding="utf-8")
    print("actualizado", man)
if raros:
    print("ABORTA: hay rutas del manifiesto que no existen:", len(raros))
    sys.exit(2)
print("OK")
PY
echo "Arrancando MOS con MOS_INTEGRIDAD=recargar"
if [[ -x ./mos2.sh ]]; then
  exec env MOS_INTEGRIDAD=recargar ./mos2.sh
fi
if [[ -x ./mos2 ]]; then
  exec env MOS_INTEGRIDAD=recargar ./mos2
fi
exec env MOS_INTEGRIDAD=recargar poetry run python rootfs/bin/mos.py
