"""
moslib.core.docgen
Motor de regeneración de documentos.
Fuente: JSON en docs/docgen/. generate no ingiere.
Tras escribir markdown, escribe HTML en docs/docgen/html/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import re
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
    (get_docgen_dir() / "specs").mkdir(parents=True, exist_ok=True)
    (get_docgen_dir() / "man").mkdir(parents=True, exist_ok=True)
    (get_docgen_dir() / "pages").mkdir(parents=True, exist_ok=True)
    (get_docgen_dir() / "root").mkdir(parents=True, exist_ok=True)
    (get_docgen_dir() / "html").mkdir(parents=True, exist_ok=True)
    (get_docgen_dir() / "reqs").mkdir(parents=True, exist_ok=True)


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



def _mejor_origen(doc_id: str, fallback: Path | None) -> Path:
    candidatos = []
    if fallback is not None and fallback.is_file():
        candidatos.append(fallback)
    candidatos.extend(list_backups(doc_id))
    if not candidatos:
        raise FileNotFoundError(f"no hay origen para {doc_id}")
    return max(candidatos, key=lambda p: p.stat().st_size)


def _partir_markdown(texto: str, titulo_defecto: str):
    lineas = texto.splitlines()
    if not any(linea.startswith("## ") for linea in lineas):
        titulo = titulo_defecto
        if lineas and lineas[0].startswith("# "):
            titulo = lineas[0][2:].strip()
        return titulo, "", [], texto

    titulo = titulo_defecto
    preambulo_lineas = []
    secciones = []
    actual = None
    buf = []
    visto_h1 = False

    def _cerrar():
        nonlocal actual, buf
        if actual is None:
            buf = []
            return
        secciones.append({"titulo": actual, "cuerpo": "\n".join(buf).strip()})
        actual = None
        buf = []

    for linea in lineas:
        if linea.startswith("## "):
            _cerrar()
            actual = linea[3:].strip()
            continue
        if linea.startswith("# "):
            titulo = linea[2:].strip()
            visto_h1 = True
            continue
        if actual is None and visto_h1:
            preambulo_lineas.append(linea)
            continue
        if actual is not None:
            buf.append(linea)
    _cerrar()
    return titulo, "\n".join(preambulo_lineas).strip(), secciones, None


def _preambulo_completo(preambulo: str) -> bool:
    return "versión del documento" in preambulo.lower()


def _recuperar_preambulo(doc_id: str, preambulo: str) -> str:
    if _preambulo_completo(preambulo):
        return preambulo
    for path in reversed(list_backups(doc_id)):
        try:
            texto = path.read_text(encoding="utf-8")
        except OSError:
            continue
        _, cand, _, cuerpo = _partir_markdown(texto, "")
        if _preambulo_completo(cand):
            return cand
        if cuerpo and _preambulo_completo(cuerpo):
            return cuerpo
    return preambulo


def _sin_version(texto: str) -> str:
    return re.sub(
        r"\*\*Versión del documento:\*\*\s*[0-9.]+",
        "**Versión del documento:**",
        texto,
    )


def _bump_preambulo(texto: str) -> str:
    def _sub(match):
        piezas = match.group(1).split(".")
        piezas[-1] = str(int(piezas[-1]) + 1)
        return f"**Versión del documento:** {'.'.join(piezas)}"

    nuevo, n = re.subn(
        r"\*\*Versión del documento:\*\*\s*([0-9.]+)",
        _sub,
        texto,
        count=1,
    )
    return nuevo if n else texto


def _ultimo_backup_texto(doc_id: str) -> str | None:
    backups = list_backups(doc_id)
    if not backups:
        return None
    return backups[-1].read_text(encoding="utf-8")


def _escribir(doc_id: str, nuevo: str, dest: Path) -> Path:
    anterior = _ultimo_backup_texto(doc_id)
    if anterior is None and dest.is_file():
        anterior = dest.read_text(encoding="utf-8")
    if anterior is not None and _sin_version(nuevo) != _sin_version(anterior):
        nuevo = _bump_preambulo(nuevo)
    if dest.is_file():
        if len(nuevo) < max(80, int(len(dest.read_text(encoding="utf-8")) * 0.5)):
            raise RuntimeError(f"docgen aborta: {doc_id} quedaría mucho más corto.")
        backup_document(doc_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(nuevo, encoding="utf-8")
    from moslib.core.docgen_html import escribir_html
    escribir_html(doc_id, nuevo)
    return dest


def scan_command_help(nombre: str) -> str:
    import importlib

    mod = importlib.import_module(f"moslib.commands.{nombre}")
    texto = mod.help()
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"help() vacío en {nombre}")
    return texto.strip()


def _guardar_json(dest: Path, payload: dict) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return dest



def man_store_path(nombre: str) -> Path:
    return get_docgen_dir() / "man" / f"{nombre}.json"


def list_man_nombres() -> list[str]:
    man_dir = get_project_root() / "docs" / "man"
    if not man_dir.is_dir():
        return []
    return [p.stem for p in sorted(man_dir.glob("*.md"))]


def ingest_man(nombre: str) -> Path:
    doc_id = f"man-{nombre}"
    origen = _mejor_origen(doc_id, get_project_root() / "docs" / "man" / f"{nombre}.md")
    titulo, preambulo, secciones, cuerpo = _partir_markdown(
        origen.read_text(encoding="utf-8"), nombre
    )
    preambulo = _recuperar_preambulo(doc_id, preambulo)
    return _guardar_json(
        man_store_path(nombre),
        {
            "schema": "metsuos-docgen-man-1",
            "id": nombre,
            "titulo": titulo,
            "preambulo": preambulo,
            "cuerpo_completo": cuerpo,
            "origen": str(origen),
            "secciones": secciones,
        },
    )


def render_man(nombre: str) -> str:
    store = man_store_path(nombre)
    if not store.is_file():
        raise FileNotFoundError(f"no hay json de {nombre}")
    extra = json.loads(store.read_text(encoding="utf-8"))
    if extra.get("cuerpo_completo"):
        return extra["cuerpo_completo"]
    bloques = [f"# {extra.get('titulo', nombre)}", ""]
    if extra.get("preambulo"):
        bloques.extend([extra["preambulo"], ""])
    for sec in extra.get("secciones") or []:
        bloques.extend(
            [f"## {sec.get('titulo') or 'SECCIÓN'}", sec.get("cuerpo") or "", ""]
        )
    bloques.extend(["## HELP DEL COMANDO", scan_command_help(nombre), ""])
    return "\n".join(bloques)


def generate_man(nombre: str) -> Path:
    return _escribir(
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


def list_spec_ids() -> list[str]:
    return [d["id"] for d in DOCUMENTOS if d["rel"].startswith("docs/specs/")]


def spec_store_path(doc_id: str) -> Path:
    return get_docgen_dir() / "specs" / f"{doc_id}.json"


def ingest_spec(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None or not item["rel"].startswith("docs/specs/"):
        raise FileNotFoundError(f"no es una spec: {doc_id}")
    origen = _mejor_origen(doc_id, get_project_root() / item["rel"])
    titulo, preambulo, secciones, cuerpo = _partir_markdown(
        origen.read_text(encoding="utf-8"), doc_id
    )
    preambulo = _recuperar_preambulo(doc_id, preambulo)
    return _guardar_json(
        spec_store_path(doc_id),
        {
            "schema": "metsuos-docgen-spec-1",
            "id": doc_id,
            "titulo": titulo,
            "preambulo": preambulo,
            "cuerpo_completo": cuerpo,
            "origen": str(origen),
            "secciones": secciones,
        },
    )



def render_spec(doc_id: str) -> str:
    store = spec_store_path(doc_id)
    if not store.is_file():
        raise FileNotFoundError(f"no hay json de {doc_id}")
    extra = json.loads(store.read_text(encoding="utf-8"))
    if extra.get("cuerpo_completo"):
        return extra["cuerpo_completo"]
    bloques = [f"# {extra.get('titulo', doc_id)}", ""]
    if extra.get("preambulo"):
        bloques.extend([extra["preambulo"], ""])
    from moslib.core.docgen_req import list_reqs, tablas_por_area

    hay_reqs = bool(list_reqs()) if doc_id == "02-srs" else False
    for sec in extra.get("secciones") or []:
        titulo = sec.get("titulo") or "SECCIÓN"
        cuerpo = sec.get("cuerpo") or ""
        if hay_reqs and "requisito" in titulo.lower():
            cuerpo = tablas_por_area()
        bloques.extend([f"## {titulo}", cuerpo, ""])
    return "\n".join(bloques)


def generate_spec(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    return _escribir(doc_id, render_spec(doc_id), get_project_root() / item["rel"])


def ingest_spec_todos(forzar: bool = True) -> list:
    ids = list_spec_ids()
    if not forzar:
        ids = [i for i in ids if not spec_store_path(i).is_file()]
    return [ingest_spec(i) for i in ids]


def generate_spec_todos() -> list:
    escritos = []
    for doc_id in list_spec_ids():
        try:
            escritos.append(generate_spec(doc_id))
        except Exception as exc:
            print(f"[docgen] {doc_id}: {exc}")
    return escritos


def store_path_doc(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    rel = item["rel"]
    if rel.startswith("docs/specs/"):
        return spec_store_path(doc_id)
    if rel.startswith("docs/man/"):
        return man_store_path(doc_id.replace("man-", "", 1))
    if rel.startswith("docs/"):
        return get_docgen_dir() / "pages" / f"{doc_id}.json"
    return get_docgen_dir() / "root" / f"{doc_id}.json"


def list_page_ids() -> list[str]:
    return [d["id"] for d in DOCUMENTOS if not d["rel"].startswith("docs/specs/")]


def ingest_doc(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    if item["rel"].startswith("docs/specs/"):
        return ingest_spec(doc_id)
    if item["id"].startswith("man-"):
        return ingest_man(item["id"][4:])
    origen = _mejor_origen(doc_id, get_project_root() / item["rel"])
    titulo, preambulo, secciones, cuerpo = _partir_markdown(
        origen.read_text(encoding="utf-8"), doc_id
    )
    preambulo = _recuperar_preambulo(doc_id, preambulo)
    return _guardar_json(
        store_path_doc(doc_id),
        {
            "schema": "metsuos-docgen-doc-1",
            "id": doc_id,
            "titulo": titulo,
            "preambulo": preambulo,
            "cuerpo_completo": cuerpo,
            "origen": str(origen),
            "secciones": secciones,
        },
    )


def render_doc(doc_id: str) -> str:
    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    if item["rel"].startswith("docs/specs/"):
        return render_spec(doc_id)
    if item["id"].startswith("man-"):
        return render_man(item["id"][4:])
    store = store_path_doc(doc_id)
    if not store.is_file():
        raise FileNotFoundError(f"no hay json de {doc_id}")
    extra = json.loads(store.read_text(encoding="utf-8"))
    if extra.get("cuerpo_completo"):
        return extra["cuerpo_completo"]
    bloques = [f"# {extra.get('titulo', doc_id)}", ""]
    if extra.get("preambulo"):
        bloques.extend([extra["preambulo"], ""])
    for sec in extra.get("secciones") or []:
        bloques.extend(
            [f"## {sec.get('titulo') or 'SECCIÓN'}", sec.get("cuerpo") or "", ""]
        )
    return "\n".join(bloques)


def generate_doc(doc_id: str) -> Path:
    item = get_documento(doc_id)
    if item is None:
        raise FileNotFoundError(doc_id)
    if item["rel"].startswith("docs/specs/"):
        return generate_spec(doc_id)
    if item["id"].startswith("man-"):
        return generate_man(item["id"][4:])
    return _escribir(doc_id, render_doc(doc_id), get_project_root() / item["rel"])


def ingest_page_todos(forzar: bool = True) -> list:
    ids = list_page_ids()
    if not forzar:
        ids = [i for i in ids if not store_path_doc(i).is_file()]
    return [ingest_doc(i) for i in ids]


def generate_page_todos() -> list:
    escritos = []
    for doc_id in list_page_ids():
        try:
            escritos.append(generate_doc(doc_id))
        except Exception as exc:
            print(f"[docgen] {doc_id}: {exc}")
    return escritos


def ingest_todo() -> list:
    return ingest_man_todos(True) + ingest_spec_todos(True) + ingest_page_todos(True)


def generate_todo() -> list:
    return generate_man_todos() + generate_spec_todos() + generate_page_todos()