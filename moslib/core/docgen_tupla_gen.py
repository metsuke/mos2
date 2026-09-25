"""Generate MD recorriendo tuplas hijas."""

from __future__ import annotations

from moslib.core.docgen_index import get_documento, get_project_root
from moslib.core.docgen_tupla_crud import list_tuplas
from moslib.core.docgen_tupla_render import render_nodos


def _prefijo(doc_id: str) -> str:
    texto = (doc_id or "").strip().strip("/")
    if texto.startswith("doc/"):
        return texto
    return "doc/" + texto


def _orden(item: dict) -> tuple:
    ident = item.get("id") or ""
    return (ident.count("/"), int(item.get("orden") or 0), ident)


def nodos_de(doc_id: str) -> list:
    items = list_tuplas(_prefijo(doc_id))
    return sorted(items, key=_orden)


def destino_md(doc_id: str):
    item = get_documento(doc_id.split("/")[-1])
    root = get_project_root()
    if item and item.get("rel"):
        return root / item["rel"]
    return root / "docs" / ((_prefijo(doc_id).split("/")[-1].upper().replace("-", "_")) + ".md")


def generate_tupla(doc_id: str):
    nodos = nodos_de(doc_id)
    if not nodos:
        raise FileNotFoundError(doc_id)
    texto = render_nodos(nodos)
    dest = destino_md(doc_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(texto, encoding="utf-8")
    try:
        from moslib.core.integridad import registrar
        rel = dest.resolve().relative_to(get_project_root().resolve()).as_posix()
        registrar(rel)
    except Exception:
        pass
    return dest
