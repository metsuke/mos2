#!/bin/bash
# =============================================
# mos2.sh - Lanzador cross-platform de MetsuOS
# =============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || {
    echo "Error: No se pudo cambiar al directorio del script: $SCRIPT_DIR"
    exit 1
}

echo "Directorio actual: $(pwd)"

# --- Detección de entorno (informativa) ---
OS_NAME="$(uname -s 2>/dev/null || echo unknown)"
case "$OS_NAME" in
    Linux*)   ENV_LABEL="Linux" ;;
    Darwin*)  ENV_LABEL="macOS" ;;
    MINGW*|MSYS*|CYGWIN*) ENV_LABEL="Windows/Git-Bash" ;;
    *)        ENV_LABEL="$OS_NAME" ;;
esac
echo "Entorno detectado: $ENV_LABEL"

# --- Resolver Poetry de forma portable ---
# En Windows/Git Bash: priorizar poetry.exe y "python -m poetry"
# (el script "poetry" sin extensión suele dar Permission denied)
resolve_poetry() {
    local is_windows=0
    case "$(uname -s 2>/dev/null || echo unknown)" in
        MINGW*|MSYS*|CYGWIN*) is_windows=1 ;;
    esac

    if [[ "$is_windows" -eq 1 ]]; then
        if command -v poetry.exe >/dev/null 2>&1; then
            echo "poetry.exe"
            return 0
        fi
        if command -v py >/dev/null 2>&1 && py -m poetry --version >/dev/null 2>&1; then
            echo "py -m poetry"
            return 0
        fi
        if command -v python >/dev/null 2>&1 && python -m poetry --version >/dev/null 2>&1; then
            echo "python -m poetry"
            return 0
        fi
        if command -v python3 >/dev/null 2>&1 && python3 -m poetry --version >/dev/null 2>&1; then
            echo "python3 -m poetry"
            return 0
        fi
        # Último recurso en Windows (puede fallar con Permission denied)
        if command -v poetry >/dev/null 2>&1; then
            echo "poetry"
            return 0
        fi
        return 1
    fi

    # Linux / macOS
    if command -v poetry >/dev/null 2>&1; then
        echo "poetry"
        return 0
    fi
    if command -v python3 >/dev/null 2>&1 && python3 -m poetry --version >/dev/null 2>&1; then
        echo "python3 -m poetry"
        return 0
    fi
    if command -v python >/dev/null 2>&1 && python -m poetry --version >/dev/null 2>&1; then
        echo "python -m poetry"
        return 0
    fi
    return 1
}

POETRY_CMD="$(resolve_poetry || true)"
if [[ -z "$POETRY_CMD" ]]; then
    echo "Error: No se pudo encontrar Poetry en este entorno ($ENV_LABEL)."
    echo "Se probaron: poetry, poetry.exe, python -m poetry, python3 -m poetry, py -m poetry"
    echo "Instálalo con: curl -sSL https://install.python-poetry.org | python3 -"
    echo "En Windows/Git Bash, cierra y abre la terminal tras instalar, o añade Poetry al PATH."
    exit 1
fi

echo "Poetry resuelto como: $POETRY_CMD"

if [[ ! -f "rootfs/bin/mos.py" ]]; then
    echo "Error: No se encuentra rootfs/bin/mos.py"
    echo "   Asegúrate de estar en la raíz correcta del proyecto MetsuOS."
    exit 1
fi

echo "Lanzando MetsuOS a través de Poetry..."
# Eval seguro del comando resuelto (puede ser "poetry.exe" o "py -m poetry")
eval "$POETRY_CMD run python rootfs/bin/mos.py \"\$@\""