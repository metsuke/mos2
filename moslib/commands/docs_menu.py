"""Menu y apertura de documentos para docs."""

from pathlib import Path
import subprocess
import sys

ROOT_DOCS = ("README.md", "CHANGELOG.md", "AGENTS.md", "LICENSE")
CATS = (
    ("raiz", "Raiz del clone"),
    ("docs", "Paginas en docs/"),
    ("specs", "Especificaciones"),
    ("man", "Manuales"),
    ("planes", "Planes"),
)
OCULTOS = {".ds_store", "thumbs.db", "desktop.ini"}


def _root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _docs() -> Path:
    return _root() / "docs"


def _visible(path: Path) -> bool:
    n = path.name.lower()
    return path.is_file() and not n.startswith(".") and n not in OCULTOS


def archivos(cat: str) -> list:
    root, docs = _root(), _docs()
    if cat == "raiz":
        return [root / n for n in ROOT_DOCS if _visible(root / n)]
    if cat == "docs":
        if not docs.is_dir():
            return []
        return sorted(p for p in docs.iterdir() if _visible(p))
    mapa = {"specs": docs / "specs", "man": docs / "man", "planes": docs / "plans"}
    base = mapa.get(cat)
    if base is None or not base.is_dir():
        return []
    return sorted(p for p in base.glob("*.md") if _visible(p))


def html_de(path: Path):
    html_dir = _docs() / "docgen" / "html"
    if not html_dir.is_dir():
        return None
    for nombre in (path.stem + ".html", path.name + ".html"):
        cand = html_dir / nombre
        if cand.is_file():
            return cand
    return None


def abrir_sistema(path: Path) -> None:
    if sys.platform == "darwin":
        cmd = ["open", str(path)]
    elif sys.platform == "win32":
        cmd = ["cmd", "/c", "start", "", str(path)]
    else:
        cmd = ["xdg-open", str(path)]
    subprocess.Popen(cmd)


def elige(titulo: str, filas: list):
    print("[docs] " + titulo)
    for i, texto in enumerate(filas, 1):
        print(f"  {i}) {texto}")
    print("  0) salir   Nh = html en el navegador")
    bruto = input("[docs] numero: ").strip().lower()
    if bruto in ("", "0", "q"):
        return None, False
    html = bruto.endswith("h")
    if html:
        bruto = bruto[:-1]
    if not bruto.isdigit():
        print("[docs] no es un numero")
        return None, False
    n = int(bruto)
    if n < 1 or n > len(filas):
        print("[docs] fuera de rango")
        return None, False
    return n - 1, html


def mostrar(path: Path) -> None:
    print(path.read_text(encoding="utf-8", errors="replace").rstrip())


def abrir_directo(bruto: str) -> None:
    cand = _root() / bruto
    if not cand.is_file():
        cand = _docs() / bruto
    if not cand.is_file():
        print("[docs] no existe: " + bruto)
        return
    mostrar(cand)


def menu() -> None:
    presentes = [c for c in CATS if archivos(c[0])]
    i, _ = elige("Categorias", [f"{c[1]} ({len(archivos(c[0]))})" for c in presentes])
    if i is None:
        return
    files = archivos(presentes[i][0])
    j, quiere_html = elige(presentes[i][1], [p.name for p in files])
    if j is None:
        return
    path = files[j]
    if not quiere_html:
        mostrar(path)
        return
    html = html_de(path)
    if html is None:
        print("[docs] no hay html de " + path.name)
        return
    abrir_sistema(html)
    print("[docs] html: " + str(html))
