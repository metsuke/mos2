"""Render de tuplas a Markdown."""

from __future__ import annotations


def _desde(ref: str) -> str:
    if not (ref or "").strip():
        return ""
    try:
        from moslib.core.autoria import resolver
        return resolver(ref.strip())
    except Exception:
        return ""


def render_nodo(nodo: dict) -> str:
    if not nodo or not nodo.get("activo", True):
        return ""
    modo = (nodo.get("render") or "parrafo").strip()
    titulo = (nodo.get("titulo") or "").strip()
    cuerpo = (nodo.get("cuerpo") or "").strip()
    extra = _desde(nodo.get("cuerpo_desde") or "")
    if extra:
        cuerpo = (cuerpo + "\n\n" + extra).strip() if cuerpo else extra
    if modo.startswith("h") and modo[1:].isdigit():
        nivel = max(1, min(6, int(modo[1:])))
        lineas = ["#" * nivel + " " + (titulo or "Sin titulo")]
        if cuerpo:
            lineas += ["", cuerpo]
        return "\n".join(lineas)
    if modo == "lista":
        items = [ln.strip() for ln in cuerpo.splitlines() if ln.strip()]
        return "\n".join("- " + item for item in items)
    if modo == "tabla":
        return cuerpo
    if modo == "imagen":
        return f"![{titulo}]({cuerpo})" if cuerpo else ""
    if modo == "mermaid":
        return "```mermaid\n" + cuerpo + "\n```" if cuerpo else ""
    if titulo and cuerpo and modo == "parrafo":
        return f"**{titulo}.** {cuerpo}"
    return cuerpo


def render_nodos(nodos: list) -> str:
    bloques = []
    i = 0
    while i < len(nodos):
        nodo = nodos[i]
        if (nodo.get("render") or "") == "tabla":
            grupo = []
            while i < len(nodos) and (nodos[i].get("render") or "") == "tabla":
                grupo.append(nodos[i])
                i += 1
            texto = "\n\n".join(filter(None, (render_nodo(g) for g in grupo)))
            if texto:
                bloques.append(texto)
            continue
        texto = render_nodo(nodo)
        if texto:
            bloques.append(texto)
        i += 1
    return "\n\n".join(bloques) + ("\n" if bloques else "")


def sembrar_modos(forzar: bool = False) -> list:
    from moslib.core.docgen_tupla import guardar_tupla
    from moslib.core.docgen_tupla_path import ruta
    creados = []
    modos = (
        "parrafo", "h1", "h2", "h3", "h4", "h5", "h6",
        "tabla", "lista", "imagen", "mermaid",
    )
    for modo in modos:
        ident = "render/" + modo
        if ruta(ident).is_file() and not forzar:
            continue
        guardar_tupla(ident, {"tipo": "render-modo", "titulo": modo, "render": modo, "orden": 0})
        creados.append(ident)
    return creados
