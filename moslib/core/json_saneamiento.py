"""Saneamiento y ensamblaje atómico de contextos JSON corruptos.

Permite:
- Releer JSONs corruptos o dañados extrayendo la parte válida/no dañada.
- Guardar elementos como ítems atómicos en una subcarpeta (por defecto en .mos/tmp/atomic_json o similar).
- Mostrar barras de progreso y vistas previas formateadas y claras para humanos.
- Ensamblar la versión completa uniendo los átomos no dañados.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from moslib.core.user import ensure_user_space, get_username, get_user_mos_dir


def _atomic_dir(nombre_sesion: str = "default") -> Path:
    d = get_user_mos_dir(get_username()) / "tmp" / "atomic_json" / nombre_sesion
    d.mkdir(parents=True, exist_ok=True)
    return d


def barra_progreso(actual: int, total: int, ancho: int = 30, mensaje: str = "") -> None:
    """Muestra una barra de progreso limpia en la terminal."""
    if total <= 0:
        porcentaje = 100.0
        completado = ancho
    else:
        porcentaje = min(100.0, max(0.0, (actual / total) * 100.0))
        completado = int(ancho * actual // total)
    
    barra = "█" * completado + "-" * (ancho - completado)
    print(f"\r[{barra}] {porcentaje:5.1f}% ({actual}/{total}) {mensaje}", end="", flush=True)
    if actual >= total:
        print()


def formatear_humano(datos: Any, limite_lineas: int = 20) -> str:
    """Devuelve una representación JSON formateada claramente para humanos."""
    texto = json.dumps(datos, indent=2, ensure_ascii=False)
    lineas = texto.splitlines()
    if len(lineas) <= limite_lineas:
        return texto
    
    corte = limite_lineas // 2
    muestra = lineas[:corte] + [f"  ... [{len(lineas) - limite_lineas} líneas omitidas] ..."] + lineas[-corte:]
    return "\n".join(muestra)


def _fusionar_dicts(bloques: list) -> dict | None:
    if not bloques or not all(isinstance(b, dict) for b in bloques):
        return None
    out: dict = {}
    for b in bloques:
        out.update(b)
    return out


def extraer_parte_valida(contenido_bruto: str) -> Tuple[Any, List[str]]:
    """Intenta parsear el JSON completo; si falla, realiza un recorrido heurístico
    o incremental para extraer objetos/pares válidos no dañados."""
    errores = []
    try:
        parsed = json.loads(contenido_bruto)
        return parsed, ["JSON completo válido."]
    except Exception as e:
        errores.append(f"JSON directo inválido: {e}")

    valido_parcial: Any = {}
    if contenido_bruto.strip().startswith("["):
        valido_parcial = []

    lineas = contenido_bruto.splitlines()
    total_lineas = len(lineas)
    bloques_validos = []

    print(f"\n[Saneamiento] Analizando {total_lineas} líneas de contexto dañado...")
    for i, linea in enumerate(lineas):
        if i % 50 == 0 or i == total_lineas - 1:
            barra_progreso(i + 1, total_lineas, mensaje="Leyendo líneas")

        linea_limpia = linea.strip()
        if not linea_limpia:
            continue
        try:
            if (linea_limpia.startswith("{") and linea_limpia.endswith("}")) or \
               (linea_limpia.startswith("[") and linea_limpia.endswith("]")) or \
               (":" in linea_limpia):
                sub_parsed = None
                try:
                    sub_parsed = json.loads(linea_limpia.rstrip(","))
                except Exception:
                    pass
                if sub_parsed is not None:
                    bloques_validos.append(sub_parsed)
        except Exception:
            pass

    if bloques_validos:
        errores.append(f"Se rescataron {len(bloques_validos)} fragmentos atómicos válidos.")
        fusion = _fusionar_dicts(bloques_validos)
        if fusion is not None:
            return fusion, errores
        return bloques_validos, errores

    return ({} if isinstance(valido_parcial, dict) else []), errores


def sanitizar_y_atomizar(ruta_origen: str | Path, nombre_sesion: str = "default") -> Tuple[bool, str, Any]:
    """Lee un contexto corrupto, extrae partes válidas, las guarda como átomos
    y devuelve la estructura completa ensamblada."""
    ruta = Path(ruta_origen)
    ensure_user_space(get_username())

    if not ruta.is_file():
        return False, f"Fichero no encontrado: {ruta}", None

    try:
        contenido = ruta.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return False, f"Error al leer fichero: {e}", None

    print(f"\n[Saneamiento] Leyendo contexto corrupto desde: {ruta}")
    parsed, logs = extraer_parte_valida(contenido)

    dir_atomos = _atomic_dir(nombre_sesion)

    items_a_procesar = []
    if isinstance(parsed, dict):
        items_a_procesar = list(parsed.items())
    elif isinstance(parsed, list):
        items_a_procesar = list(enumerate(parsed))
    else:
        items_a_procesar = [("valor_unico", parsed)]

    total_items = len(items_a_procesar)
    print(f"\n[Atomización] Guardando {total_items} ítems atómicos en {dir_atomos}...")

    atomos_guardados = {}
    for idx, (k, v) in enumerate(items_a_procesar):
        if idx % max(1, total_items // 10) == 0 or idx == total_items - 1:
            barra_progreso(idx + 1, total_items, mensaje="Guardando átomos")

        atomo_nombre = f"atomo_{idx}_{str(k)[:30]}.json"
        atomo_path = dir_atomos / atomo_nombre
        atomo_data = {"key": k, "value": v}
        atomo_path.write_text(json.dumps(atomo_data, indent=2, ensure_ascii=False), encoding="utf-8")
        atomos_guardados[str(k)] = v

    ensamblado: Any = {}
    if isinstance(parsed, list):
        ensamblado = list(atomos_guardados.values())
    else:
        ensamblado = atomos_guardados

    print("\n[Ensamblaje] Versión completa reconstruida con éxito.")
    return True, "\n".join(logs), ensamblado
