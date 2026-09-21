#!/usr/bin/env bash
# Lanza el multi real de MOS, sin emular el lote.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
if command -v poetry >/dev/null 2>&1 && [ -f "$ROOT/pyproject.toml" ]; then
  exec poetry run python -c "from moslib.commands.multi import execute; execute([])"
fi
exec python3 -c "from moslib.commands.multi import execute; execute([])"