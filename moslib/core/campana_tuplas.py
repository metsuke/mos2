"""Campaña de conversión de documentación JSON a tuplas y limpieza."""

from __future__ import annotations

import json
from pathlib import Path
from moslib.core.docgen_tupla import guardar_tupla, load_tupla, plantilla
from moslib.core.user import get_username, get_user_mos_dir


def _leer_status_usuario() -> dict:
    dir_mos = get_user_mos_dir(get_username())
    status_path = dir_mos / "status.json"
    if status_path.is_file():
        try:
            return json.loads(status_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"usuario": get_username(), "estado": "activo", "notas_usuario": []}


def _upsert(ident: str, tipo: str, titulo: str, cuerpo: str, para_humano: str) -> bool:
    try:
        actual = load_tupla(ident)
    except FileNotFoundError:
        actual = None
    if (
        isinstance(actual, dict)
        and actual.get("titulo") == titulo
        and actual.get("cuerpo") == cuerpo
        and actual.get("para_humano") == para_humano
        and actual.get("tipo") == tipo
    ):
        return False
    t = actual if isinstance(actual, dict) else plantilla(ident, tipo=tipo)
    t["id"] = ident
    t["tipo"] = tipo
    t["titulo"] = titulo
    t["cuerpo"] = cuerpo
    t["para_humano"] = para_humano
    guardar_tupla(t)
    return True


def convertir_docs_json_a_tuplas() -> list[str]:
    root = Path(__file__).resolve().parent.parent.parent
    docs_dir = root / "docs"
    convertidos = []

    status_usr = _leer_status_usuario()
    status_id = f"user_status_{get_username()}"
    cuerpo = json.dumps(status_usr, ensure_ascii=False, indent=2)
    if _upsert(
        status_id,
        "status_usuario",
        f"Status de usuario: {get_username()}",
        cuerpo,
        f"Estado actual recogido desde la carpeta del usuario {get_username()}.",
    ):
        convertidos.append(status_id)

    planes_dir = docs_dir / "plans"
    if planes_dir.is_dir():
        for p in planes_dir.glob("*.md"):
            contenido = p.read_text(encoding="utf-8", errors="replace")
            ident = f"plan_{p.stem}"
            if _upsert(
                ident,
                "plan",
                f"Plan: {p.stem}",
                contenido,
                f"Plan real importado desde {p.relative_to(root)}",
            ):
                convertidos.append(ident)
    return convertidos
