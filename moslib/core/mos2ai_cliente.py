"""Cliente mos2ai. La cuota no devuelve el prompt al humano."""

from __future__ import annotations

from moslib.core.mos2ai_bucle import anotar, montar, rotar, ultimo_encargo


def _linea(texto: str) -> None:
    print(texto, flush=True)


def pedir_modelo(modelo: str, mensajes: list[dict], completar) -> tuple[bool, str]:
    """completar(modelo, mensajes) -> (ok, texto). ok False y texto 'cuota' rota."""
    return completar(modelo, mensajes)


def paso(modelo: str, completar, ejecutar, pendiente: str = "") -> tuple[str, str]:
    """Un paso del modelo. Si hay cuota, el nuevo sigue con el mismo pendiente."""
    mensajes = montar()
    encargo = ultimo_encargo()
    if not mensajes and encargo:
        mensajes = [{"role": "user", "content": encargo}]
    ok, texto = pedir_modelo(modelo, mensajes, completar)
    if ok:
        anotar("acciones", "assistant", texto, modelo)
        _linea("[mos2ai] respuesta del modelo. Sigo.")
        return modelo, texto
    if texto.strip().lower() != "cuota":
        _linea(f"[mos2ai] error del modelo: {texto}")
        return modelo, texto
    siguiente = completar.siguiente(modelo)
    _linea(f"[!] Cuota. Siguiente: {siguiente}")
    _linea("[mos2ai] paso el contexto y el ultimo encargo. No espero al humano.")
    salida = rotar(siguiente, pendiente, lambda msgs: pedir_modelo(siguiente, msgs, completar)[1])
    return siguiente, salida


def tras_herramienta(modelo: str, nombre: str, resultado: str, completar, ejecutar) -> str:
    _linea(f"[mos2ai] {nombre}: devuelvo el resultado al modelo y sigo.")
    anotar("acciones", "assistant", f"Resultado de {nombre}:\n{resultado}", modelo)
    modelo, _texto = paso(modelo, completar, ejecutar, resultado)
    return modelo


def bucle(modelo: str, completar, ejecutar) -> None:
    """No abre [Tu - modelo] al rotar. El humano solo entra si no hay encargo."""
    if not ultimo_encargo():
        _linea(f"[Tu - {modelo}]:")
        return
    while True:
        modelo, texto = paso(modelo, completar, ejecutar)
        if texto.strip().lower() == "fin":
            return
        if not ultimo_encargo():
            _linea(f"[Tu - {modelo}]:")
            return