"""
moslib.core.docgen
Motor de regeneración de documentos: rutas, inventario, backup, man.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import shutil


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def get_docgen_dir() -> Path:
    return get_project_root() / "docs" / "docgen"


def get_backup_dir() -> Path:
    return get_docgen_dir() / "backup"


def get_areas_path() -> Path:
    return get_docgen_dir() / "areas.json"


DOCUMENTOS = (
    {"id": "readme", "rel": "README.md"},
    {"id": "changelog", "rel": "CHANGELOG.md"},
    {"id": "agents", "rel": "AGENTS.md"},
    {"id": "license", "rel": "LICENSE"},
    {"id": "user-manual", "rel": "docs/USER_MANUAL.md"},
    {"id": "methodology", "rel": "docs/METHODOLOGY.md"},
    {"id": "environments", "rel": "docs/ENVIRONMENTS.md"},
    {"id": "versioning", "rel": "docs/VERSIONING.md"},
    {"id": "style-guide", "rel": "docs/STYLE_GUIDE.md"},
    {"id": "a11y", "rel": "docs/A11Y.md"},
    {"id": "ai-onboarding", "rel": "docs/AI_ONBOARDING.md"},
    {"id": "human-onboarding", "rel": "docs/HUMAN_ONBOARDING.md"},
    {"id": "developer-guide", "rel": "docs/DEVELOPER_GUIDE.md"},
    {"id": "incentivos", "rel": "docs/INCENTIVOS.md"},
    {"id": "interaction-review", "rel": "docs/INTERACTION_REVIEW.md"},
    {"id": "deuda", "rel": "docs/DEUDA_Y_CAMPANAS.md"},
    {"id": "plans-readme", "rel": "docs/plans/README.md"},
    {"id": "00-overview", "rel": "docs/specs/00-OVERVIEW.md"},
    {"id": "01-sss", "rel": "docs/specs/01-SSS-System-Specification.md"},
    {"id": "02-srs", "rel": "docs/specs/02-SRS-Software-Requirements.md"},
    {"id": "03-icd", "rel": "docs/specs/03-ICD-Interfaces-and-Command-Contract.md"},
    {"id": "04-sec", "rel": "docs/specs/04-SEC-Security-Policy.md"},
    {"id": "05-sdd", "rel": "docs/specs/05-SDD-Architecture-and-Design.md"},
    {"id": "06-test", "rel": "docs/specs/06-TEST-Verification-and-Validation.md"},
    {"id": "07-sreld", "rel": "docs/specs/07-SRelD-Release-Baseline.md"},
    {"id": "08-apps", "rel": "docs/specs/08-APPS.md"},
    {"id": "09-tasks", "rel": "docs/specs/09-TASKS.md"},
    {"id": "10-ia-router", "rel": "docs/specs/10-IA-ROUTER.md"},
)



def man_documentos() -> list[dict]:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    return [
        {"id": f"man-{path.stem}", "rel": f"docs/man/{path.name}"}
        for path in sorted(man_dir.glob("*.md"))
    ]


def todos_documentos() -> list[dict]:
    vistos = {}
    for item in list(DOCUMENTOS) + man_documentos():
        vistos[item["id"]] = item
    return list(vistos.values())


def list_document_ids() -> list[str]:
    return [d["id"] for d in todos_documentos()]


def get_documento(doc_id: str) -> dict | None:
    key = (doc_id or "").strip().lower()
    for item in todos_documentos():
        if item["id"] == key:
            return dict(item)
    return None


def resolve_path(doc_id: str) -> Path | None:
    item = get_documento(doc_id)
    if item is None:
        return None
    return get_project_root() / item["rel"]


def ensure_docgen_dirs() -> None:
    get_backup_dir().mkdir(parents=True, exist_ok=True)


def backup_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def backup_document(doc_id: str) -> Path | None:
    src = resolve_path(doc_id)
    if src is None or not src.is_file():
        return None
    ensure_docgen_dirs()
    dest_dir = get_backup_dir() / doc_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{backup_stamp()}{src.suffix or '.md'}"
    shutil.copy2(src, dest)
    return dest


def list_backups(doc_id: str) -> list[Path]:
    folder = get_backup_dir() / doc_id
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_file())


def scan_command_help(nombre: str) -> str:
    import importlib

    mod = importlib.import_module(f"moslib.commands.{nombre}")
    texto = mod.help()
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"help() vacío en {nombre}")
    return texto.strip()


def man_store_path(nombre: str) -> Path:
    return get_docgen_dir() / "man" / f"{nombre}.json"


def list_man_nombres() -> list[str]:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    return [p.stem for p in sorted(man_dir.glob("*.md"))]



def ingest_man(nombre: str) -> Path:
    import json
    import re

    doc_id = f"man-{nombre}"
    candidatos = []
    src = get_project_root() / "docs" / "man" / f"{nombre}.md"
    if src.is_file():
        candidatos.append(src)
    candidatos.extend(list_backups(doc_id))
    if not candidatos:
        raise FileNotFoundError(f"no hay man ni backup para {nombre}")

    def _tam(path: Path) -> int:
        try:
            return path.stat().st_size
        except OSError:
            return 0

    origen = max(candidatos, key=_tam)
    texto = origen.read_text(encoding="utf-8")
    titulo = nombre
    secciones = []
    actual = None
    buf = []

    def _cerrar():
        nonlocal actual, buf
        if actual is None:
            buf = []
            return
        secciones.append({"titulo": actual, "cuerpo": "\n".join(buf).strip()})
        actual = None
        buf = []

    for linea in texto.splitlines():
        if linea.startswith("## "):
            _cerrar()
            actual = linea[3:].strip()
            continue
        if linea.startswith("# "):
            titulo = linea[2:].strip()
            continue
        if actual is not None:
            buf.append(linea)
    _cerrar()
    dest = man_store_path(nombre)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps(
            {
                "schema": "metsuos-docgen-man-1",
                "id": nombre,
                "titulo": titulo,
                "origen": str(origen),
                "secciones": secciones,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return dest


def render_man(nombre: str) -> str:
    import json

    ayuda = scan_command_help(nombre)
    store = man_store_path(nombre)
    if not store.is_file():
        raise FileNotFoundError(
            f"no hay json de {nombre}; ejecuta docgen ingest man"
        )
    extra = json.loads(store.read_text(encoding="utf-8"))
    bloques = [f"# {extra.get('titulo', nombre)}", ""]
    for sec in extra.get("secciones") or []:
        tit = sec.get("titulo") or "SECCIÓN"
        cuerpo = sec.get("cuerpo") or ""
        bloques.extend([f"## {tit}", cuerpo, ""])
    bloques.extend(["## HELP DEL COMANDO", ayuda, ""])
    return "\n".join(bloques)


def generate_man(nombre: str) -> Path:
    doc_id = f"man-{nombre}"
    nuevo = render_man(nombre)
    src = resolve_path(doc_id)
    if src is not None and src.is_file():
        actual = src.read_text(encoding="utf-8")
        if len(nuevo) < max(80, int(len(actual) * 0.5)):
            raise RuntimeError(
                f"docgen aborta: man-{nombre} quedaría mucho más corto."
            )
        backup_document(doc_id)
    dest = get_project_root() / "docs" / "man" / f"{nombre}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(nuevo, encoding="utf-8")
    return dest


def ingest_man_todos(forzar: bool = True) -> list:
    nombres = list_man_nombres()
    if not forzar:
        nombres = [n for n in nombres if not man_store_path(n).is_file()]
    return [ingest_man(n) for n in nombres]


def generate_man_todos() -> list:
    ingest_man_todos(forzar=True)
    return [generate_man(n) for n in list_man_nombres()]