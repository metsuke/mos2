"""Historial del puente mos2ai."""

from __future__ import annotations

import json
import os
from datetime import datetime

from moslib.core.mos2ai_estado import ARCHIVO_HISTORIAL, RUTA_BASE


def guardar_historial_chat(chat) -> None:
    temp = ARCHIVO_HISTORIAL + ".tmp"
    try:
        serial = []
        for message in chat.history:
            parts = []
            for p in message.parts:
                if getattr(p, "text", None):
                    parts.append({"text": p.text})
                elif getattr(p, "function_call", None):
                    fc = p.function_call
                    parts.append({"function_call": {"name": fc.name, "args": dict(fc.args)}})
                elif getattr(p, "function_response", None):
                    fr = p.function_response
                    parts.append({"function_response": {"name": fr.name, "response": dict(fr.response)}})
            serial.append({"role": message.role, "parts": parts})
        os.makedirs(RUTA_BASE, exist_ok=True)
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(serial, f, indent=4)
        if os.path.exists(ARCHIVO_HISTORIAL):
            os.remove(ARCHIVO_HISTORIAL)
        os.rename(temp, ARCHIVO_HISTORIAL)
    except Exception as exc:
        print(f"[Aviso] No se pudo guardar el historial: {exc}")
        if os.path.exists(temp):
            os.remove(temp)


def cargar_historial_chat():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []
    try:
        with open(ARCHIVO_HISTORIAL, encoding="utf-8") as f:
            data = json.load(f)
        from google.ai.generativelanguage_v1beta.types import Content, FunctionCall, FunctionResponse, Part
        out = []
        for item in data:
            parts = []
            for p in item.get("parts") or []:
                if "text" in p:
                    parts.append(Part.from_text(p["text"]))
                elif "function_call" in p:
                    fc = p["function_call"]
                    parts.append(Part(function_call=FunctionCall(name=fc["name"], args=fc["args"])))
                elif "function_response" in p:
                    fr = p["function_response"]
                    parts.append(Part(function_response=FunctionResponse(name=fr["name"], response=fr["response"])))
            out.append(Content(role=item["role"], parts=parts))
        return out
    except Exception as exc:
        print(f"[Aviso] Historial incompatible, se reinicia: {exc}")
        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.rename(ARCHIVO_HISTORIAL, f"{ARCHIVO_HISTORIAL}.corrupt_{marca}")
        return []
