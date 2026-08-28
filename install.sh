#!/bin/bash
# =============================================
# install.sh - Instalación cross-platform de MetsuOS
# =============================================

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR" || {
    echo "Error: No se pudo cambiar al directorio del script: $SCRIPT_DIR"
    exit 1
}

# --- Guard WSL: no ejecutar desde /mnt/<letra>/ (disco Windows) ---
is_wsl() {
    if [ -n "${WSL_DISTRO_NAME:-}" ]; then
        return 0
    fi
    if [ -r /proc/version ] && grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
        return 0
    fi
    return 1
}

path_on_windows_mount() {
    case "$1" in
        /mnt/[a-zA-Z]/*|/mnt/[a-zA-Z]) return 0 ;;
        *) return 1 ;;
    esac
}

if is_wsl && path_on_windows_mount "$SCRIPT_DIR"; then
    echo "Error: MetsuOS en WSL no debe ejecutarse desde un clone bajo /mnt/..."
    echo "  Ruta actual: $SCRIPT_DIR"
    echo ""
    echo "Eso provoca venv rotos, CRLF en scripts y confusión entre clones."
    echo "Usa un clone en el filesystem Linux, por ejemplo:"
    echo "  git clone <url-del-repo> \"\$HOME/mos2\""
    echo "  cd \"\$HOME/mos2\""
    echo "  ./install.sh"
    echo "  ./mos2.sh"
    echo ""
    echo "Detalle: docs/ENVIRONMENTS.md (perfil windows/wsl)."
    exit 1
fi

echo "Iniciando despliegue de entorno mos2..."

OS_NAME="$(uname -s 2>/dev/null || echo unknown)"
case "$OS_NAME" in
    Linux*)   ENV_LABEL="linux/native-or-wsl" ;;
    Darwin*)  ENV_LABEL="macos/native" ;;
    MINGW*|MSYS*|CYGWIN*) ENV_LABEL="windows/git-bash" ;;
    *)        ENV_LABEL="$OS_NAME" ;;
esac
echo "Entorno detectado: $ENV_LABEL"

# --- Resolver Poetry (misma política que mos2.sh) ---
resolve_poetry() {
    local is_windows=0
    case "$(uname -s 2>/dev/null || echo unknown)" in
        MINGW*|MSYS*|CYGWIN*) is_windows=1 ;;
    esac

    if [[ "$is_windows" -eq 1 ]]; then
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
        if command -v poetry.exe >/dev/null 2>&1 && poetry.exe --version >/dev/null 2>&1; then
            echo "poetry.exe"
            return 0
        fi
        if command -v poetry >/dev/null 2>&1 && poetry --version >/dev/null 2>&1; then
            echo "poetry"
            return 0
        fi
        return 1
    fi

    if command -v poetry >/dev/null 2>&1 && poetry --version >/dev/null 2>&1; then
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
    echo "Error: No se pudo encontrar Poetry ($ENV_LABEL)."
    echo "Se probaron: py -m poetry, python -m poetry, python3 -m poetry, poetry.exe, poetry"
    echo "Instálalo con: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "Poetry resuelto como: $POETRY_CMD"

eval "$POETRY_CMD config virtualenvs.in-project true"
eval "$POETRY_CMD install"

ALIAS_NAMES=(
    "python-is-python3"
    "mos2"
    "mos2f"
    "mos2u"
)
ALIAS_CMDS=(
    "alias python='python3'"
    "alias mos2='bash \"$SCRIPT_DIR/mos2.sh\" '"
    "alias mos2f='cd \"$SCRIPT_DIR/\"'"
    "alias mos2u='bash \"$SCRIPT_DIR/install.sh\" '"
)
ALIAS_DESCS=(
    "Se asegura de que python y python3 sean equivalentes si no está ya configurado en tu sistema"
    "Ejecuta MetsuOS"
    "Se mueve, mediante 'cd', a la carpeta raiz de MetsuOS"
    "Ejecuta install.sh (actualizar)"
)

echo "================================================="
echo "Configuración de alias de uso rápido (Opcional)"
echo "================================================="
echo "Se pueden instalar los siguientes alias en tu sistema para facilitar el uso:"
echo ""

for i in "${!ALIAS_NAMES[@]}"; do
    echo "  -> ${ALIAS_NAMES[$i]}"
    echo "     ${ALIAS_DESCS[$i]}"
    echo "     ${ALIAS_CMDS[$i]}"
    echo ""
done

read -p "¿Deseas añadir estos alias a tu perfil? (s/N): " user_response

case "$user_response" in
    [sS]|[sS][iI]|[yY]|[yY][eE][sS])
        TARGET_FILES=()
        CMD_TO_COPY=""

        case "$OS_NAME" in
            Darwin*)
                TARGET_FILES+=("$HOME/.bash_profile")
                CMD_TO_COPY="source ~/.bash_profile"
                ;;
            MINGW*|CYGWIN*|MSYS*)
                TARGET_FILES+=("$HOME/.bash_profile" "$HOME/.bashrc")
                CMD_TO_COPY="source ~/.bash_profile"

                if command -v powershell.exe >/dev/null 2>&1; then
                    echo ""
                    echo "Entorno Windows/Git-Bash: configurando PowerShell (opcional)..."
                    WIN_SCRIPT_DIR=$(pwd -W 2>/dev/null || pwd)
                    PS_PROFILE=$(powershell.exe -NoProfile -NonInteractive -Command 'Write-Host $PROFILE' | tr -d '\r')

                    if [ -n "$PS_PROFILE" ]; then
                        BASH_PS_PROFILE=$(cygpath -u "$PS_PROFILE" 2>/dev/null || echo "$PS_PROFILE")
                        mkdir -p "$(dirname "$BASH_PS_PROFILE")"
                        touch "$BASH_PS_PROFILE"

                        echo "" >> "$BASH_PS_PROFILE"
                        echo "# Alias instalados por install.sh (MetsuOS)" >> "$BASH_PS_PROFILE"

                        if ! grep -q "function mos2 " "$BASH_PS_PROFILE"; then
                            echo "function mos2 { & \"C:\Program Files\Git\bin\bash.exe\" \"$WIN_SCRIPT_DIR/mos2.sh\" }" >> "$BASH_PS_PROFILE"
                            echo "function mos2u { & \"C:\Program Files\Git\bin\bash.exe\" \"$WIN_SCRIPT_DIR/install.sh\" }" >> "$BASH_PS_PROFILE"
                            echo "function mos2f { Set-Location \"$WIN_SCRIPT_DIR\" }" >> "$BASH_PS_PROFILE"
                            echo "  Funciones instaladas en PowerShell."
                        else
                            echo "  Las funciones de PowerShell ya existen. Se omiten."
                        fi
                    fi
                fi
                ;;
            *)
                TARGET_FILES+=("$HOME/.bashrc")
                CMD_TO_COPY="source ~/.bashrc"
                ;;
        esac

        if command -v zsh >/dev/null 2>&1 || [ -f "$HOME/.zshrc" ]; then
            TARGET_FILES+=("$HOME/.zshrc")
            if [[ "$SHELL" == *"zsh"* ]]; then
                CMD_TO_COPY="source ~/.zshrc"
            fi
        fi

        for RC_FILE in "${TARGET_FILES[@]}"; do
            if [ ! -f "$RC_FILE" ]; then
                touch "$RC_FILE"
            fi

            echo ""
            echo "Instalando alias en $RC_FILE..."
            echo "" >> "$RC_FILE"
            echo "# Alias instalados por install.sh (MetsuOS)" >> "$RC_FILE"

            for i in "${!ALIAS_NAMES[@]}"; do
                if grep -q "alias ${ALIAS_NAMES[$i]}=" "$RC_FILE" 2>/dev/null; then
                    echo "  El alias '${ALIAS_NAMES[$i]}' ya existe. Se omite."
                else
                    echo "${ALIAS_CMDS[$i]}" >> "$RC_FILE"
                    echo "  Alias '${ALIAS_NAMES[$i]}' instalado."
                fi
            done
        done

        echo ""
        echo "Alias instalados en los perfiles detectados."
        echo ""

        if [[ "$OS_NAME" == MINGW* ]] || [[ "$OS_NAME" == CYGWIN* ]] || [[ "$OS_NAME" == MSYS* ]]; then
            echo "Para usar en PowerShell:  . \$PROFILE"
            echo "Para usar en esta terminal (Bash):  $CMD_TO_COPY"
        else
            echo "Para usarlos ahora:  $CMD_TO_COPY"
        fi
        echo "(O cierra y abre una nueva terminal)."
        echo "================================================="
        ;;
    *)
        echo "Saltando la instalación de alias."
        ;;
esac

echo ""
echo "Entorno mos2 (MetsuOS) listo para su uso."