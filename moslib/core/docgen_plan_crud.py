"""CRUD e ingest de planes docgen."""

from __future__ import annotations

from pathlib import Path


def _estado_desde_md(texto: str) -> str:
    for linea in texto.splitlines():
        baja = linea.strip()
        if baja.lower().startswith("**estado:**"):
            return baja.split(":", 1)[1].strip().strip("*").strip()
        if baja.lower().startswith("estado:"):
            return baja.split(":", 1)[1].strip()
    return "Diseñada"


def ingest_planes() -> list[Path]:
    from moslib.core.docgen_plan import guardar_plan, parse_nombre, plan_md_dir

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
        estado = "Diseñada"
        try:
            estado = _estado_desde_md(path.read_text(encoding="utf-8"))
        except OSError:
            pass
        escritos.append(
            guardar_plan(
                {
                    "schema": "metsuos-docgen-plan-1",
                    "id": path.stem,
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
    from moslib.core.docgen_plan import guardar_plan, parse_nombre, plan_path

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
    from moslib.core.docgen_plan import guardar_plan, load_plan

    data = load_plan(plan_id)
    if campo != "estado":
        raise ValueError("solo se asigna estado por CRUD")
    data["estado"] = valor
    return guardar_plan(data)


def plan_rm(plan_id: str) -> Path:
    from moslib.core.docgen_plan import plan_path

    path = plan_path(plan_id)
    if not path.is_file():
        raise FileNotFoundError(plan_id)
    path.unlink()
    return path
