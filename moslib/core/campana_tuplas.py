"""Campaña de conversión de documentación JSON a tuplas y limpieza."""

from __future__ import annotations

import json
from pathlib import Path
from moslib.core.docgen_tupla import guardar_tupla, plantilla
from moslib.core.user import get_username, get_user_mos_dir


def _leer_status_usuario() -> dict:
    """Lee el status o tareas/progreso desde la carpeta de usuario (.mos/status o similar)."""
    dir_mos = get_user_mos_dir(get_username())
    status_path = dir_mos / "status.json"
    if status_path.is_file():
        try:
            return json.loads(status_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"usuario": get_username(), "estado": "activo", "notas_usuario": []}


def convertir_docs_json_a_tuplas() -> list[str]:
    """Convierte ficheros de documentación antiguos y planes reales a tuplas,
    leyendo además el status del usuario en su carpeta."""
    root = Path(__file__).resolve().parent.parent.parent
    docs_dir = root / "docs"
    convertidos = []

    # 1. Leer status de usuario
    status_usr = _leer_status_usuario()
    status_id = f"user_status_{get_username()}"
    tupla_status = plantilla(status_id, tipo="status_usuario")
    tupla_status["titulo"] = f"Status de usuario: {get_username()}"
    tupla_status["cuerpo"] = json.dumps(status_usr, ensure_ascii=False, indent=2)
    tupla_status["para_humano"] = f"Estado actual recogido desde la carpeta del usuario {get_username()}."
    guardar_tupla(tupla_status)
    convertidos.append(status_id)

    # 2. Buscar planes reales y documentos legacy en docs/
    planes_dir = docs_dir / "plans"
    if planes_dir.is_dir():
        for p in planes_dir.glob("*.md"):
            contenido = p.read_text(encoding="utf-8", errors="replace")
            ident = f"plan_{p.stem}"
            t = plantilla(ident, tipo="plan")
            t["titulo"] = f"Plan: {p.stem}"
            t["cuerpo"] = contenido
            t["para_humano"] = f"Plan real importado desde {p.relative_to(root)}"
            guardar_tupla(t)
            convertidos.append(ident)

    # 3. Limpiar referencias a viejos sistemas JSON de docgen si existen en docs/docgen/
    docgen_dir = docs_dir / "docgen"
    legacy_jsons = list(docgen_dir.glob("*.json"))
    for lj in legacy_jsons:
        if lj.name != "integridad.json":
            # Opcional: respaldar o eliminar archivos JSON antiguos de documentación
            pass

    return convertidos
