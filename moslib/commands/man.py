"""
Comando man de MetsuOS.
Sistema: docs/man/
Apps: <app>/man/<comando>.md (instalada o cuna apps/ en el clone).
"""

from pathlib import Path

from moslib.core.cmd_loader import invocation_names
from moslib.core.user import get_project_root, get_system_apps_dir, get_user_apps_dir


def _system_man_dir() -> Path:
    return get_project_root() / "docs" / "man"


def _app_roots() -> list[Path]:
    roots = []
    cradle = get_project_root() / "apps"
    if cradle.is_dir():
        roots.append(cradle)
    sysr = get_system_apps_dir()
    if sysr.is_dir():
        roots.append(sysr)
    usr = get_user_apps_dir()
    if usr.is_dir():
        roots.append(usr)
    return roots


def _list_system_pages() -> list[str]:
    man_dir = _system_man_dir()
    if not man_dir.is_dir():
        return []
    return sorted(p.stem for p in man_dir.glob("*.md") if p.is_file())


def _list_app_pages() -> list[tuple[str, str]]:
    found = []
    seen = set()
    for root in _app_roots():
        for app_dir in sorted(root.iterdir()):
            man_dir = app_dir / "man"
            if not app_dir.is_dir() or not man_dir.is_dir():
                continue
            aid = app_dir.name
            for page in sorted(man_dir.glob("*.md")):
                stem = page.stem
                names = invocation_names(aid, stem)
                key = f"{aid}:{stem}"
                if key in seen:
                    continue
                seen.add(key)
                found.append((stem, " ".join(sorted(names))))
    return found


def _read_system(command_name: str) -> str | None:
    path = _system_man_dir() / f"{command_name}.md"
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def _read_app(command_name: str) -> str | None:
    for root in _app_roots():
        for app_dir in sorted(root.iterdir()):
            man_dir = app_dir / "man"
            if not man_dir.is_dir():
                continue
            aid = app_dir.name
            for page in man_dir.glob("*.md"):
                if command_name in invocation_names(aid, page.stem):
                    return page.read_text(encoding="utf-8")
    return None


def execute(args):
    system_pages = _list_system_pages()
    app_pages = _list_app_pages()

    if not args:
        if not system_pages and not app_pages:
            print("man: no hay páginas de manual")
            return
        if system_pages:
            print("Manuales de sistema:")
            for name in system_pages:
                print(f"  {name}")
        if app_pages:
            print("Manuales de app:")
            for stem, aliases in app_pages:
                print(f"  {stem}  ({aliases})")
        print("Uso: man <comando>")
        return

    command_name = args[0].strip()
    if not command_name:
        print("man: indica un comando")
        return

    content = _read_system(command_name)
    if content is None:
        content = _read_app(command_name)
    if content is None:
        print(f"man: no existe página de manual para '{command_name}'")
        return

    print(content)


def help():
    return (
        "Uso: man [comando] - Manual de sistema (docs/man/) "
        "o de app (<app>/man/)."
    )