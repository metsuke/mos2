"""CRUD del indice docgen (JSON en disco)."""

from moslib.core.docgen_index import load_index, save_index


def index_list() -> list:
    return load_index()


def index_add(args) -> str:
    if len(args) < 3:
        return "[docgen] Uso: docgen index add <id> <rel>"
    clave = args[1].strip().lower()
    rel = args[2].strip().replace("\\", "/")
    items = [i for i in load_index() if i["id"] != clave]
    items.append({"id": clave, "rel": rel})
    save_index(items)
    return f"[docgen] index + {clave} -> {rel}"


def index_set(args) -> str:
    if len(args) < 3:
        return "[docgen] Uso: docgen index set <id> <rel>"
    return index_add(args)


def index_rm(args) -> str:
    if len(args) < 2:
        return "[docgen] Uso: docgen index rm <id>"
    clave = args[1].strip().lower()
    items = [i for i in load_index() if i["id"] != clave]
    save_index(items)
    return f"[docgen] index - {clave}"
