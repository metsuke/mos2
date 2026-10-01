"""Bucle del puente. Una llamada a herramienta no se lee como texto."""

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
    "No salgas de ese sandbox."
)
_ULTIMA = 0.0


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


def _herramientas(response, chat):
    llamadas = _llamadas(response)
    if not llamadas:
        return response
    partes = []
    for fc in llamadas:
        args = dict(getattr(fc, "args", {}) or {})
        print(f"[tool] {fc.name} {args}")
        res = aplicar_permiso(fc.name, args, DISPATCH.get(fc.name))
        print(res)
        partes.append({"function_response": {"name": fc.name, "response": {"result": res}}})
    _ritmo()
    return chat.send_message(partes)


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
            _ritmo()
            response = _herramientas(chat.send_message(prompt), chat)
            guardar_historial_chat(chat)
            print("\n[MetsuAI]:")
            print(_texto(response) or "(sin texto)")
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
