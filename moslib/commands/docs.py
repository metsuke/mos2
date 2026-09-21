"""Comando docs: menu por categoria y visualizacion."""

from pathlib import Path

ROOT_DOCS = ("README.md", "CHANGELOG.md", "AGENTS.md", "LICENSE")
CATS = (
    ("raiz", "Raiz del clone"),
    ("docs", "Paginas en docs/"),
    ("specs", "Especificaciones"),
    ("man", "Manuales"),
    ("planes", "Planes"),
)


def _root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _docs() -> Path:
    return _root() / "docs"


def _archivos(cat: str) -> list:
    root, docs = _root(), _docs()
    if cat == "raiz":
        return [root / n for n in ROOT_DOCS if (root / n).is_file()]
    if cat == "docs":
        if not docs.is_dir():
            return []
        return sorted(p for p in docs.iterdir() if p.is_file())
    mapa = {"specs": docs / "specs", "man": docs / "man", "planes": docs / "plans"}
    base = mapa.get(cat)
    if base is None or not base.is_dir():
        return []
    return sorted(base.glob("*.md"))


def _elige(titulo: str, filas: list) -> int | None:
    print("[docs] " + titulo)
    for i, texto in enumerate(filas, 1):
        print(f"  {i}) {texto}")
    print("  0) salir")
    bruto = input("[docs] numero: ").strip().lower()
    if bruto in ("", "0", "q"):
        return None
    if not bruto.isdigit():
        print("[docs] no es un numero")
        return None
    n = int(bruto)
    if n < 1 or n > len(filas):
        print("[docs] fuera de rango")
        return None
    return n - 1


def _mostrar(path: Path) -> None:
    texto = path.read_text(encoding="utf-8", errors="replace")
    print(texto.rstrip())


def execute(args):
    if args:
        bruto = " ".join(args).strip()
        cand = _root() / bruto
        if not cand.is_file():
            cand = _docs() / bruto
        if not cand.is_file():
            print("[docs] no existe: " + bruto)
            return
        _mostrar(cand)
        return
    presentes = [c for c in CATS if _archivos(c[0])]
    i = _elige("Categorias", [f"{c[1]} ({len(_archivos(c[0]))})" for c in presentes])
    if i is None:
        return
    cat = presentes[i][0]
    files = _archivos(cat)
    j = _elige(presentes[i][1], [p.name for p in files])
    if j is None:
        return
    _mostrar(files[j])


def help():
    return "Uso: docs  (menu)  |  docs <ruta>  (abre directo)"


def sinopsis():
    return ["docs", "docs <ruta>"]
