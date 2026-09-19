"""Ingesta y generate de specs."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.docgen_index import DOCUMENTOS, get_documento, get_docgen_dir, get_project_root
from moslib.core.docgen_io import escribir, mejor_origen, partir_markdown, recuperar_preambulo
from moslib.core.docgen_man_run import guardar_json


def list_spec_ids() -> list[str]:
    return [d["id"] for d in DOCUMENTOS if d["rel"].startswith("docs/specs/")]


def spec_store_path(doc_id: str) -> Path:
    return get_docgen_dir() / "specs" / f"{doc_id}.json"


def ingest_spec(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None or not item["rel"].startswith("docs/specs/"):
        raise FileNotFoundError(f"no es una spec: {doc_id}")
    origen = mejor_origen(doc_id, get_project_root() / item["rel"])
    titulo, preambulo, secciones, cuerpo = partir_markdown(
        origen.read_text(encoding="utf-8"), doc_id
    )
    return guardar_json(
        spec_store_path(doc_id),
        {
            "schema": "metsuos-docgen-spec-1",
            "id": doc_id,
            "titulo": titulo,
            "preambulo": recuperar_preambulo(doc_id, preambulo),
            "cuerpo_completo": cuerpo,
            "origen": str(origen),
            "secciones": secciones,
        },
    )


def render_spec(doc_id: str) -> str:
    store = spec_store_path(doc_id)
    if not store.is_file():
        raise FileNotFoundError(f"no hay json de {doc_id}")
    extra = json.loads(store.read_text(encoding="utf-8"))
    if extra.get("cuerpo_completo"):
        return extra["cuerpo_completo"]
    bloques = [f"# {extra.get('titulo', doc_id)}", ""]
    if extra.get("preambulo"):
        bloques.extend([extra["preambulo"], ""])
    from moslib.core.docgen_req import list_reqs, tablas_por_area

    hay_reqs = bool(list_reqs()) if doc_id == "02-srs" else False
    for sec in extra.get("secciones") or []:
        titulo = sec.get("titulo") or "SECCIÓN"
        cuerpo = sec.get("cuerpo") or ""
        if hay_reqs and "requisito" in titulo.lower():
            cuerpo = tablas_por_area()
        bloques.extend([f"## {titulo}", cuerpo, ""])
    return "\n".join(bloques)


def generate_spec(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    return escribir(doc_id, render_spec(doc_id), get_project_root() / item["rel"])


def ingest_spec_todos(forzar: bool = True) -> list:
    ids = list_spec_ids()
    if not forzar:
        ids = [i for i in ids if not spec_store_path(i).is_file()]
    return [ingest_spec(i) for i in ids]


def generate_spec_todos() -> list:
    escritos = []
    for doc_id in list_spec_ids():
        try:
            escritos.append(generate_spec(doc_id))
        except Exception as exc:
            print(f"[docgen] {doc_id}: {exc}")
    return escritos
