#!/usr/bin/env bash
# write.sh — mini-multi fuera de MOS. write / hash / b64 / .  y el resto del lote.
# Uso: ./write.sh   luego :e o ;e  |  :q cancela
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
echo "[write.sh] Pega el lote. :e ejecuta  |  :q cancela  |  ;e ;q valen."
LOTE=()
while IFS= read -r linea || true; do
  s="${linea#"${linea%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  [ -z "$s" ] && continue
  meta="$s"
  case "$meta" in
    \;*) meta=":${meta:1}" ;;
  esac
  ml="$(printf '%s' "$meta" | tr '[:upper:]' '[:lower:]')"
  case "$ml" in
    :q) echo "[write.sh] Cancelado."; exit 0 ;;
    :e|:w) break ;;
    *) LOTE+=("$s"); echo "[write.sh] + $s" ;;
  esac
done

aplicar() {
  local rel="$1" esperado="$2" b64="$3" tmp real
  esperado="$(printf '%s' "$esperado" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')"
  esperado="${esperado#sha256:}"
  esperado="${esperado#esperado:}"
  if [ "${#esperado}" -ne 64 ]; then
    echo "[write.sh] FAIL $rel: hash no es sha256 hex"
    return 1
  fi
  tmp="$(mktemp)"
  printf '%s' "$b64" | base64 -d >"$tmp" 2>/dev/null || { echo "[write.sh] FAIL $rel: base64"; rm -f "$tmp"; return 1; }
  if command -v shasum >/dev/null 2>&1; then
    real="$(shasum -a 256 "$tmp" | awk '{print $1}')"
  else
    real="$(sha256sum "$tmp" | awk '{print $1}')"
  fi
  if [ "$real" != "$esperado" ]; then
    echo "[write.sh] FAIL $rel esperado=$esperado real=$real"
    rm -f "$tmp"
    return 1
  fi
  mkdir -p "$(dirname "$ROOT/$rel")"
  cp "$tmp" "$ROOT/$rel"
  rm -f "$tmp"
  echo "[write.sh] OK $rel $real"
  python3 -c "from moslib.core.integridad import registrar; print(registrar('$rel'))" 2>/dev/null || \
    echo "[write.sh] aviso: no se pudo registrar integridad."
}

i=0
n=${#LOTE[@]}
while [ "$i" -lt "$n" ]; do
  line="${LOTE[$i]}"
  i=$((i + 1))
  set -- $line
  cmd="${1:-}"
  [ "$cmd" = "w" ] && cmd="write"
  if [ "$cmd" != "write" ]; then
    echo "[write.sh] $line"
    bash -lc "$line" || true
    continue
  fi
  rel="${2:-}"
  [ -z "$rel" ] && { echo "[write.sh] write sin ruta"; continue; }
  [ "$i" -ge "$n" ] && { echo "[write.sh] $rel sin hash"; continue; }
  esperado="${LOTE[$i]}"
  i=$((i + 1))
  b64=""
  while [ "$i" -lt "$n" ]; do
    piece="${LOTE[$i]}"
    i=$((i + 1))
    [ "$piece" = "." ] && break
    b64="${b64}${piece}"
  done
  aplicar "$rel" "$esperado" "$b64" || true
done
echo "[write.sh] Lote terminado."
