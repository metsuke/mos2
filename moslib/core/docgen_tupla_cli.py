"""CLI docgen tupla."""

from moslib.core import docgen_tupla_crud as crud
from moslib.core.docgen_tupla_gen import generate_tupla
from moslib.core.docgen_tupla_render import sembrar_modos
from moslib.core.docgen_tupla_req import migrar_reqs


def tupla(args):
    if not args or args[0] == "list":
        pref = args[1] if len(args) > 1 else ""
        items = crud.list_tuplas(pref)
        if not items:
            print("[docgen] No hay tuplas.")
            return
        for item in items:
            ident = item.get("id") or ""
            tipo = item.get("tipo") or ""
            titulo = item.get("titulo") or ""
            print(f"  {ident:40} {tipo:10} {titulo}")
        return
    try:
        if args[0] in ("migrar-reqs", "migrate-reqs"):
            paths = migrar_reqs(forzar="forzar" in args)
            print("[docgen] Requisitos ya en tuplas." if not paths else f"[docgen] Migrados {len(paths)}")
            return
        if args[0] in ("sembrar-render", "migrar-render"):
            paths = sembrar_modos(forzar="forzar" in args)
            print("[docgen] Modos ya sembrados." if not paths else f"[docgen] Modos {len(paths)}")
            return
        if args[0] in ("generate", "gen") and len(args) >= 2:
            dest = generate_tupla(args[1])
            print(f"[docgen] Tupla MD {dest}")
            return
        if args[0] == "add" and len(args) >= 2:
            tipo = args[2] if len(args) > 2 else "elemento"
            print(f"[docgen] Tupla {crud.tupla_add(args[1], tipo)}")
            return
        if args[0] == "set" and len(args) >= 4:
            print(f"[docgen] Tupla {crud.tupla_set(args[1], args[2], chr(32).join(args[3:]))}")
            return
        if args[0] == "link" and len(args) >= 3:
            print(f"[docgen] Enlace {crud.tupla_link(args[1], args[2])}")
            return
        if args[0] == "rm" and len(args) >= 2:
            print(f"[docgen] Eliminada {crud.tupla_rm(args[1])}")
            return
    except Exception as exc:
        print(f"[docgen] tupla: {exc}")
        return
    print("[docgen] Uso: docgen tupla list|add|set|link|rm|migrar-reqs|sembrar-render|generate")
