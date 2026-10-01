"""Bucle completo del puente. Raiz y comando llaman a main()."""

from __future__ import annotations

import os
import time
import random

from moslib.core.mos2ai_estado import (
    bloquear_modelo_hoy,
    cargar_modelos_seleccionados,
    guardar_modelos_seleccionados,
    modelo_esta_bloqueado_hoy,
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
        key = ia_keys.resolve_key("google") or ia_keys.resolve_key("gemini") or ""
        if key:
            print("[INFO] Clave de Google desde iarouter.")
        return key
    except Exception:
        return ""


def _cuota(exc: Exception) -> bool:
    texto = str(exc)
    return "429" in texto or "Quota" in texto or "PerDay" in texto


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


def _chat(genai, modelo, history):
    modelo_api = genai.GenerativeModel(modelo, tools=HERRAMIENTAS, system_instruction=SYSTEM)
    return modelo_api.start_chat(history=history, enable_automatic_function_calling=False)


def _herramientas(response, chat) -> None:
    llamadas = list(getattr(response, "function_calls", None) or [])
    if not llamadas:
        return
    partes = []
    for fc in llamadas:
        args = dict(getattr(fc, "args", {}) or {})
        print(f"[tool] {fc.name} {args}")
        res = aplicar_permiso(fc.name, args, DISPATCH.get(fc.name))
        print(res)
        partes.append({"function_response": {"name": fc.name, "response": {"result": res}}})
    _ritmo()
    chat.send_message(partes)


def _fallback(prompt: str) -> bool:
    from moslib.core.ia_cascade import ORDEN, complete

    print("[INFO] Google agotado. Cascada: grok, openai, openrouter, jan, gpt4all.")
    ok, texto, prov = complete(prompt)
    if ok and prov != "google":
        print(f"[{prov}] {texto}")
        return True
    if ok:
        return False
    print(texto)
    print("Orden:", ", ".join(ORDEN))
    return False


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
    try:
        vivos = _modelos(genai)
    except Exception as exc:
        print(f"[Error] {exc}")
        return
    cola = [m for m in cargar_modelos_seleccionados() if m in vivos]
    guardar_modelos_seleccionados(cola)
    if not cola and vivos:
        for i, modelo in enumerate(vivos):
            print(f"  {i + 1}. {modelo}")
        sel = int(input("Numero inicial: ")) - 1
        cola = [vivos[sel]]
        guardar_modelos_seleccionados(cola)
    if not cola:
        print("[Error] No hay modelos Flash.")
        return
    indice = 0
    while modelo_esta_bloqueado_hoy(cola[indice]) and indice < len(cola) - 1:
        indice += 1
    modelo = cola[indice]
    print(f"[INFO] Modelo activo: {modelo}")
    historial = cargar_historial_chat()
    chat = _chat(genai, modelo, historial)
    print("[INFO] Permiso en lotes de 50. Vista antes/despues al escribir.")
    while True:
        prompt = input(f"\n[Tu - {modelo}]: ").strip()
        if prompt.lower() in ("salir", "exit", "quit"):
            guardar_historial_chat(chat)
            return
        if not prompt:
            continue
        try:
            _ritmo()
            response = chat.send_message(prompt)
            _herramientas(response, chat)
            guardar_historial_chat(chat)
            print("\n[MetsuAI]:")
            print(getattr(response, "text", "") or "")
        except Exception as exc:
            if not _cuota(exc):
                print(f"[Error] {exc}")
                continue
            bloquear_modelo_hoy(modelo)
            print(f"[!] Cuota de {modelo}.")
            if all(modelo_esta_bloqueado_hoy(m) for m in cola):
                _fallback(prompt)
                continue
            indice = (indice + 1) % len(cola)
            modelo = cola[indice]
            chat = _chat(genai, modelo, chat.history)
