#!/bin/bash
echo "🚀 Iniciando despliegue de entorno mos2..."
# Asegurar entorno local estanco
poetry config virtualenvs.in-project true
# Instalación silenciosa
poetry install


# 1. Obtener la ruta absoluta del script actual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_PATH="$SCRIPT_DIR/install.sh"

# 2. Definir los alias
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
echo "🛠️  Configuración de alias de uso rapido (Opcional)"
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

if [[ ! "$user_response" =~ ^[sS]$ ]]; then
    echo "Saltando la instalación de alias. ¡Continuamos!"
else
    # 5. Determinar archivos de configuración según entorno y shells disponibles
    OS_NAME=$(uname -s)
    TARGET_FILES=()

    # Añadir archivo correspondiente a Bash
    if [ "$OS_NAME" = "Darwin" ]; then
        TARGET_FILES+=("$HOME/.bash_profile")
    else
        TARGET_FILES+=("$HOME/.bashrc")
    fi

    # Detectar si Zsh está presente (buscando el comando o el archivo de configuración)
    # y añadirlo silenciosamente a la lista de destinos
    if command -v zsh >/dev/null 2>&1 || [ -f "$HOME/.zshrc" ]; then
        TARGET_FILES+=("$HOME/.zshrc")
    fi

    # 6. Bucle de instalación: iteramos por todos los archivos detectados
    for RC_FILE in "${TARGET_FILES[@]}"; do
        
        # Si el archivo no existe, lo creamos
        if [ ! -f "$RC_FILE" ]; then 
            touch "$RC_FILE" 
        fi

        echo ""
        echo "Instalando alias en $RC_FILE..."
        
        # Cabecera visual
        echo "" >> "$RC_FILE"
        echo "# Alias instalados por install.sh" >> "$RC_FILE"

        for i in "${!ALIAS_NAMES[@]}"; do
            # Comprobación individual por cada archivo
            if grep -q "alias ${ALIAS_NAMES[$i]}=" "$RC_FILE"; then
                echo "  ⚠️  El alias '${ALIAS_NAMES[$i]}' ya existe. Se omite."
            else
                echo "${ALIAS_CMDS[$i]}" >> "$RC_FILE"
                echo "  ✅ Alias '${ALIAS_NAMES[$i]}' instalado correctamente."
            fi
        done
    done
        
    # 7. Determinar qué comando mostrar al usuario basándonos en su shell actual
    if [[ "$SHELL" == *"zsh"* ]]; then
        CMD_TO_COPY="source ~/.zshrc"
    elif [ "$OS_NAME" = "Darwin" ]; then
        CMD_TO_COPY="source ~/.bash_profile"
    else
        CMD_TO_COPY="source ~/.bashrc"
    fi

    echo ""
    echo "✅ Alias instalados correctamente."
    echo ""
    echo "💡 Para empezar a usarlos INMEDIATAMENTE en esta ventana, copia y pega"
    echo "el siguiente comando (esto recargará tu archivo de configuración):"
    echo ""
    echo "    $CMD_TO_COPY"
    echo ""
    echo "(O alternativamente, simplemente cierra y abre una nueva terminal)."
    echo "================================================="
fi
  
echo ""
echo "✅ Entorno mos2 (MetsuOS) listo para su uso."

