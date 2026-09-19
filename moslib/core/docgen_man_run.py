"""Ingesta y generate de páginas man."""

from __future__ import annotations

import json
from pathlib import Path

from moslib.core.docgen_index import get_docgen_dir, get_project_root
from moslib.core.docgen_io import (
    escribir,
    mejor_origen,
    partir_markdown,
    recuperar_preambulo,
)


def man_store_path(nombre: str) -> Path:
    return get_docgen_dir() / "man" / f"{nombre}.json"


def list_man_nombres() -> list[str]:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    return [p.stem for p in sorted(man_dir.glob("*.md"))]


def guardar_json(dest: Path, payload: dict) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def ingest_man(nombre: str) -> Path:
    from moslib.core.docgen_man import marcar_sinopsis_en_store

    doc_id = f"man-{nombre}"
    origen = mejor_origen(doc_id, get_project_root() / "docs" / "man" / f"{nombre}.md")
    titulo, preambulo, secciones, cuerpo = partir_markdown(
        origen.read_text(encoding="utf-8"), nombre
    )
    dest = guardar_json(
        man_store_path(nombre),
        {
            "schema": "metsuos-docgen-man-1",
            "id": nombre,
            "titulo": titulo,
            "preambulo": recuperar_preambulo(doc_id, preambulo),
            "cuerpo_completo": cuerpo,
            "origen": str(origen),
            "secciones": secciones,
        },
    )
    marcar_sinopsis_en_store(nombre)
    return dest


def render_man(nombre: str) -> str:
    from moslib.core.docgen_man import armar_man, marcar_sinopsis_en_store

    marcar_sinopsis_en_store(nombre)
    store = man_store_path(nombre)
    extra = {}
    if store.is_file():
        extra = json.loads(store.read_text(encoding="utf-8"))
    return armar_man(nombre, extra)


def generate_man(nombre: str) -> Path:
    from moslib.core.docgen_man import marcar_sinopsis_en_store

    marcar_sinopsis_en_store(nombre)
    return escribir(
        f"man-{nombre}",
        render_man(nombre),
        get_project_root() / "docs" / "man" / f"{nombre}.md",
    )


def ingest_man_todos(forzar: bool = True) -> list:
    nombres = list_man_nombres()
    if not forzar:
        nombres = [n for n in nombres if not man_store_path(n).is_file()]
    return [ingest_man(n) for n in nombres]


def generate_man_todos() -> list:
    escritos = []
    for nombre in list_man_nombres():
        try:
            escritos.append(generate_man(nombre))
        except Exception as exc:
            print(f"[docgen] man-{nombre}: {exc}")
    return escritos


def scan_command_help(nombre: str) -> str:
    import importlib

    texto = importlib.import_module(f"moslib.commands.{nombre}").help()
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"help() vacío en {nombre}")
    return texto.strip()
