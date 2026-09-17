"""
moslib.core.entorno
Etiqueta del anfitrión y política de locale de arranque.

Chequeo técnico, no cláusula extra de licencia. GPL-3.0 intacta.
"""

from __future__ import annotations

import locale
import os
import sys
from pathlib import Path

ETIQUETAS = (
    ("wsl", "WSL"),
    ("win", "Windows nativo"),
    ("mac", "macOS"),
    ("nix", "Linux nativo"),
)

LOCALES_PERMITIDOS = ("es_ES",)

URL_DUDH = "https://www.un.org/es/about-us/universal-declaration-of-human-rights"


def es_wsl() -> bool:
    if Path("/mnt/c/Windows").is_dir():
        return True
    proc = Path("/proc/version")
    if proc.is_file():
        try:
            return "microsoft" in proc.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            return False
    return False


def etiqueta() -> str:
    if es_wsl():
        return "wsl"
    plat = sys.platform
    if plat.startswith("win"):
        return "win"
    if plat == "darwin":
        return "mac"
    if plat.startswith("linux"):
        return "nix"
    return plat[:3]


def descripcion(tag: str | None = None) -> str:
    tag = tag or etiqueta()
    for clave, texto in ETIQUETAS:
        if clave == tag:
            return texto
    return tag


def _normaliza(valor: str) -> str:
    pieza = valor.strip().split(".")[0].split("@")[0]
    return pieza.replace("-", "_")


def locales_detectados() -> list[str]:
    crudos = []
    for clave in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        valor = os.environ.get(clave)
        if valor:
            crudos.append(valor)
    for fn in (locale.getlocale, locale.getdefaultlocale):
        try:
            par = fn()
        except Exception:
            par = None
        if par and par[0]:
            crudos.append(par[0])
    out = []
    for item in crudos:
        for parte in item.replace(":", ";").split(";"):
            norma = _normaliza(parte)
            if norma:
                out.append(norma)
    return out


def locale_permitido() -> bool:
    detectados = [x.lower() for x in locales_detectados()]
    for permitido in LOCALES_PERMITIDOS:
        clave = permitido.lower()
        if clave in detectados:
            return True
        if any(x.startswith(clave + "_") for x in detectados):
            return True
    return False


def pide_simular_bloqueo(argv=None) -> bool:
    if os.environ.get("MOS2_SIMULAR_BLOQUEO_LOCALE", "").strip().lower() in (
        "1",
        "true",
        "si",
        "sí",
    ):
        return True
    return "--simular-bloqueo-locale" in list(argv or [])


def debe_bloquear_locale(argv=None) -> bool:
    return pide_simular_bloqueo(argv) or not locale_permitido()


def mensaje_locale_bloqueado(prueba: bool = False) -> str:
    vistos = ", ".join(locales_detectados()) or "(ninguno)"
    cabecera = ""
    if prueba:
        cabecera = (
            "[PRUEBA] Simulación de bloqueo de locale (--simular-bloqueo-locale).\n"
            "[PRUEBA] El locale real de esta máquina no se ha usado para decidir.\n"
            "[PRUEBA] Esto no es un fallo de tu sistema; es una demostración.\n"
            "\n"
        )
    return cabecera + (
        "[SEGURIDAD] Arranque bloqueado: esta copia oficial de MetsuOS solo arranca\n"
        "con locale español de España (es_ES).\n"
        f"[SEGURIDAD] Locale detectado: {vistos}\n"
        "\n"
        "[MOTIVO] MetsuOS no quiere ser herramienta de quien gobierna contra la\n"
        "dignidad humana. El criterio ético de esta copia oficial es la\n"
        "Declaración Universal de Derechos Humanos:\n"
        f"  {URL_DUDH}\n"
        "En particular: igualdad (arts. 1-2), vida e integridad (3, 5),\n"
        "igualdad ante la ley (6-7), libertad de pensamiento, conciencia y\n"
        "religión (18), opinión (19), y derechos de las mujeres (2 y 16).\n"
        "\n"
        "[MOTIVO] Por eso no se abrirá el arranque oficial a locales de países\n"
        "o territorios cuyo derecho vigente aplica la sharia o un equivalente\n"
        "teocrático como fuente real de coacción (castigos corporales o capitales,\n"
        "tutela religiosa del Estado, discriminación legal de mujeres, minorías\n"
        "o personas LGTBI). Lista de casos conocidos, no cada matiz jurídico,\n"
        "sí los que constan de forma pública:\n"
        "\n"
        "- Ámbito estatal o constitucional islámico / hudud u homólogo:\n"
        "  Arabia Saudí, Irán, Afganistán, Brunéi, Mauritania, Yemen,\n"
        "  Catar, Sudán (cuando rige derecho islámico penal), Maldivas,\n"
        "  Somalia, Pakistán (fuero federal de la sharia / hudood).\n"
        "- Aplicación territorial o federada documentada:\n"
        "  Nigeria (estados del norte), Indonesia (Aceh), Malasia (sharia\n"
        "  estatal para musulmanes), Emiratos Árabes Unidos, Kuwait, Baréin,\n"
        "  Omán, Gaza bajo administración de Hamás.\n"
        "- Derecho de familia o estatuto personal islámico amplio:\n"
        "  Egipto, Jordania, Irak, Libia, Argelia, Marruecos,\n"
        "  Túnez (residual o reformado a tramos),\n"
        "  Palestina (Cisjordania, tribunales de estatuto personal),\n"
        "  Bangladés, Comoras.\n"
        "- Equivalentes teocráticos o clericales no suníes ya incluidos:\n"
        "  Irán (velayat-e faqih). Otros sistemas teocráticos o de partido\n"
        "  único que nieguen la DUDH se estudiarán uno a uno si se pide el locale.\n"
        "\n"
        "[MOTIVO] Esta lista no es un ranking moral de personas. Es una reserva\n"
        "del proyecto frente a ordenamientos. Quien viva bajo esos regímenes y\n"
        "quiera usar MetsuOS en un locale democrático (es_ES u otro que se\n"
        "abra) no está vetado como persona; está vetado el locale de ese\n"
        "ordenamiento en la copia oficial.\n"
        "\n"
        "[QUÉ HACER] Configura la sesión a es_ES (p. ej. LANG=es_ES.UTF-8) y\n"
        "relanza. Si pides otro locale, hazlo de forma razonada. Solo se\n"
        "estudiarán idiomas y países con regímenes democráticos no fanatizados.\n"
        "\n"
        "[LICENCIA] MetsuOS sigue en GPL-3.0. El chequeo es técnico.\n"
        "Puedes leer el código, quitar el chequeo o hacer fork.\n"
        "Quien lo quite asume la carga moral de facilitar el uso donde\n"
        "este proyecto no quiere operar. El árbol oficial no colabora con esa vía."
    )