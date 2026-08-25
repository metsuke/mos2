"""
Comando man de MetsuOS.
Muestra páginas de manual extendido desde docs/man/.
"""

from pathlib import Path


def _project_root() -> Path:
    # moslib/commands/man.py -> raíz del proyecto
    return Path(__file__).resolve().parent.parent.parent


def _man_dir() -> Path:
    return _project_root() / "docs" / "man"


def _list_pages() -> list[str]:
    man_dir = _man_dir()
    if not man_dir.is_dir():
        return []
    return sorted(p.stem for p in man_dir.glob("*.md") if p.is_file())


def _read_page(command_name: str) -> str | None:
    path = _man_dir() / f"{command_name}.md"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def execute(args):
    pages = _list_pages()

    if not args:
        if not pages:
            print("man: no hay páginas de manual en docs/man/")
            return

        print("Páginas de manual disponibles:")
        print("-" * 40)
        for name in pages:
            print(f"  {name}")
        print("-" * 40)
        print("Uso: man <comando>")
        return

    command_name = args[0].strip()
    if not command_name:
        print("man: indica un comando")
        return

    # Permitir pedir "user_xxx" o nombres simples de sistema
    content = _read_page(command_name)
    if content is None:
        print(f"man: no existe página de manual para '{command_name}'")
        if pages:
            print("Disponibles: " + ", ".join(pages))
        return

    print(content)


def help():
    return "Uso: man [comando] - Muestra el manual extendido de un comando (docs/man/)."