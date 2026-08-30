"""
Comando docs de MetsuOS.
Lista o muestra documentación de docs/ y de ficheros públicos de la raíz.
"""

from pathlib import Path

ROOT_DOCS = (
    "README.md",
    "CHANGELOG.md",
    "AGENTS.md",
    "LICENSE",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _docs_root() -> Path:
    return _project_root() / "docs"


def _norm(rel: str) -> str:
    raw = rel.strip().replace("\\", "/").lstrip("/")
    if raw.lower().startswith("./"):
        raw = raw[2:]
    return raw


def _resolve(rel: str) -> Path | None:
    raw = _norm(rel)
    root = _project_root()
    docs = _docs_root()

    if raw in ROOT_DOCS or raw.upper() == "LICENSE":
        name = "LICENSE" if raw.upper() == "LICENSE" else raw
        target = (root / name).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            return None
        return target

    if raw.lower().startswith("docs/"):
        raw = raw[5:]
    target = (docs / raw).resolve()
    try:
        target.relative_to(docs.resolve())
    except ValueError:
        return None
    return target


def _list_docs() -> None:
    root = _project_root()
    docs = _docs_root()
    print("Documentación disponible:")
    print()
    print("Raíz del proyecto:")
    for name in ROOT_DOCS:
        path = root / name
        mark = name if path.is_file() else f"{name} (no está en este clone)"
        print(f"  {mark}")
    print()
    print("docs/:")
    if not docs.is_dir():
        print("  Error: no existe docs/")
        print("  Comprueba que estás en la raíz del proyecto MetsuOS.")
        return
    files = sorted(p for p in docs.rglob("*") if p.is_file())
    if not files:
        print("  (vacío)")
    else:
        for path in files:
            print(f"  {path.relative_to(docs).as_posix()}")
    print()
    print("Uso: docs <ruta>")
    print("Ejemplo: docs README.md")
    print("Ejemplo: docs A11Y.md")
    print("Ejemplo: docs a11y/DECLARACION.md")


def _show_docs(rel: str) -> None:
    target = _resolve(rel)
    if target is None:
        print("Error: la ruta no está permitida.")
        print("Puedes abrir ficheros bajo docs/ o README.md, CHANGELOG.md, AGENTS.md, LICENSE.")
        return
    if not target.is_file():
        print(f"Error: no existe el documento: {rel}")
        print("Usa: docs    (sin argumentos) para listar.")
        return
    text = target.read_text(encoding="utf-8", errors="replace")
    print(text.rstrip())


def execute(args):
    if not args:
        _list_docs()
        return
    _show_docs(" ".join(args).strip())


def help():
    return (
        "Uso: docs - Lista documentación (docs/ y README, CHANGELOG, AGENTS, LICENSE). "
        "Uso: docs <ruta> - Muestra un fichero permitido "
        "(ejemplo: docs README.md, docs A11Y.md)"
    )