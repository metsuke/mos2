"""Comando 'campanatuplas': Ejecuta la conversión de docs y planes a tuplas."""

from __future__ import annotations

from moslib.core.campana_tuplas import convertir_docs_json_a_tuplas


def execute(args):
    print("[campanatuplas] Iniciando conversión de documentación y planes a tuplas...")
    convertidos = convertir_docs_json_a_tuplas()
    print(f"[campanatuplas] Se han convertido/sincronizado {len(convertidos)} nodos en tuplas:")
    for c in convertidos:
        print(f"  - {c}")
    return 0


def help():
    return (
        "Uso: campanatuplas\n"
        "Convierte la documentación y planes reales a formato tupla, leyendo\n"
        "además el status desde la carpeta de usuario y limpiando sistemas legacy."
    )


def sinopsis():
    return ["campanatuplas"]
