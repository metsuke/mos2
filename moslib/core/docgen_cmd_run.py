"""Ingesta y generate del comando docgen."""

from moslib.core import docgen as motor
from moslib.core import docgen_cli as cli
from moslib.core import docgen_plan as planes
from moslib.core import docgen_req as reqs


def ingest(objetivo: str) -> None:
    print("[docgen] Ingesta: solo primera vez o recuperación.")
    try:
        if objetivo in ("plans", "plan", "planes"):
            cli.mostrar("[docgen] Planes absorbidos:", planes.ingest_planes())
        elif objetivo in ("reqs", "req", "requisitos"):
            cli.mostrar("[docgen] Requisitos absorbidos:", reqs.ingest_reqs_srs())
        elif objetivo in ("", "man", "all-man"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_man_todos(forzar=True))
        elif objetivo in ("specs", "spec", "all-specs"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_spec_todos(forzar=True))
        elif objetivo in ("pages", "page", "docs"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_page_todos(forzar=True))
        elif objetivo in ("all", "todo"):
            cli.mostrar("[docgen] Absorbidos:", motor.ingest_todo())
        elif objetivo.startswith("man-") or objetivo in motor.list_man_nombres():
            nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
            print(f"[docgen] Absorbido en {motor.ingest_man(nombre)}")
        else:
            print(f"[docgen] Absorbido en {motor.ingest_doc(objetivo)}")
    except Exception as exc:
        print(f"[docgen] Ingesta fallida: {exc}")


def generate(objetivo: str) -> None:
    try:
        if objetivo in ("", "man", "all-man"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_man_todos())
        elif objetivo in ("specs", "spec", "all-specs"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_spec_todos())
        elif objetivo in ("pages", "page", "docs"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_page_todos())
        elif objetivo in ("all", "todo"):
            cli.mostrar("[docgen] Regenerados:", motor.generate_todo())
        elif objetivo.startswith("man-") or objetivo in motor.list_man_nombres():
            nombre = objetivo[4:] if objetivo.startswith("man-") else objetivo
            print(f"[docgen] Regenerado {motor.generate_man(nombre)}")
        else:
            print(f"[docgen] Regenerado {motor.generate_doc(objetivo)}")
    except Exception as exc:
        print(f"[docgen] No se ha escrito: {exc}")
