#!/bin/bash
# setLocale.sh — solo si el anfitrión está en C/POSIX (caso MOS: "C, C, C").
# Instala y fija es_ES.UTF-8. Pide aceptación. Idempotente en ~/.bashrc.

set -euo pipefail

DESTINO="es_ES.UTF-8"
BASHRC="${HOME}/.bashrc"
EXPORT_LANG="export LANG=${DESTINO}"
EXPORT_ALL="export LC_ALL=${DESTINO}"

es_wsl() {
    if [ -n "${WSL_DISTRO_NAME:-}" ]; then
        return 0
    fi
    if [ -r /proc/version ] && grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
        return 0
    fi
    return 1
}

locales_vistos() {
    local crudos="" clave valor
    for clave in LC_ALL LC_MESSAGES LANG LANGUAGE; do
        eval "valor=\${${clave}-}"
        if [ -n "${valor}" ]; then
            crudos="${crudos} ${valor}"
        fi
    done
    if command -v locale >/dev/null 2>&1; then
        crudos="${crudos} $(locale 2>/dev/null | awk -F= '/^(LANG|LC_ALL|LC_MESSAGES)=/{gsub(/\"/,\"\"); print $2}')"
    fi
    echo "${crudos}" | tr '[:upper:]' '[:lower:]' | tr ':-' '  ' | tr -s ' '
}

solo_c_o_posix() {
    local token hay=0
    for token in $(locales_vistos); do
        token="${token%%.*}"
        token="${token%%@*}"
        [ -z "${token}" ] && continue
        hay=1
        case "${token}" in
            c|posix) ;;
            *) return 1 ;;
        esac
    done
    [ "${hay}" -eq 1 ]
}

ya_en_bashrc() {
    local linea="$1"
    [ -f "${BASHRC}" ] && grep -Fqx "${linea}" "${BASHRC}"
}

anadir_export() {
    local linea="$1"
    if ya_en_bashrc "${linea}"; then
        echo "[setLocale] Ya estaba en ${BASHRC}: ${linea}"
        return
    fi
    touch "${BASHRC}"
    printf '\n# MetsuOS locale (setLocale.sh)\n%s\n' "${linea}" >> "${BASHRC}"
    echo "[setLocale] Añadido a ${BASHRC}: ${linea}"
}

echo "[setLocale] Locales vistos: $(locales_vistos | tr -s ' ' ',')"

if ! solo_c_o_posix; then
    echo "[setLocale] No es el caso C/POSIX. No se toca nada."
    exit 0
fi

if ! es_wsl && [ "$(uname -s 2>/dev/null)" != "Linux" ]; then
    echo "[setLocale] Solo Linux/WSL. En Git Bash no uses este script."
    exit 1
fi

if [ ! -d "${HOME}" ] || [[ "${PWD}" == /mnt/[a-zA-Z]/* ]]; then
    echo "[setLocale] Aviso: si el clone de MOS está bajo /mnt/<letra>/, muévelo a \$HOME."
fi

echo
echo "[setLocale] Este sistema está en locale C/POSIX."
echo "[setLocale] MetsuOS oficial solo arranca con es_ES."
echo "[setLocale] Se va a:"
echo "  1. Instalar/generar ${DESTINO} (apt + locale-gen; pide sudo)."
echo "  2. Fijar LANG y LC_ALL en esta sesión."
echo "  3. Añadir esos export a ${BASHRC} si no existen."
echo
echo "[setLocale] No cambia otros idiomas. No se ejecuta si el locale ya no es C."
printf "[setLocale] ¿Aceptas? Escribe s y Enter: "
read -r resp
case "${resp}" in
    s|S|si|sí|Si|Sí) ;;
    *)
        echo "[setLocale] Cancelado."
        exit 1
        ;;
esac

if ! command -v locale-gen >/dev/null 2>&1; then
    echo "[setLocale] Instalando paquete locales..."
    sudo apt-get update
    sudo apt-get install -y locales
fi

echo "[setLocale] Generando ${DESTINO}..."
sudo locale-gen "${DESTINO}"
if command -v update-locale >/dev/null 2>&1; then
    sudo update-locale "LANG=${DESTINO}"
fi

export LANG="${DESTINO}"
export LC_ALL="${DESTINO}"

anadir_export "${EXPORT_LANG}"
anadir_export "${EXPORT_ALL}"

echo
echo "[setLocale] Sesión actual: LANG=${LANG} LC_ALL=${LC_ALL}"
echo "[setLocale] Abre otra terminal WSL o: source ${BASHRC}"
echo "[setLocale] Luego, en el clone Linux (no /mnt/c): ./mos2.sh"