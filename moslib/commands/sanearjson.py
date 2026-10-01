"""Comando 'sanearjson': Sanea contextos JSON corruptos, crea átomos y ensambla la versión limpia."""

from __future__ import annotations

import json
from pathlib import Path
from moslib.core.json_saneamiento import sanitizar_y_atomizar, formatear_humano


def execute(args):
    if not args:
        print("[sanearjson] Uso: sanearjson <ruta_json_corrupto> [nombre_sesion]")
        print("Ejemplo: sanearjson datos_rotos.json sesion_01")
        return 1

    ruta_origen = args[0]
    nombre_sesion = args[1] if len(args) > 1 else "default"

    exito, mensaje, ensamblado = sanitizar_y_atomizar(ruta_origen, nombre_sesion)
    print(f"\n--- Logs de Saneamiento ---\n{mensaje}")

    if not exito or ensamblado is None:
        print("[sanearjson] Error en el proceso de saneamiento.")
        return 1

    print("\n--- Vista Previa Formateada para Humanos ---")
    print(formatear_humano(ensamblado, limite_lineas=25))

    # Opcional: preguntar si desea guardar el archivo saneado limpio
    salida_defecto = Path(ruta_origen).with_name(f"saneado_{Path(ruta_origen).name}")
    resp = input(f"\n¿Desea guardar el JSON completo ensamblado en '{salida_defecto}'? [S/n]: ").strip().lower()
    if resp in ("", "s", "si", "sí"):
        try:
            salida_defecto.write_text(json.dumps(ensamblado, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"[sanearjson] Guardado correctamente en: {salida_defecto}")
        except Exception as e:
            print(f"[sanearjson] Error al guardar: {e}")
            return 1

    return 0


def help():
    return (
        "Uso: sanearjson <ruta_json_corrupto> [nombre_sesion]\n"
        "Relee contextos JSON dañados, extrae partes válidas, crea ítems atómicos\n"
        "en subcarpeta, muestra progreso y ofrece vista y guardado formateado."
    )


def sinopsis():
    return ["sanearjson <ruta>", "sanearjson <ruta> <sesion>"]
