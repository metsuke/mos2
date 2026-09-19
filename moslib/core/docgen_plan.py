"""Un JSON por plan. El índice README se pinta desde esos JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path

from moslib.core import docgen as motor
from moslib.core.docgen_plan_crud import ingest_planes, plan_add, plan_rm, plan_set

NOMBRE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(\d{2})-(.+)\.md$")


def plans_dir() -> Path:
    d = motor.get_docgen_dir() / "plans"
    d.mkdir(parents=True, exist_ok=True)
    return d


def plan_md_dir() -> Path:
    return motor.get_project_root() / "docs" / "plans"


def plan_path(plan_id: str) -> Path:
    return plans_dir() / f"{plan_id}.json"


def parse_nombre(nombre: str) -> tuple[str, str, str] | None:
    m = NOMBRE.match(nombre)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def load_plan(plan_id: str) -> dict:
    path = plan_path(plan_id)
    if not path.is_file():
        raise FileNotFoundError(plan_id)
    return json.loads(path.read_text(encoding="utf-8"))


def guardar_plan(payload: dict) -> Path:
    dest = plan_path(payload["id"])
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def list_planes() -> list[dict]:
    out = []
    for path in sorted(plans_dir().glob("*.json")):
        if path.name.startswith("_"):
            continue
        out.append(json.loads(path.read_text(encoding="utf-8")))
    out.sort(key=lambda p: (p.get("fecha") or "", p.get("nn") or "", p.get("id") or ""))
    return out


def tabla_planes() -> str:
    filas = [
        "| Fecha | NN del día | Archivo | Estado |",
        "|-------|------------|---------|--------|",
    ]
    for item in list_planes():
        filas.append(
            f"| {item.get('fecha') or ''} | {item.get('nn') or ''} | "
            f"{item.get('archivo') or ''} | {item.get('estado') or ''} |"
        )
    return "\n".join(filas)


def render_plans_readme() -> str:
    store = motor.store_path_doc("plans-readme")
    titulo = "Planes de campaña de MetsuOS"
    preambulo = ""
    secciones = []
    if store.is_file():
        extra = json.loads(store.read_text(encoding="utf-8"))
        titulo = extra.get("titulo") or titulo
        preambulo = extra.get("preambulo") or ""
        secciones = list(extra.get("secciones") or [])
        if extra.get("cuerpo_completo"):
            return extra["cuerpo_completo"]
    if not secciones:
        secciones = [
            {"titulo": "Propósito", "cuerpo": "Cada campaña tiene un plan escrito antes de implementar."},
            {"titulo": "Índice", "cuerpo": ""},
            {"titulo": "Ciclo", "cuerpo": "Diseñar, escribir el plan, ejecutar, cerrar estado."},
            {"titulo": "Autoridad", "cuerpo": "No se inicia una campaña amplia sin su plan en esta carpeta."},
        ]
    bloques = [f"# {titulo}", ""]
    if preambulo:
        bloques.extend([preambulo, ""])
    hay = bool(list_planes())
    for sec in secciones:
        tit = sec.get("titulo") or "SECCIÓN"
        cuerpo = sec.get("cuerpo") or ""
        if hay and tit.strip().lower() in ("índice", "indice"):
            cuerpo = tabla_planes()
        bloques.extend([f"## {tit}", cuerpo, ""])
    return "\n".join(bloques)
