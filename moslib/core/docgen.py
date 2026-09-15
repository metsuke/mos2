"""
moslib.core.docgen
Motor de regeneración de documentos: rutas, inventario, backup.

No pisa un markdown en este módulo hasta que exista ingestión
y render en fases posteriores. Aquí solo cimientos.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import shutil


def get_project_root() -> Path:
    """Raíz del clone (moslib/ y docs/)."""
    return Path(__file__).resolve().parent.parent.parent


def get_docgen_dir() -> Path:
    return get_project_root() / "docs" / "docgen"


def get_backup_dir() -> Path:
    return get_docgen_dir() / "backup"


def get_areas_path() -> Path:
    return get_docgen_dir() / "areas.json"


# id estable -> ruta relativa al clone
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
    {"id": "man-echo", "rel": "docs/man/echo.md"},
)



def man_documentos() -> list[dict]:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    out = []
    for path in sorted(man_dir.glob("*.md")):
        out.append({"id": f"man-{path.stem}", "rel": f"docs/man/{path.name}"})
    return out


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
    """Crea docs/docgen y backup si faltan."""
    backup = get_backup_dir()
    backup.mkdir(parents=True, exist_ok=True)


def backup_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def backup_document(doc_id: str) -> Path | None:
    """
    Copia el markdown actual a docs/docgen/backup/<id>/<stamp>.md
    No pisa el original. Si el original no existe, no hace nada.
    """
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
    return sorted(folder.iterdir())



def scan_command_help(nombre: str) -> str:
    """Lee help() del comando de sistema sin ejecutarlo."""
    import importlib

    mod = importlib.import_module(f"moslib.commands.{nombre}")
    texto = mod.help()
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"help() vacío en {nombre}")
    return texto.strip()


def man_store_path(nombre: str) -> Path:
    return get_docgen_dir() / "man" / f"{nombre}.json"


def render_man_echo() -> str:
    """Plantilla + help() + prosa absorbida en json si existe."""
    import json

    ayuda = scan_command_help("echo")
    extra = {}
    store = man_store_path("echo")
    if store.is_file():
        extra = json.loads(store.read_text(encoding="utf-8"))
    nombre = extra.get("nombre", "echo – imprime texto en la salida estándar")
    descripcion = extra.get(
        "descripcion",
        "Escribe en pantalla los argumentos recibidos, separados por espacios.",
    )
    opciones = extra.get("opciones", "Ninguna formal en esta baseline.")
    ejemplos = extra.get("ejemplos", "echo hola\necho Hola desde MetsuOS")
    seguridad = extra.get(
        "seguridad",
        "Comando de sistema. No ejecuta el texto como código.",
    )
    vease = extra.get("vease", "help, man")
    return (
        "# echo\n\n"
        "## NOMBRE\n"
        f"{nombre}\n\n"
        "## SINOPSIS\n"
        "echo [texto...]\n\n"
        "## DESCRIPCIÓN\n"
        f"{descripcion}\n\n"
        f"{ayuda}\n\n"
        "## OPCIONES\n"
        f"{opciones}\n\n"
        "## EJEMPLOS\n"
        f"{ejemplos}\n\n"
        "## SEGURIDAD\n"
        f"{seguridad}\n\n"
        "## VÉASE TAMBIÉN\n"
        f"{vease}\n"
    )


def generate_man_echo() -> Path:
    """Backup del man actual y pisa docs/man/echo.md."""
    doc_id = "man-echo"
    nuevo = render_man_echo()
    src = resolve_path(doc_id)
    if src is not None and src.is_file():
        actual = src.read_text(encoding="utf-8")
        if len(nuevo) < len(actual) * 0.5:
            raise RuntimeError(
                "docgen aborta: el render de man-echo es mucho más corto "
                "que el fichero actual. Revisa la plantilla o el json."
            )
        backup_document(doc_id)
    dest = get_project_root() / "docs" / "man" / "echo.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(nuevo, encoding="utf-8")
    return dest



def render_man(nombre: str) -> str:
    import json

    ayuda = scan_command_help(nombre)
    extra = {}
    store = man_store_path(nombre)
    if store.is_file():
        extra = json.loads(store.read_text(encoding="utf-8"))
    titulo = extra.get("titulo", nombre)
    nom = extra.get("nombre", f"{nombre} – comando de sistema")
    sinopsis = extra.get("sinopsis", f"{nombre} [args...]")
    descripcion = extra.get("descripcion", ayuda)
    opciones = extra.get("opciones", "Ver help del comando.")
    ejemplos = extra.get("ejemplos", nombre)
    seguridad = extra.get(
        "seguridad",
        "Comando de sistema. Sujeto a la política de imports.",
    )
    vease = extra.get("vease", "help, man")
    return (
        f"# {titulo}\n\n"
        "## NOMBRE\n"
        f"{nom}\n\n"
        "## SINOPSIS\n"
        f"{sinopsis}\n\n"
        "## DESCRIPCIÓN\n"
        f"{descripcion}\n\n"
        f"{ayuda}\n\n"
        "## OPCIONES\n"
        f"{opciones}\n\n"
        "## EJEMPLOS\n"
        f"{ejemplos}\n\n"
        "## SEGURIDAD\n"
        f"{seguridad}\n\n"
        "## VÉASE TAMBIÉN\n"
        f"{vease}\n"
    )


def generate_man(nombre: str) -> Path:
    doc_id = f"man-{nombre}"
    nuevo = render_man(nombre)
    src = resolve_path(doc_id)
    if src is not None and src.is_file():
        actual = src.read_text(encoding="utf-8")
        if len(nuevo) < max(80, int(len(actual) * 0.5)):
            raise RuntimeError(
                f"docgen aborta: man-{nombre} quedaría mucho más corto. "
                "Absorbe prosa en docs/docgen/man/<nombre>.json"
            )
        backup_document(doc_id)
    dest = get_project_root() / "docs" / "man" / f"{nombre}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(nuevo, encoding="utf-8")
    return dest



def ingest_man(nombre: str) -> Path:
    """
    Lee docs/man/<nombre>.md de hoy y escribe docs/docgen/man/<nombre>.json.
    No pisa el markdown. Secciones por encabezado ##.
    """
    import json
    import re

    src = get_project_root() / "docs" / "man" / f"{nombre}.md"
    if not src.is_file():
        raise FileNotFoundError(f"no existe {src}")
    texto = src.read_text(encoding="utf-8")
    partes = {"titulo": nombre}
    actual = None
    buf = []
    for linea in texto.splitlines():
        m = re.match(r"^#\s+(.+)$", linea)
        if m and not linea.startswith("##"):
            partes["titulo"] = m.group(1).strip()
            continue
        m = re.match(r"^##\s+(.+)$", linea)
        if m:
            if actual is not None:
                partes[actual] = "\n".join(buf).strip()
            raw = m.group(1).strip().lower()
            raw = raw.replace("é", "e").replace("á", "a")
            clave = {
                "nombre": "nombre",
                "sinopsis": "sinopsis",
                "descripcion": "descripcion",
                "opciones": "opciones",
                "ejemplos": "ejemplos",
                "seguridad": "seguridad",
                "vease tambien": "vease",
                "vease": "vease",
            }.get(raw)
            actual = clave
            buf = []
            continue
        if actual is not None:
            buf.append(linea)
    if actual is not None:
        partes[actual] = "\n".join(buf).strip()
    partes["schema"] = "metsuos-docgen-man-1"
    partes["id"] = nombre
    dest = man_store_path(nombre)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(partes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def list_man_nombres() -> list[str]:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    return [p.stem for p in sorted(man_dir.glob("*.md"))]


def ingest_man_faltantes() -> list[Path]:
    """Absorbe cada docs/man/*.md que aún no tenga json."""
    escritos = []
    for nombre in list_man_nombres():
        store = man_store_path(nombre)
        if store.is_file():
            continue
        escritos.append(ingest_man(nombre))
    return escritos


def ingest_man_todos(forzar: bool = False) -> list[Path]:
    """Absorbe todos. Si forzar=False, solo los que faltan."""
    if not forzar:
        return ingest_man_faltantes()
    return [ingest_man(nombre) for nombre in list_man_nombres()]


def generate_man_todos() -> list[Path]:
    """Ingesta lo que falte y regenera todos los man."""
    ingest_man_faltantes()
    return [generate_man(nombre) for nombre in list_man_nombres()]