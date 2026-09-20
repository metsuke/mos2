"""Git de ramas de desarrollo (no main)."""

from pathlib import Path

from moslib.core.update_git import run


def raiz() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def rama_actual(cwd: Path) -> str:
    r = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd, check=False)
    return (r.stdout or "").strip()


def sucio(cwd: Path) -> bool:
    r = run(["git", "status", "--porcelain"], cwd, check=False)
    return bool((r.stdout or "").strip())


def ramas_remotas(cwd: Path) -> list[str]:
    run(["git", "fetch", "origin"], cwd, check=False)
    r = run(["git", "branch", "-r"], cwd, check=False)
    out = []
    for line in (r.stdout or "").splitlines():
        name = line.strip().lstrip("* ").strip()
        if name.startswith("origin/") and "->" not in name:
            corta = name[len("origin/"):]
            if corta != "main":
                out.append(corta)
    return sorted(set(out))


def checkout_rama(cwd: Path, rama: str) -> None:
    run(["git", "checkout", rama], cwd, check=False)
    run(["git", "pull", "origin", rama], cwd, check=False)
