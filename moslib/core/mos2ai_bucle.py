"""Bucle del puente mos2ai. Lo llaman mos2AI.py y el comando."""

from __future__ import annotations

import os

from moslib.core.mos2ai_estado import (
    bloquear_modelo_hoy,
    cargar_modelos_seleccionados,
    guardar_modelos_seleccionados,
    modelo_esta_bloqueado_hoy,
    quitar_modelos_inexistentes,
)
from moslib.core.mos2ai_tools import DISPATCH, HERRAMIENTAS

SYSTEM = (
    "Eres un asistente de IA dentro de MetsuOS. "
    "Usa las herramientas para listar, leer, crear directorios y "
    "escribir o crear ficheros dentro del directorio de trabajo. "
    "No inventes rutas fuera de ese sandbox."
)


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


def _modelos(genai) -> list[str]:
    vivos = []
    for m in genai.list_models():
        if "generateContent" not in (m.supported_generation_methods or []):
            continue
        if "flash" not in m.name.lower():
            continue
        nombre = m.name.replace("models/", "")
        if "tts" in nombre or "image" in nombre:
            continue
        vivos.append(nombre)
    return vivos


def _elegir(vivos: list[str]) -> list[str]:
    cola = quitar_modelos_inexistentes(cargar_modelos_seleccionados(), vivos)
    if cola:
        return cola
    print("\n[INFO] Secuencia vacia. Elige el primer modelo:")
    for i, modelo in enumerate(vivos):
        print(f"  {i + 1}. {modelo}")
    while True:
        try:
            sel = int(input("\nNumero: ")) - 1
        except ValueError:
            continue
        if 0 <= sel < len(vivos):
            cola = [vivos[sel]]
            guardar_modelos_seleccionados(cola)
            return cola


def _aplicar(response) -> None:
    llamadas = getattr(response, "function_calls", None) or []
    if not llamadas:
        return
    for fc in llamadas:
        fn = DISPATCH.get(fc.name)
        args = dict(getattr(fc, "args", {}) or {})
        print(f"[tool] {fc.name} {args}")
        res = fn(**args) if fn else "Funcion no reconocida."
        print(res)


def main() -> None:
    print("========================================")
    print("   PUENTE DE INGESTA METSUAI (sistema)  ")
    print("========================================")
    try:
        import google.generativeai as genai
    except ImportError:
        print("Falta google-generativeai")
        return
    key = _clave()
    if not key:
        key = input("GEMINI_API_KEY: ").strip()
    if not key:
        print("Se requiere la clave.")
        return
    genai.configure(api_key=key)
    try:
        vivos = _modelos(genai)
    except Exception as exc:
        print(f"[Error] No se pudo listar modelos: {exc}")
        return
    if not vivos:
        print("[Error] No hay modelos Flash.")
        return
    cola = _elegir(vivos)
    indice = 0
    while modelo_esta_bloqueado_hoy(cola[indice]) and indice < len(cola) - 1:
        indice += 1
    modelo = cola[indice]
    print(f"\n[INFO] Modelo activo: {modelo}")
    chat = genai.GenerativeModel(modelo, tools=HERRAMIENTAS, system_instruction=SYSTEM).start_chat()
    print("[INFO] Puente establecido. 'salir' termina.")
    while True:
        prompt = input(f"\n[Tu - {modelo}]: ").strip()
        if prompt.lower() in ("salir", "exit", "quit"):
            print("[INFO] Cerrando puente.")
            return
        if not prompt:
            continue
        try:
            response = chat.send_message(prompt)
        except Exception as exc:
            texto = str(exc)
            if "429" in texto or "Quota" in texto:
                bloquear_modelo_hoy(modelo)
                indice = (indice + 1) % len(cola)
                modelo = cola[indice]
                print(f"[!] Cuota. Siguiente: {modelo}")
                chat = genai.GenerativeModel(
                    modelo, tools=HERRAMIENTAS, system_instruction=SYSTEM
                ).start_chat(history=chat.history)
                continue
            print(f"[Error] {exc}")
            continue
        _aplicar(response)
        print("\n[MetsuAI]:")
        print(getattr(response, "text", "") or "")
