"""Consulta del tope de 120 líneas en moslib."""

from pathlib import Path

TOPE = 120
RAIZ = Path(__file__).resolve().parent.parent


def lineas(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def excesos() -> list[tuple[int, str]]:
    out = []
    for path in sorted(RAIZ.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        n = lineas(path)
        if n > TOPE:
            out.append((n, path.relative_to(RAIZ).as_posix()))
    return out


def informe() -> str:
    rows = excesos()
    if not rows:
        return (
            f"[tope] ok: ningún .py de moslib supera {TOPE} líneas"
            + "\n"
            + "[tope] total a corregir: 0"
        )
    partes = [f"[tope] {len(rows)} fichero(s) por encima de {TOPE} líneas:"]
    partes.extend(f"[tope] {n:4}  {rel}" for n, rel in rows)
    partes.append(f"[tope] total a corregir: {len(rows)}")
    return "\n".join(partes)
