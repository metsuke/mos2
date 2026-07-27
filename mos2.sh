#!/bin/bash
# =============================================
# launch-metsuos.sh - Lanzador seguro de MetsuOS
# =============================================

# === 1. Cambiar al directorio del script ===
# Obtiene la ruta absoluta del propio script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cambia al directorio del script
cd "$SCRIPT_DIR" || {
    echo "❌ Error: No se pudo cambiar al directorio del script: $SCRIPT_DIR"
    exit 1
}

echo "✅ Directorio actual: $(pwd)"

# === 2. Verificar que existe Poetry ===
if ! command -v poetry &> /dev/null; then
    echo "❌ Error: Poetry no está instalado o no está en el PATH."
    echo "   Instálalo con: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# === 3. Verificar que existe el archivo principal ===
if [[ ! -f "rootfs/bin/mos.py" ]]; then
    echo "❌ Error: No se encuentra rootfs/bin/mos.py"
    echo "   Asegúrate de estar en la raíz correcta del proyecto MetsuOS."
    exit 1
fi

# === 4. Lanzar MetsuOS ===
echo "🚀 Lanzando MetsuOS a través de Poetry..."
poetry run python rootfs/bin/mos.py "$@"