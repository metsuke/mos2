"""Generate MD recorriendo tuplas hijas."""

from __future__ import annotations

from moslib.core.docgen_index import documentos, get_documento, get_project_root
from moslib.core.docgen_tupla_crud import list_tuplas
from moslib.core.docgen_tupla_render import render_nodos


def _prefijo(doc_id: str) -> str:
    texto = (doc_id or "").strip().strip("/")
    if texto.startswith("doc/"):
        return texto
    return "doc/" + texto


def _padre(ident: str) -> str:
    if "/el/" in ident:
        return ident.rsplit("/el/", 1)[0]
    if "/sec/" in ident:
        base, resto = ident.rsplit("/sec/", 1)
        if "/" in resto:
            return ident.rsplit("/", 1)[0]
        return base
    if "/" in ident:
        return ident.rsplit("/", 1)[0]
    return ""


def _arbol(items: list) -> list:
    por_id = {str(x.get("id") or ""): x for x in items if x.get("id")}
    hijos = {}
    for ident in por_id:
        hijos.setdefault(_padre(ident), []).append(por_id[ident])
    for lista in hijos.values():
        lista.sort(key=lambda x: (int(x.get("orden") or 0), x.get("id") or ""))

    def walk(padre: str) -> list:
        out = []
        for item in hijos.get(padre, []):
            out.append(item)
            out.extend(walk(item.get("id") or ""))
        return out

    raices = [x for x in items if _padre(x.get("id") or "") not in por_id]
    raices.sort(key=lambda x: (int(x.get("orden") or 0), x.get("id") or ""))
    visto = set()
    ordenados = []
    for raiz in raices:
        for n in [raiz] + walk(raiz.get("id") or ""):
            vid = n.get("id") or ""
            if vid in visto:
                continue
            visto.add(vid)
            ordenados.append(n)
    return ordenados


def nodos_de(doc_id: str) -> list:
    return _arbol(list_tuplas(_prefijo(doc_id)))


def _busca_indice(doc_id: str):
    texto = (doc_id or "").strip().strip("/")
    cola = texto.split("/")[-1]
    for clave in (texto, cola, "man-" + cola, "doc/" + texto):
        item = get_documento(clave)
        if item and item.get("rel"):
            return item
    for item in documentos():
        ident = str(item.get("id") or "")
        rel = str(item.get("rel") or "")
        if ident.endswith(cola) or rel.endswith("/" + cola + ".md"):
            return item
    return None


def destino_md(doc_id: str):
    root = get_project_root()
    item = _busca_indice(doc_id)
    if item and item.get("rel"):
        return root / item["rel"]
    pref = _prefijo(doc_id)
    if "/man/" in pref + "/":
        return root / "docs" / "man" / (pref.split("/")[-1] + ".md")
    nombre = pref.split("/")[-1].upper().replace("-", "_") + ".md"
    return root / "docs" / nombre


def generate_tupla(doc_id: str):
    nodos = nodos_de(doc_id)
    if not nodos:
        raise FileNotFoundError(doc_id)
    dest = destino_md(doc_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(render_nodos(nodos), encoding="utf-8")
    try:
        from moslib.core.integridad import registrar
        rel = dest.resolve().relative_to(get_project_root().resolve()).as_posix()
        registrar(rel)
    except Exception:
        pass
    return dest
