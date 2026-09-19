"""Ingesta y generate de pages/root."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.docgen_index import (
    DOCUMENTOS,
    get_documento,
    get_docgen_dir,
    get_project_root,
)
from moslib.core.docgen_io import escribir, mejor_origen, partir_markdown, recuperar_preambulo
from moslib.core.docgen_man_run import man_store_path
from moslib.core.docgen_spec_run import spec_store_path


def store_path_doc(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    rel = item["rel"]
    if rel.startswith("docs/specs/"):
        return spec_store_path(doc_id)
    if rel.startswith("docs/man/"):
        return man_store_path(doc_id.replace("man-", "", 1))
    if rel.startswith("docs/"):
        return get_docgen_dir() / "pages" / f"{doc_id}.json"
    return get_docgen_dir() / "root" / f"{doc_id}.json"


def list_page_ids() -> list[str]:
    return [d["id"] for d in DOCUMENTOS if not d["rel"].startswith("docs/specs/")]


def _guardar_json(dest: Path, payload: dict) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def ingest_doc(doc_id: str) -> Path:
    from moslib.core.docgen_man_run import ingest_man
    from moslib.core.docgen_spec_run import ingest_spec

    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    if item["rel"].startswith("docs/specs/"):
        return ingest_spec(doc_id)
    if item["id"].startswith("man-"):
        return ingest_man(item["id"][4:])
    origen = mejor_origen(doc_id, get_project_root() / item["rel"])
    titulo, preambulo, secciones, cuerpo = partir_markdown(
        origen.read_text(encoding="utf-8"), doc_id
    )
    preambulo = recuperar_preambulo(doc_id, preambulo)
    return _guardar_json(
        store_path_doc(doc_id),
        {
            "schema": "metsuos-docgen-doc-1",
            "id": doc_id,
            "titulo": titulo,
            "preambulo": preambulo,
            "cuerpo_completo": cuerpo,
            "origen": str(origen),
            "secciones": secciones,
        },
    )


def render_doc(doc_id: str) -> str:
    from moslib.core.docgen_man_run import render_man
    from moslib.core.docgen_spec_run import render_spec

    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    if item["rel"].startswith("docs/specs/"):
        return render_spec(doc_id)
    if item["id"].startswith("man-"):
        return render_man(item["id"][4:])
    store = store_path_doc(doc_id)
    if not store.is_file():
        raise FileNotFoundError(f"no hay json de {doc_id}")
    extra = json.loads(store.read_text(encoding="utf-8"))
    if extra.get("cuerpo_completo"):
        return extra["cuerpo_completo"]
    bloques = [f"# {extra.get('titulo', doc_id)}", ""]
    if extra.get("preambulo"):
        bloques.extend([extra["preambulo"], ""])
    for sec in extra.get("secciones") or []:
        bloques.extend([f"## {sec.get('titulo') or 'SECCIÓN'}", sec.get("cuerpo") or "", ""])
    return "\n".join(bloques)


def generate_doc(doc_id: str) -> Path:
    from moslib.core.docgen_man_run import generate_man
    from moslib.core.docgen_spec_run import generate_spec

    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    if doc_id == "plans-readme":
        from moslib.core.docgen_plan import render_plans_readme
        return escribir(doc_id, render_plans_readme(), get_project_root() / item["rel"])
    if item["rel"].startswith("docs/specs/"):
        return generate_spec(doc_id)
    if item["id"].startswith("man-"):
        return generate_man(item["id"][4:])
    return escribir(doc_id, render_doc(doc_id), get_project_root() / item["rel"])
