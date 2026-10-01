"""Estado de mos2ai: cuotas, cola y modelos que ya no existen."""

from __future__ import annotations

import json
import os
from datetime import datetime

RUTA_BASE = os.path.join(os.getcwd(), "rootfs", "home", "Metsuke")
ARCHIVO_CUOTAS = os.path.join(RUTA_BASE, ".quota_state.json")
ARCHIVO_SELECCIONADOS = os.path.join(RUTA_BASE, ".selected_models.json")
ARCHIVO_VETADOS = os.path.join(RUTA_BASE, ".vetados_models.json")
ARCHIVO_HISTORIAL = os.path.join(RUTA_BASE, ".chat_history.json")


def cargar_json(path: str, vacio):
    if not os.path.exists(path):
        return vacio
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return vacio


def guardar_json(path: str, data) -> None:
    os.makedirs(RUTA_BASE, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def cargar_estado_cuotas():
    return cargar_json(ARCHIVO_CUOTAS, {})


def guardar_estado_cuotas(estado):
    guardar_json(ARCHIVO_CUOTAS, estado)


def modelo_esta_bloqueado_hoy(modelo: str) -> bool:
    estado = cargar_estado_cuotas()
    hoy = datetime.now().strftime("%Y-%m-%d")
    item = estado.get(modelo) or {}
    return item.get("fecha") == hoy and bool(item.get("bloqueado"))


def bloquear_modelo_hoy(modelo: str) -> None:
    estado = cargar_estado_cuotas()
    estado[modelo] = {"fecha": datetime.now().strftime("%Y-%m-%d"), "bloqueado": True}
    guardar_estado_cuotas(estado)


def cargar_modelos_seleccionados():
    data = cargar_json(ARCHIVO_SELECCIONADOS, [])
    return data if isinstance(data, list) else []


def guardar_modelos_seleccionados(lista) -> None:
    guardar_json(ARCHIVO_SELECCIONADOS, lista)


def vetados() -> list[str]:
    data = cargar_json(ARCHIVO_VETADOS, [])
    return data if isinstance(data, list) else []


def vetar_modelo(modelo: str) -> None:
    fuera = vetados()
    if modelo not in fuera:
        fuera.append(modelo)
        guardar_json(ARCHIVO_VETADOS, fuera)
    cola = [m for m in cargar_modelos_seleccionados() if m != modelo]
    guardar_modelos_seleccionados(cola)


def quitar_modelos_inexistentes(cola: list, vivos: list) -> list:
    fuera = set(vetados())
    limpia = [m for m in cola if m in vivos and m not in fuera]
    if limpia != cola:
        guardar_modelos_seleccionados(limpia)
    return limpia
