"""
moslib.core.docgen_plan
Un JSON por plan en docs/docgen/plans/.
El índice docs/plans/README.md se pinta desde esos JSON.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from moslib.core import docgen as motor

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
    dest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return dest


def list_planes() -> list[dict]:
    out = []
    for path in sorted(plans_dir().glob("*.json")):
        if path.name.startswith("_"):
            continue
        out.append(json.loads(path.read_text(encoding="utf-8")))
    out.sort(key=lambda p: (p.get("fecha") or "", p.get("nn") or "", p.get("id") or ""))
    return out


def _estado_desde_md(texto: str) -> str:
    for linea in texto.splitlines():
        baja = linea.strip()
        if baja.lower().startswith("**estado:**"):
            return baja.split(":", 1)[1].strip().strip("*").strip()
        if baja.lower().startswith("estado:"):
            return baja.split(":", 1)[1].strip()
    return "Diseñada"


def ingest_planes() -> list[Path]:
    escritos = []
    carpeta = plan_md_dir()
    if not carpeta.is_dir():
        return escritos
    for path in sorted(carpeta.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        partes = parse_nombre(path.name)
        if partes is None:
            continue
        fecha, nn, slug = partes
        plan_id = path.stem
        estado = "Diseñada"
        try:
            estado = _estado_desde_md(path.read_text(encoding="utf-8"))
        except OSError:
            pass
        escritos.append(
            guardar_plan(
                {
                    "schema": "metsuos-docgen-plan-1",
                    "id": plan_id,
                    "fecha": fecha,
                    "nn": nn,
                    "slug": slug,
                    "archivo": path.name,
                    "estado": estado,
                }
            )
        )
    return escritos


def plan_add(archivo: str, estado: str = "Diseñada") -> Path:
    nombre = Path(archivo).name
    if not nombre.endswith(".md"):
        nombre = f"{nombre}.md"
    partes = parse_nombre(nombre)
    if partes is None:
        raise ValueError(f"nombre no cumple YYYY-MM-DD-NN-slug.md: {nombre}")
    fecha, nn, slug = partes
    plan_id = Path(nombre).stem
    if plan_path(plan_id).is_file():
        raise FileExistsError(plan_id)
    return guardar_plan(
        {
            "schema": "metsuos-docgen-plan-1",
            "id": plan_id,
            "fecha": fecha,
            "nn": nn,
            "slug": slug,
            "archivo": nombre,
            "estado": estado,
        }
    )


def plan_set(plan_id: str, campo: str, valor: str) -> Path:
    data = load_plan(plan_id)
    if campo != "estado":
        raise ValueError("solo se asigna estado por CRUD")
    data["estado"] = valor
    return guardar_plan(data)


def plan_rm(plan_id: str) -> Path:
    path = plan_path(plan_id)
    if not path.is_file():
        raise FileNotFoundError(plan_id)
    path.unlink()
    return path


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