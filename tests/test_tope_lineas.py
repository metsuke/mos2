"""Ningún .py de moslib por encima de 120 líneas, salvo lista blanca temporal."""

from pathlib import Path

TOPE = 120
RAIZ = Path(__file__).resolve().parent.parent / "moslib"
BLANCOS = {
    "core/docgen.py",
    "core/docgen_req.py",
    "core/docgen_plan.py",
    "core/docgen_html.py",
    "core/entorno.py",
    "commands/docgen.py",
    "commands/help.py",
    "commands/iarouter.py",
    "commands/docs.py",
}


def _lineas(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def test_moslib_no_supera_120_salvo_blancos():
    faltan = []
    sobran_blancos = []
    for path in sorted(RAIZ.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = path.relative_to(RAIZ).as_posix()
        n = _lineas(path)
        if rel in BLANCOS:
            if n <= TOPE:
                sobran_blancos.append(rel)
            continue
        if n > TOPE:
            faltan.append(f"{rel}: {n}")
    assert not faltan, "partir estos ficheros (<=120):\n" + "\n".join(faltan)
    assert not sobran_blancos, "quitar de BLANCOS (ya caben):\n" + "\n".join(
        sobran_blancos
    )