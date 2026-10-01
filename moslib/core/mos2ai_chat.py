"""Chat agentico. El humano no recupera el prompt al rotar."""

from __future__ import annotations

import json

from moslib.core.mos2ai_bucle import anotar, montar, rotar, ultimo_encargo

HERRAMIENTAS = ("listar_directorio", "leer_fichero", "fin")


def _linea(texto: str) -> None:
    print(texto, flush=True)


def _pedir(modelo: str, mensajes: list[dict], completar) -> tuple[bool, str]:
    return completar(modelo, mensajes)


def _parsear(texto: str) -> dict:
    bruto = texto.strip()
    if bruto.startswith("```"):
        bruto = bruto.strip("`")
        if bruto.startswith("json"):
            bruto = bruto[4:]
    try:
        data = json.loads(bruto)
    except json.JSONDecodeError:
        return {"tipo": "decir", "texto": texto}
    return data if isinstance(data, dict) else {"tipo": "decir", "texto": texto}


def _mensajes(extra: str) -> list[dict]:
    base = montar()
    orden = (
        "Eres el agente de MetsuOS. Responde solo JSON: "
        '{"tipo":"decir","texto":"..."} o '
        '{"tipo":"herramienta","nombre":"listar_directorio|leer_fichero|fin","args":""}. '
        "No esperes al humano si ya hay encargo.\n"
        + extra
    )
    base.append({"role": "user", "content": orden})
    return base


def turno(modelo: str, completar, ejecutar, pendiente: str = "") -> tuple[str, bool]:
    extra = pendiente or ultimo_encargo() or "Espera el encargo del humano."
    ok, texto = _pedir(modelo, _mensajes(extra), completar)
    if not ok and texto.strip().lower() == "cuota":
        siguiente = completar.siguiente(modelo)
        _linea(f"[!] Cuota. Siguiente: {siguiente}")
        _linea("[mos2ai] contexto y ultimo encargo al modelo nuevo. Sigo.")
        rotar(siguiente, pendiente, lambda msgs: _pedir(siguiente, msgs, completar)[1])
        return siguiente, False
    if not ok:
        _linea(f"[mos2ai] error: {texto}")
        return modelo, True
    anotar("acciones", "assistant", texto, modelo)
    orden = _parsear(texto)
    if orden.get("tipo") == "decir":
        _linea(orden.get("texto") or "")
        return modelo, False
    nombre = str(orden.get("nombre") or "")
    if nombre == "fin":
        return modelo, True
    if nombre not in HERRAMIENTAS:
        anotar("acciones", "assistant", f"Herramienta desconocida: {nombre}", modelo)
        return modelo, False
    _linea(f"[cliente] ejecutando 1 vez: {nombre}")
    resultado = ejecutar(nombre, str(orden.get("args") or ""))
    _linea(f"[mos2ai] resultado de {nombre}. Lo devuelvo al modelo y sigo.")
    anotar("acciones", "assistant", f"Resultado de {nombre}:\n{resultado}", modelo)
    return turno(modelo, completar, ejecutar, resultado)


def chat(modelo: str, completar, ejecutar) -> None:
    encargo = ultimo_encargo()
    if not encargo:
        _linea(f"[Tu - {modelo}]:")
        return
    _linea(f"[mos2ai] encargo en curso con {modelo}. No espero.")
    activo = modelo
    while True:
        activo, parar = turno(activo, completar, ejecutar)
        if parar:
            return
        if not ultimo_encargo():
            _linea(f"[Tu - {activo}]:")
            return