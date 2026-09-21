"""Comando docs: menu y visualizacion."""

from moslib.commands.docs_menu import abrir_directo, menu


def execute(args):
    if args:
        abrir_directo(" ".join(args).strip())
        return
    menu()


def help():
    return "Uso: docs (menu; Nh abre html) | docs <ruta>"


def sinopsis():
    return ["docs", "docs <ruta>"]
