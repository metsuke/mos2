"""CRUD del indice docgen."""

from moslib.core.docgen_index import documentos, load_index, save_index


def index_list() -> list:
    return documentos()


def index_add(args) -> str:
    args = list(args or [])
    if len(args) < 3:
        return "[docgen] Uso: docgen index add <id> <rel>"
    doc_id, rel = args[1], args[2]
    data = load_index()
    items = list(data.get("documentos") or [])
    if any(x.get("id") == doc_id for x in items):
        return f"[docgen] ya existe {doc_id}"
    items.append({"id": doc_id, "rel": rel})
    data["documentos"] = items
    save_index(data)
    return f"[docgen] index + {doc_id} -> {rel}"


def index_set(args) -> str:
    args = list(args or [])
    if len(args) < 3:
        return "[docgen] Uso: docgen index set <id> <rel>"
    doc_id, rel = args[1], args[2]
    data = load_index()
    items = list(data.get("documentos") or [])
    for item in items:
        if item.get("id") == doc_id:
            item["rel"] = rel
            save_index(data)
            return f"[docgen] index = {doc_id} -> {rel}"
    return f"[docgen] no esta {doc_id}"


def index_rm(args) -> str:
    args = list(args or [])
    if len(args) < 2:
        return "[docgen] Uso: docgen index rm <id>"
    doc_id = args[1]
    data = load_index()
    antes = list(data.get("documentos") or [])
    despues = [x for x in antes if x.get("id") != doc_id]
    if len(despues) == len(antes):
        return f"[docgen] no esta {doc_id}"
    data["documentos"] = despues
    save_index(data)
    return f"[docgen] index - {doc_id}"
