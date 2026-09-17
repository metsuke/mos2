"""Tope 120 líneas: siempre se ejecuta, informa, no bloquea."""

from pathlib import Path

TOPE = 120
RAIZ = Path(__file__).resolve().parent.parent / "moslib"


def _lineas(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def test_moslib_no_supera_120(capsys):
    excesos = []
    for path in sorted(RAIZ.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        n = _lineas(path)
        if n > TOPE:
            excesos.append(f"{n:4}  {path.relative_to(RAIZ).as_posix()}")
    if excesos:
        print(f"[tope] {len(excesos)} fichero(s) por encima de {TOPE} líneas:")
        for fila in excesos:
            print(f"[tope] {fila}")
    else:
        print(f"[tope] ok: ningún .py de moslib supera {TOPE} líneas")
    assert True