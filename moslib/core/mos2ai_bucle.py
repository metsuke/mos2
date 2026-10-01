"""Bucle del puente. Tras una herramienta sigue hasta haber texto."""

from __future__ import annotations

import os
import time
import random

from moslib.core.mos2ai_estado import (
    bloquear_modelo_hoy,
    cargar_modelos_seleccionados,
    guardar_modelos_seleccionados,
    modelo_esta_bloqueado_hoy,
    vetados,
    vetar_modelo,
)
from moslib.core.mos2ai_historial import cargar_historial_chat, guardar_historial_chat
from moslib.core.mos2ai_permiso import aplicar as aplicar_permiso
from moslib.core.mos2ai_tools import DISPATCH, HERRAMIENTAS

SYSTEM = (
    "Eres el puente de ingesta de MetsuOS. "
    "Lista, lee, crea directorios y escribe o crea ficheros en el directorio de trabajo. "
    "No salgas de ese sandbox. Tras cada herramienta, sigue la tarea o responde."
)
_ULTIMA = 0.0
TOPE_PASOS = 8


def _ritmo() -> None:
    global _ULTIMA
    ahora = time.time()
    ideal = 12.0 + random.uniform(1.0, 3.0)
    if _ULTIMA and ahora - _ULTIMA < ideal:
        time.sleep(ideal - (ahora - _ULTIMA))
    _ULTIMA = time.time()


def _clave() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    try:
        from moslib.core import ia_keys
        ia_keys.ingest_env()
        return ia_keys.resolve_key("google") or ia_keys.resolve_key("gemini") or ""
    except Exception:
        return ""


def _cuota(texto: str) -> bool:
    return "429" in texto or "Quota" in texto or "PerDay" in texto


def _no_existe(texto: str) -> bool:
    baja = texto.lower()
    return "404" in baja or "no longer available" in baja or "not found" in baja


def _llamadas(response) -> list:
    vistas = list(getattr(response, "function_calls", None) or [])
    if vistas:
        return vistas
    out = []
    for part in getattr(response, "parts", None) or []:
        fc = getattr(part, "function_call", None)
        if fc and getattr(fc, "name", None):
            out.append(fc)
    return out


def _texto(response) -> str:
    trozos = []
    for part in getattr(response, "parts", None) or []:
        texto = getattr(part, "text", None)
        if texto:
            trozos.append(texto)
    return "\n".join(trozos)


def _resumen(nombre: str, res: str) -> str:
    if nombre != "listar_directorio":
        return res
    if res.startswith("Error") or res.startswith("(vac"):
        return res
    n = len([ln for ln in res.splitlines() if ln.strip()])
    return f"{n} elementos listados"


def _modelos(genai) -> list[str]:
    fuera = set(vetados())
    vivos = []
    for m in genai.list_models():
        if "generateContent" not in (m.supported_generation_methods or []):
            continue
        if "flash" not in m.name.lower():
            continue
        nombre = m.name.replace("models/", "")
        if "tts" in nombre or "image" in nombre or nombre in fuera:
            continue
        vivos.append(nombre)
    return vivos


def _chat(genai, modelo, history):
    modelo_api = genai.GenerativeModel(modelo, tools=HERRAMIENTAS, system_instruction=SYSTEM)
    return modelo_api.start_chat(history=history, enable_automatic_function_calling=False)


def _ronda(response, chat):
    paso = 0
    while _llamadas(response) and paso < TOPE_PASOS:
        paso += 1
        partes = []
        for fc in _llamadas(response):
            args = dict(getattr(fc, "args", {}) or {})
            print(f"[mos2ai] paso {paso}: el modelo pide {fc.name}, aun no hay respuesta final")
            res = aplicar_permiso(fc.name, args, DISPATCH.get(fc.name))
            print(f"[mos2ai] {_resumen(fc.name, res)}. Devuelvo el resultado al modelo y sigo.")
            partes.append({"function_response": {"name": fc.name, "response": {"result": res}}})
        _ritmo()
        print("[mos2ai] esperando el siguiente paso del modelo")
        response = chat.send_message(partes)
    return response


def _siguiente(cola, indice, genai, history):
    if not cola:
        return None, 0, None
    indice = indice % len(cola)
    modelo = cola[indice]
    return modelo, indice, _chat(genai, modelo, history)


def main() -> None:
    print("========================================")
    print("   PUENTE DE INGESTA METSUAI (sistema)  ")
    print("========================================")
    try:
        import google.generativeai as genai
    except ImportError:
        print("Falta google-generativeai")
        return
    key = _clave() or input("GEMINI_API_KEY: ").strip()
    if not key:
        print("Se requiere la clave.")
        return
    genai.configure(api_key=key)
    vivos = _modelos(genai)
    cola = [m for m in cargar_modelos_seleccionados() if m in vivos]
    guardar_modelos_seleccionados(cola)
    if not cola and vivos:
        for i, nombre in enumerate(vivos):
            print(f"  {i + 1}. {nombre}")
        sel = int(input("Numero inicial: ")) - 1
        cola = [vivos[sel]]
        guardar_modelos_seleccionados(cola)
    if not cola:
        print("[Error] No hay modelos Flash utilizables.")
        return
    indice = 0
    modelo, indice, chat = _siguiente(cola, indice, genai, cargar_historial_chat())
    print(f"[INFO] Modelo activo: {modelo}")
    while True:
        prompt = input(f"\n[Tu - {modelo}]: ").strip()
        if prompt.lower() in ("salir", "exit", "quit"):
            guardar_historial_chat(chat)
            return
        if not prompt:
            continue
        try:
            print("[mos2ai] pidiendo respuesta al modelo")
            _ritmo()
            response = _ronda(chat.send_message(prompt), chat)
            guardar_historial_chat(chat)
            print("\n[MetsuAI]:")
            print(_texto(response) or "[mos2ai] el modelo no ha escrito cierre")
        except Exception as exc:
            texto = str(exc)
            if _no_existe(texto):
                print(f"[!] {modelo} no existe. Fuera de la rotacion.")
                vetar_modelo(modelo)
                cola = [m for m in cola if m != modelo]
                if not cola:
                    print("[Error] No quedan modelos en la cola.")
                    return
                modelo, indice, chat = _siguiente(cola, indice, genai, chat.history)
                print(f"[INFO] Siguiente: {modelo}")
                continue
            if not _cuota(texto):
                print(f"[Error] {exc}")
                continue
            bloquear_modelo_hoy(modelo)
            indice = (indice + 1) % len(cola)
            modelo, indice, chat = _siguiente(cola, indice, genai, chat.history)
            print(f"[!] Cuota. Siguiente: {modelo}")
