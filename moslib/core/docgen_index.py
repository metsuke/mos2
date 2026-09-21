"""Indice de documentos y rutas de docgen."""

from __future__ import annotations

from pathlib import Path


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
    {"id": "11-integridad", "rel": "docs/specs/11-INTEGRIDAD.md"},
)


def man_documentos() -> list:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    return [
        {"id": "man-" + path.stem, "rel": "docs/man/" + path.name}
        for path in sorted(man_dir.glob("*.md"))
    ]


def todos_documentos() -> list:
    vistos = {}
    for item in list(DOCUMENTOS) + man_documentos():
        vistos[item["id"]] = item
    return list(vistos.values())


def list_document_ids() -> list:
    return [d["id"] for d in todos_documentos()]


def get_documento(doc_id: str):
    key = (doc_id or "").strip().lower()
    for item in todos_documentos():
        if item["id"] == key:
            return dict(item)
    return None


def resolve_path(doc_id: str):
    item = get_documento(doc_id)
    if item is None:
        return None
    return get_project_root() / item["rel"]


resuelve_path = resolve_path


def ensure_docgen_dirs():
    get_backup_dir().mkdir(parents=True, exist_ok=True)
    base = get_docgen_dir()
    for nombre in ("specs", "man", "pages", "root", "html", "reqs", "plans"):
        (base / nombre).mkdir(parents=True, exist_ok=True)
