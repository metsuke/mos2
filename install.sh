#!/bin/bash
echo "🚀 Iniciando despliegue de entorno mos2..."

# Asegurar entorno local estanco
poetry config virtualenvs.in-project true
# Instalación silenciosa
poetry install

# 1. Obtener la ruta absoluta del script actual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# 2. Definir los alias para Bash
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

# 3. Mostrar la información al usuario
echo "================================================="
echo "🛠️  Configuración de alias de uso rápido (Opcional)"
echo "================================================="
echo "Se pueden instalar los siguientes alias en tu sistema para facilitar el uso:"
echo ""

for i in "${!ALIAS_NAMES[@]}"; do
    echo "  👉 ${ALIAS_NAMES[$i]}"
    echo "     ${ALIAS_DESCS[$i]}"
    echo "     ${ALIAS_CMDS[$i]}"
    echo ""
done

# 4. Preguntar al usuario
read -p "¿Deseas añadir estos alias a tu perfil? (s/N): " user_response

case "$user_response" in 
    [sS]|[sS][iI]|[yY]|[yY][eE][sS])
        
        # 5. Determinar entorno
        OS_NAME=$(uname -s)
        TARGET_FILES=()
        CMD_TO_COPY=""

        case "$OS_NAME" in
            Darwin*)    
                TARGET_FILES+=("$HOME/.bash_profile") 
                CMD_TO_COPY="source ~/.bash_profile"
                ;;
            MINGW*|CYGWIN*|MSYS*) 
                # Entorno Windows detectado
                TARGET_FILES+=("$HOME/.bash_profile" "$HOME/.bashrc")
                CMD_TO_COPY="source ~/.bash_profile"
                
                # INTEGRACIÓN CON POWERSHELL
                if command -v powershell.exe >/dev/null 2>&1; then
                    echo ""
                    echo "⚙️  Entorno Windows detectado. Configurando PowerShell..."
                    
                    # Extraer la ruta nativa de Windows
                    WIN_SCRIPT_DIR=$(pwd -W 2>/dev/null || pwd)
                    
                    # Preguntar a PowerShell dónde está el $PROFILE
                    PS_PROFILE=$(powershell.exe -NoProfile -NonInteractive -Command 'Write-Host $PROFILE' | tr -d '\r')
                    
                    if [ -n "$PS_PROFILE" ]; then
                        BASH_PS_PROFILE=$(cygpath -u "$PS_PROFILE" 2>/dev/null || echo "$PS_PROFILE")
                        
                        mkdir -p "$(dirname "$BASH_PS_PROFILE")"
                        touch "$BASH_PS_PROFILE"
                        
                        echo "" >> "$BASH_PS_PROFILE"
                        echo "# Alias instalados por install.sh" >> "$BASH_PS_PROFILE"
                        
                        # Escribir funciones nativas de PowerShell apuntando a Git Bash
                        if ! grep -q "function mos2 " "$BASH_PS_PROFILE"; then
                            echo "function mos2 { & \"C:\Program Files\Git\bin\bash.exe\" \"$WIN_SCRIPT_DIR/mos2.sh\" }" >> "$BASH_PS_PROFILE"
                            echo "function mos2u { & \"C:\Program Files\Git\bin\bash.exe\" \"$WIN_SCRIPT_DIR/install.sh\" }" >> "$BASH_PS_PROFILE"
                            echo "function mos2f { Set-Location \"$WIN_SCRIPT_DIR\" }" >> "$BASH_PS_PROFILE"
                            echo "  ✅ Funciones instaladas en PowerShell ($PS_PROFILE)."
                        else
                            echo "  ⚠️  Las funciones de PowerShell ya existen. Se omiten."
                        fi
                    fi
                fi
                ;;
            *)          
                TARGET_FILES+=("$HOME/.bashrc") 
                CMD_TO_COPY="source ~/.bashrc"
                ;;
        esac

        # Añadir soporte para Zsh si existe
        if command -v zsh >/dev/null 2>&1 || [ -f "$HOME/.zshrc" ]; then
            TARGET_FILES+=("$HOME/.zshrc")
            if [[ "$SHELL" == *"zsh"* ]]; then
                CMD_TO_COPY="source ~/.zshrc"
            fi
        fi

        # 6. Bucle de instalación para Bash/Zsh
        for RC_FILE in "${TARGET_FILES[@]}"; do
            if [ ! -f "$RC_FILE" ]; then 
                touch "$RC_FILE" 
            fi

            echo ""
            echo "Instalando alias en $RC_FILE..."
            echo "" >> "$RC_FILE"
            echo "# Alias instalados por install.sh" >> "$RC_FILE"

            for i in "${!ALIAS_NAMES[@]}"; do
                if grep -q "alias ${ALIAS_NAMES[$i]}=" "$RC_FILE"; then
                    echo "  ⚠️  El alias '${ALIAS_NAMES[$i]}' ya existe. Se omite."
                else
                    echo "${ALIAS_CMDS[$i]}" >> "$RC_FILE"
                    echo "  ✅ Alias '${ALIAS_NAMES[$i]}' instalado correctamente."
                fi
            done
        done
        
        echo ""
        echo "✅ Alias instalados correctamente en todos los perfiles detectados."
        echo ""
        
        if [[ "$OS_NAME" == MINGW* ]] || [[ "$OS_NAME" == CYGWIN* ]] || [[ "$OS_NAME" == MSYS* ]]; then
            echo "💡 Para usar en PowerShell, ejecuta:  . \$PROFILE"
            echo "💡 Para usar en esta terminal (Bash), ejecuta:  $CMD_TO_COPY"
        else
            echo "💡 Para empezar a usarlos INMEDIATAMENTE, ejecuta:"
            echo "    $CMD_TO_COPY"
        fi
        
        echo "(O alternativamente, cierra y abre una nueva terminal)."
        echo "================================================="
        ;;
    *)
        echo "Saltando la instalación de alias. ¡Continuamos!"
        ;;
esac
  
echo ""
echo "✅ Entorno mos2 (MetsuOS) listo para su uso."