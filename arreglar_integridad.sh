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
python3 - <<'ENDPY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))
from moslib.core.integridad import local_path, repo_path, sha256_fichero
from moslib.core.integridad_map import _escribir, _leer

root = Path.cwd()
repo = repo_path()
if not repo.is_file():
    print("No hay", repo)
    sys.exit(1)
mapa = _leer(repo)
cambiados = 0
quitados = []
for rel in list(mapa):
    if rel in ("schema", "sello"):
        continue
    path = root / rel
    if not path.is_file():
        mapa.pop(rel, None)
        quitados.append(rel)
        continue
    h = sha256_fichero(path)
    if mapa.get(rel) != h:
        mapa[rel] = h
        cambiados += 1
        print("act", rel)
if quitados:
    print("QUITADOS", quitados[:20])
_escribir(repo, mapa)
_escribir(local_path(), mapa)
print("ok rutas", cambiados, "manifiesto", repo)
ENDPY
echo "Arrancando MOS con MOS_INTEGRIDAD=recargar"
if [[ -x ./mos2.sh ]]; then
  exec env MOS_INTEGRIDAD=recargar ./mos2.sh
fi
if [[ -x ./mos2 ]]; then
  exec env MOS_INTEGRIDAD=recargar ./mos2
fi
if command -v mos2 >/dev/null 2>&1; then
  exec env MOS_INTEGRIDAD=recargar mos2
fi
exec env MOS_INTEGRIDAD=recargar poetry run python rootfs/bin/mos.py
