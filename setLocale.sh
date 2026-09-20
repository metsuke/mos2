#!/bin/bash
# setLocale.sh — solo el caso MOS "C, C, C" (C/POSIX). Fija es_ES.UTF-8.

set -euo pipefail

DESTINO="es_ES.UTF-8"
BASHRC="${HOME}/.bashrc"
EXPORT_LANG="export LANG=${DESTINO}"
EXPORT_ALL="export LC_ALL=${DESTINO}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

es_wsl() {
    if [ -n "${WSL_DISTRO_NAME:-}" ]; then
        return 0
    fi
    if [ -r /proc/version ] && grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
        return 0
    fi
    return 1
}

env_locales() {
    local clave valor out=""
    for clave in LC_ALL LC_MESSAGES LANG LANGUAGE; do
        eval "valor=\${${clave}-}"
        if [ -n "${valor}" ]; then
            out="${out} ${valor}"
        fi
    done
    echo "${out}"
}

normaliza_token() {
    local t="$1"
    t="${t%%.*}"
    t="${t%%@*}"
    t="$(printf '%s' "${t}" | tr '[:upper:]' '[:lower:]' | tr '-' '_')"
    printf '%s' "${t}"
}

solo_c_o_posix_env() {
    local token hay=0
    for token in $(env_locales); do
        token="$(normaliza_token "${token}")"
        [ -z "${token}" ] && continue
        hay=1
        case "${token}" in
            c|posix) ;;
            *) return 1 ;;
        esac
    done
    [ "${hay}" -eq 1 ]
}

mos_detectados=""
mos_ok=""

mos_consulta() {
    local py=""
    if command -v python3 >/dev/null 2>&1; then
        py="python3"
    elif command -v python >/dev/null 2>&1; then
        py="python"
    else
        return 1
    fi
    mos_detectados="$(
        cd "${ROOT}" && PYTHONPATH="${ROOT}" "${py}" -c \
            "from moslib.core.entorno import locales_detectados; print(', '.join(locales_detectados()) or '(ninguno)')" \
            2>/dev/null
    )" || return 1
    if cd "${ROOT}" && PYTHONPATH="${ROOT}" "${py}" -c \
        "from moslib.core.entorno import locale_permitido; import sys; sys.exit(0 if locale_permitido() else 1)" \
        2>/dev/null
    then
        mos_ok="si"
    else
        mos_ok="no"
    fi
}

es_caso_c() {
    if [ "${mos_ok}" = "si" ]; then
        return 1
    fi
    if [ -n "${mos_detectados}" ]; then
        local t hay=0
        local IFS=','
        for t in ${mos_detectados}; do
            t="$(normaliza_token "${t}")"
            [ -z "${t}" ] || [ "${t}" = "(ninguno)" ] && continue
            hay=1
            case "${t}" in
                c|posix) ;;
                *) return 1 ;;
            esac
        done
        [ "${hay}" -eq 1 ]
        return
    fi
    solo_c_o_posix_env
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

mos_consulta || true
echo "[setLocale] Env:$(env_locales | tr -s ' ' ',') "
echo "[setLocale] MOS detectado: ${mos_detectados:-n/d} permitido=${mos_ok:-n/d}"

if [ "${mos_ok}" = "si" ]; then
    echo "[setLocale] MOS ya acepta el locale. No se toca nada."
    exit 0
fi

if ! es_caso_c; then
    echo "[setLocale] No es el caso C/POSIX. No se toca nada."
    exit 0
fi

if ! es_wsl && [ "$(uname -s 2>/dev/null)" != "Linux" ]; then
    echo "[setLocale] Solo Linux/WSL. En Git Bash no uses este script."
    exit 1
fi

echo
echo "[setLocale] Caso C/POSIX (el de 'Locale detectado: C, C, C')."
echo "[setLocale] Se va a generar ${DESTINO}, fijar LANG/LC_ALL y escribir ${BASHRC}."
echo "[setLocale] Pide sudo para apt/locale-gen."
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
echo "[setLocale] Sesión: LANG=${LANG} LC_ALL=${LC_ALL}"
mos_consulta || true
echo "[setLocale] MOS tras el cambio: ${mos_detectados:-n/d} permitido=${mos_ok:-n/d}"
echo "[setLocale] source ${BASHRC}  y  ./mos2.sh"