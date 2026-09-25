"""CRUD de tuplas. Relaciones bidireccionales."""

from __future__ import annotations

from moslib.core.docgen_tupla import CAMPOS, guardar_tupla, load_tupla, plantilla
from moslib.core.docgen_tupla_path import normalizar_id, tupla_path, tuplas_root


def tupla_add(ident: str, tipo: str = "elemento"):
    ident = normalizar_id(ident)
    if tupla_path(ident).is_file():
        raise FileExistsError(ident)
    return guardar_tupla(plantilla(ident, tipo))


def tupla_set(ident: str, campo: str, valor: str):
    ident = normalizar_id(ident)
    if campo not in CAMPOS or campo in ("schema", "id", "creado"):
        raise ValueError(f"campo no válido: {campo}")
    data = load_tupla(ident)
    if campo in ("influye_de", "influye_a"):
        raise ValueError("usa tupla link")
    if campo == "orden":
        data[campo] = int(valor)
    elif campo == "activo":
        data[campo] = valor.strip().lower() in ("1", "true", "si", "sí", "on")
    else:
        data[campo] = valor
    return guardar_tupla(data)


def tupla_rm(ident: str):
    ident = normalizar_id(ident)
    path = tupla_path(ident)
    if not path.is_file():
        raise FileNotFoundError(ident)
    path.unlink()
    return path


def list_tuplas(prefijo: str = "") -> list:
    root = tuplas_root()
    items = []
    for path in sorted(root.rglob("*.json")):
        ident = path.with_suffix("").relative_to(root).as_posix()
        if prefijo and not ident.startswith(prefijo.strip("/")):
            continue
        items.append(load_tupla(ident))
    return items


def _lista(data: dict, campo: str) -> list:
    return list(data.get(campo) or [])


def tupla_link(origen: str, destino: str):
    origen = normalizar_id(origen)
    destino = normalizar_id(destino)
    a = load_tupla(origen)
    b = load_tupla(destino)
    if destino not in _lista(a, "influye_a"):
        a["influye_a"] = _lista(a, "influye_a") + [destino]
    if origen not in _lista(b, "influye_de"):
        b["influye_de"] = _lista(b, "influye_de") + [origen]
    guardar_tupla(a)
    return guardar_tupla(b)
