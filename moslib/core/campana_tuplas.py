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


def _reescribir(ident: str, tipo: str, titulo: str, cuerpo: str, para_humano: str) -> str:
    """Pisa la tupla con la fuente. Un toque en disco no sobrevive a esta pasada."""
    try:
        actual = load_tupla(ident)
    except FileNotFoundError:
        actual = None
    t = actual if isinstance(actual, dict) else plantilla(ident, tipo=tipo)
    t["id"] = ident
    t["tipo"] = tipo
    t["titulo"] = titulo
    t["cuerpo"] = cuerpo
    t["para_humano"] = para_humano
    guardar_tupla(t)
    return ident


def convertir_docs_json_a_tuplas() -> list[str]:
    root = Path(__file__).resolve().parent.parent.parent
    docs_dir = root / "docs"
    convertidos = []

    status_usr = _leer_status_usuario()
    status_id = f"user_status_{get_username()}"
    convertidos.append(
        _reescribir(
            status_id,
            "status_usuario",
            f"Status de usuario: {get_username()}",
            json.dumps(status_usr, ensure_ascii=False, indent=2),
            f"Estado actual recogido desde la carpeta del usuario {get_username()}.",
        )
    )

    planes_dir = docs_dir / "plans"
    if planes_dir.is_dir():
        for p in sorted(planes_dir.glob("*.md")):
            convertidos.append(
                _reescribir(
                    f"plan_{p.stem}",
                    "plan",
                    f"Plan: {p.stem}",
                    p.read_text(encoding="utf-8", errors="replace"),
                    f"Plan real importado desde {p.relative_to(root)}",
                )
            )
    return convertidos
